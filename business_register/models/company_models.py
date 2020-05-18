from data_ocean.models.common_models import Authority, Status, TaxpayerType
from data_ocean.models.main import DataOceanModel
from data_ocean.models.kved_models import Kved
from data_ocean.models.ruo_models import State
from django.db import models
from simple_history.models import HistoricalRecords

class Bylaw(DataOceanModel):
    name = models.CharField(max_length=100, unique=True)

class CompanyType(DataOceanModel):
    name = models.CharField(max_length=100, unique=True)

class Company(DataOceanModel): #constraint for not null in both name & short_name fields
    INVALID = 'invalid' #constant for empty edrpou fild etc.
    name = models.CharField(max_length=500, null=True)
    short_name = models.CharField(max_length=500, null=True)
    company_type = models.ForeignKey(CompanyType, on_delete=models.CASCADE)
    edrpou = models.CharField(max_length=50)
    address = models.CharField(max_length=500, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    bylaw = models.ForeignKey(Bylaw, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(null=True)
    registration_info = models.CharField(max_length=100, null=True)
    contact_info = models.CharField(max_length=100, null=True)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    history = HistoricalRecords()

class Assignee(DataOceanModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)

class BancruptcyReadjustment(DataOceanModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    op_date = models.DateTimeField(null=True)
    reason = models.TextField(null=True)
    sbj_state = models.CharField(max_length=100, null=True)
    head_name = models.CharField(max_length=300, null=True)

class CompanyDetail(DataOceanModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    founding_document_number = models.CharField(max_length=100, null=True)
    executive_power = models.CharField(max_length=100, null=True)
    superior_management = models.CharField(max_length=100, null=True)
    authorized_capital = models.CharField(max_length=100, null=True)
    managing_paper = models.CharField(max_length=100, null=True)
    terminated_info = models.CharField(max_length=100, null=True)
    termination_cancel_info = models.CharField(max_length=100, null=True)
    vp_dates = models.CharField(max_length=100, null=True)
    history = HistoricalRecords()

class CompanyToKved(DataOceanModel): #constraint for only only one truth in primary field
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    kved = models.ForeignKey(Kved, on_delete=models.CASCADE)
    primary_kved = models.BooleanField(default=False)

class ExchangeDataCompany(DataOceanModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)
    taxpayer_type = models.ForeignKey(TaxpayerType, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True)
    start_number = models.CharField(max_length=20, null=True)
    end_date = models.DateTimeField(null=True)
    end_number = models.CharField(max_length=20, null=True)

class FounderFull(DataOceanModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.TextField(null=True)

class Predecessor(DataOceanModel): #constraint for not null in both fields
    name = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=100, null=True)

class CompanyToPredecessor(DataOceanModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    predecessor = models.ForeignKey(Predecessor, on_delete=models.CASCADE)

class Signer(DataOceanModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, null=True)

class TerminationStarted(DataOceanModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    op_date = models.DateTimeField(null=True)
    reason = models.TextField(null=True)
    sbj_state = models.CharField(max_length=100, null=True)
    signer_name = models.CharField(max_length=300, null=True)
    creditor_reg_end_date = models.DateTimeField(null=True)