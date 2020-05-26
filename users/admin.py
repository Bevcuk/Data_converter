from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import DataOceanUser


class DataOceanUserAdmin(UserAdmin):
    model = DataOceanUser
    list_display = ['email', 'username', ]


admin.site.register(DataOceanUser, DataOceanUserAdmin)