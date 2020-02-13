from rest_framework import serializers
from CompanyModel.models import Dbdcompany, DbdNewQuery, DbdQuery


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dbdcompany
        fields = '__all__'
        #fields = ('')


class NewQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = DbdNewQuery
        fields = '__all__'
        #fields = ('')


class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = DbdQuery
        fields = '__all__'
        #fields = ('')
