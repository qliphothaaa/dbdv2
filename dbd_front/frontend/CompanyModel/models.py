# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DbdNewQuery(models.Model):
    dbd_company_id = models.CharField(db_column='DBD_COMPANY_ID', primary_key=True, max_length=45)  # Field name made lowercase.
    dbd_typecode = models.CharField(db_column='DBD_TYPECODE', max_length=45, blank=True, null=True)  # Field name made lowercase.
    dbd_status = models.TextField(db_column='DBD_STATUS', blank=True, null=True)  # Field name made lowercase.
    dbd_last_run = models.DateTimeField(db_column='DBD_LAST_RUN', blank=True, null=True)  # Field name made lowercase.
    dbd_ignore = models.IntegerField(db_column='DBD_IGNORE', blank=True, null=True)  # Field name made lowercase.
    dbd_change = models.IntegerField(db_column='DBD_CHANGE', blank=True, null=True)  # Field name made lowercase.
    c_dbd_name_th = models.TextField(db_column='C_DBD_NAME_TH', blank=True, null=True)  # Field name made lowercase.
    c_dbd_status = models.TextField(db_column='C_DBD_STATUS', blank=True, null=True)  # Field name made lowercase.
    c_dbd_objective = models.TextField(db_column='C_DBD_OBJECTIVE', blank=True, null=True)  # Field name made lowercase.
    c_dbd_business_type = models.TextField(db_column='C_DBD_BUSINESS_TYPE', blank=True, null=True)  # Field name made lowercase.
    c_dbd_address = models.TextField(db_column='C_DBD_ADDRESS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dbd_new_query'


class DbdQuery(models.Model):
    dbd_company_id = models.CharField(db_column='DBD_COMPANY_ID', primary_key=True, max_length=45)  # Field name made lowercase.
    dbd_typecode = models.CharField(db_column='DBD_TYPECODE', max_length=45, blank=True, null=True)  # Field name made lowercase.
    dbd_status = models.TextField(db_column='DBD_STATUS', blank=True, null=True)  # Field name made lowercase.
    dbd_last_run = models.DateTimeField(db_column='DBD_LAST_RUN', blank=True, null=True)  # Field name made lowercase.
    dbd_ignore = models.IntegerField(db_column='DBD_IGNORE', blank=True, null=True)  # Field name made lowercase.
    dbd_change = models.IntegerField(db_column='DBD_CHANGE', blank=True, null=True)  # Field name made lowercase.
    c_dbd_name_th = models.TextField(db_column='C_DBD_NAME_TH', blank=True, null=True)  # Field name made lowercase.
    c_dbd_status = models.TextField(db_column='C_DBD_STATUS', blank=True, null=True)  # Field name made lowercase.
    c_dbd_objective = models.TextField(db_column='C_DBD_OBJECTIVE', blank=True, null=True)  # Field name made lowercase.
    c_dbd_business_type = models.TextField(db_column='C_DBD_BUSINESS_TYPE', blank=True, null=True)  # Field name made lowercase.
    c_dbd_address = models.TextField(db_column='C_DBD_ADDRESS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dbd_query'


class Dbdcompany(models.Model):
    dbd_id = models.CharField(db_column='DBD_ID', primary_key=True, max_length=45)  # Field name made lowercase.
    dbd_type = models.CharField(db_column='DBD_TYPE', max_length=45, blank=True, null=True)  # Field name made lowercase.
    dbd_name_th = models.CharField(db_column='DBD_NAME_TH', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dbd_name_en = models.CharField(db_column='DBD_NAME_EN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dbd_registration_date = models.DateField(db_column='DBD_REGISTRATION_DATE', blank=True, null=True)  # Field name made lowercase.
    dbd_status = models.CharField(db_column='DBD_STATUS', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dbd_registration_money = models.BigIntegerField(db_column='DBD_REGISTRATION_MONEY', blank=True, null=True)  # Field name made lowercase.
    dbd_address = models.TextField(db_column='DBD_ADDRESS', blank=True, null=True)  # Field name made lowercase.
    dbd_objective = models.TextField(db_column='DBD_OBJECTIVE', blank=True, null=True)  # Field name made lowercase.
    dbd_street = models.TextField(db_column='DBD_STREET', blank=True, null=True)  # Field name made lowercase.
    dbd_subdistrict = models.TextField(db_column='DBD_SUBDISTRICT', blank=True, null=True)  # Field name made lowercase.
    dbd_district = models.TextField(db_column='DBD_DISTRICT', blank=True, null=True)  # Field name made lowercase.
    dbd_province = models.TextField(db_column='DBD_PROVINCE', blank=True, null=True)  # Field name made lowercase.
    dbd_zipcode = models.CharField(db_column='DBD_ZIPCODE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dbd_business_type_code = models.TextField(db_column='DBD_BUSINESS_TYPE_CODE', blank=True, null=True)  # Field name made lowercase.
    dbd_business_type = models.TextField(db_column='DBD_BUSINESS_TYPE', blank=True, null=True)  # Field name made lowercase.
    dbd_directors = models.TextField(db_column='DBD_DIRECTORS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dbdcompany'
