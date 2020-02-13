from django.contrib import admin
from CompanyModel.models import Dbdcompany, DbdQuery, DbdNewQuery

# Register your models here.
admin.site.register([Dbdcompany, DbdQuery, DbdNewQuery])
