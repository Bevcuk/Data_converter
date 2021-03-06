from data_ocean.converter import Converter
from location_register.models import Region, District, City, Citydistrict


class KoatuuConverter(Converter):

    #paths for the local souce file
    LOCAL_FILE_NAME = "koatuu.json"
    DATASET_ID = "dc081fb0-f504-4696-916c-a5b24312ab6e"

    #constants from json file
    LEVEL_ONE = 'Перший рівень'
    LEVEL_TWO = 'Другий рівень'
    LEVEL_THREE = 'Третій рівень'
    LEVEL_FOUR= 'Четвертий рівень'
    OBJECT_NAME = "Назва об'єкта українською мовою"

    #geting all words before virgule and changing string to lowercase
    def get_lowercase_words_before_virgule(self, string):
        return string.lower().split('/')[0]

    #creating a dictionary out off the values, which already exists in region table
    def create_dictionary_for(self, table_model):#table_medel is one model from ratu_models
        koatuu_dict = {}
        table_model_objects = table_model.objects.all()
        for table_record in table_model_objects: # dictionary for keeping whole model class objects
            if (table_record.name):
                unit_name = table_record.name
                koatuu_dict[unit_name]=table_record
        return koatuu_dict

    #creating a dictionary out off the values, which already exists in city table
    def create_dictionary_for_city_table(self, table_model):#table_medel is one model from ratu_models
        koatuu_dict = {}
        table_model_objects = table_model.objects.all()
        for table_record in table_model_objects: # dictionary for keeping whole model class objects
            if (table_record.name):
                unit_name = table_record.name + str(table_record.district_id)
                koatuu_dict[unit_name]=table_record
        return koatuu_dict

    #creating a dictionary out off the values, which already exists in district y city table
    def create_dictionary_for_district_table(self, table_model):#table_medel is one model from ratu_models
        koatuu_dict = {}
        table_model_objects = table_model.objects.all()
        for table_record in table_model_objects: # dictionary for keeping whole model class objects
            if (table_record.name):
                unit_name = table_record.name + str(table_record.region_id)
                koatuu_dict[unit_name]=table_record
        return koatuu_dict

    #creating a dictionary out off the values, which already exists in citydistrict table
    def create_dictionary_for_citydistrict_table(self):#table_medel is one model from ratu_models
        koatuu_dict = {}
        table_model_objects = Citydistrict.objects.all()
        for table_record in table_model_objects: # dictionary for keeping whole model class objects
            if (table_record.name):
                unit_name = table_record.name + str(table_record.city_id)
                koatuu_dict[unit_name]=table_record
        return koatuu_dict
    

    #creating list out of name and district_id from json file for district items
    def create_district_items_list(self, object_koatuu, object_region_name, region_dict, object_district_name, KOATUU_VALUE):
        district_items_list = []
        if not (object_region_name in region_dict):
            return
        region_koatuu = region_dict[object_region_name]            
        if not (KOATUU_VALUE[:2] == str(region_koatuu.koatuu)[:2]):
            return
        object_district_name = object_district_name + str(region_koatuu.id)
        district_items_list.append(object_district_name)
        return district_items_list

    #creating list out of name and district_id from json file fot city items
    def create_city_items_list(self, data, object_koatuu, city_dict, district_items_list, KOATUU_VALUE):
        city_list =[]
        for object_district_name in district_items_list:
            if (object_district_name in city_dict) & (KOATUU_VALUE[2] =='1'):
                city_koatuu = city_dict[object_district_name]
                city_list.append(city_koatuu.name + str(city_koatuu.district_id))
            return city_list

    #storing data to all tables
    def save_to_db(self,data):
        region_dict = self.create_dictionary_for(Region)
        district_dict = self.create_dictionary_for_district_table(District)
        city_dict_for_district_table = self.create_dictionary_for_district_table(City)
        city_dict = self.create_dictionary_for_city_table(City)
        citydistrict_dict = self.create_dictionary_for_citydistrict_table()
        #getting values in json file Koatuu
        for index, object_koatuu in enumerate(data):
            if (object_koatuu[self.LEVEL_ONE]!='') & (object_koatuu[self.LEVEL_TWO]==''):
                object_region_name = self.get_lowercase_words_before_virgule(object_koatuu[self.OBJECT_NAME])
                self.save_to_region_table(data, object_koatuu, region_dict, object_region_name)
            if (object_koatuu[self.LEVEL_ONE]!='') & (object_koatuu[self.LEVEL_TWO]!='') & (object_koatuu[self.LEVEL_THREE]==''):
                KOATUU_VALUE = str(object_koatuu[self.LEVEL_TWO]) #position in koatuu wich defines district or city record 
                object_district_name = self.get_lowercase_words_before_virgule(object_koatuu[self.OBJECT_NAME])
                district_items_list = self.create_district_items_list(object_koatuu, object_region_name, region_dict, object_district_name, KOATUU_VALUE)
                city_items_list = self.create_city_items_list(data, object_koatuu, city_dict_for_district_table, district_items_list, KOATUU_VALUE)
                self.save_to_district_table(data, object_koatuu, district_dict, city_dict_for_district_table, object_region_name, region_dict, district_items_list, KOATUU_VALUE)
            if (object_koatuu[self.LEVEL_ONE]!='') & (object_koatuu[self.LEVEL_TWO]!='') & (object_koatuu[self.LEVEL_THREE]!='') & (object_koatuu[self.LEVEL_FOUR]==''):
                object_city_name = self.get_lowercase_words_before_virgule(object_koatuu[self.OBJECT_NAME])
                object_level_three = object_koatuu[self.LEVEL_THREE]
                self.save_to_city_or_citydistrict_table(data, object_level_three, object_city_name, district_items_list, district_dict, city_dict)
                self.save_to_city_or_citydistrict_table(data, object_level_three, object_city_name, city_items_list, city_dict, citydistrict_dict)
            if (object_koatuu[self.LEVEL_ONE]!='') & (object_koatuu[self.LEVEL_TWO]!='') & (object_koatuu[self.LEVEL_THREE]!='') & (object_koatuu[self.LEVEL_FOUR]!=''):
                object_citydistrict_name = self.get_lowercase_words_before_virgule(object_koatuu[self.OBJECT_NAME])
                object_level_four = object_koatuu[self.LEVEL_FOUR]
                self.save_to_city_or_citydistrict_table(data, object_level_four, object_citydistrict_name, district_items_list, district_dict, city_dict)
                self.save_to_city_or_citydistrict_table(data, object_level_four, object_citydistrict_name, city_items_list, city_dict, citydistrict_dict)
        print("Koatuu values saved")
       
    #writing entry to koatuu field in region table
    def save_to_region_table(self, data, object_koatuu, region_dict, object_region_name):
        if  not object_region_name in region_dict:
            return
        region_koatuu = region_dict[object_region_name]
        region_koatuu.koatuu = object_koatuu[self.LEVEL_ONE]
        region_koatuu.save(update_fields=['koatuu'])
            
    #writing entry to koatuu field in district table and level_two records of city_table
    def save_to_district_table(self, data, object_koatuu, district_dict, city_dict, object_region_name, region_dict, district_items_list, KOATUU_VALUE):
        for object_district_name in district_items_list:
            if (object_district_name in district_dict) & (KOATUU_VALUE[2]!='1'):
                district_koatuu = district_dict[object_district_name]
                district_koatuu.koatuu = object_koatuu[self.LEVEL_TWO]
                district_koatuu.save(update_fields=['koatuu'])
            elif (object_district_name in city_dict) & (KOATUU_VALUE[2]=='1'):
                city_koatuu = city_dict[object_district_name]
                city_koatuu.koatuu = object_koatuu[self.LEVEL_TWO]
                city_koatuu.save(update_fields=['koatuu'])

    #writing entry to koatuu field in city and citydistrict table
    def save_to_city_or_citydistrict_table(self, data, object_level_number, object_level_name, level_items_list, up_level_dict, level_dict):
        for object_name in level_items_list:
            if not object_name in up_level_dict:
                return
            up_level_koatuu = up_level_dict[object_name]
            if not str(object_level_number)[:5] == str(up_level_koatuu.koatuu)[:5]:
                return
            object_level_name = object_level_name + str(up_level_koatuu.id)
            if not (object_level_name in level_dict):
                return
            level_koatuu = level_dict[object_level_name]
            level_koatuu.koatuu = object_level_number
            level_koatuu.save(update_fields=['koatuu'])