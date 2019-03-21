from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:

        model  = Customer
        fields = ('id','address','professions','data_sheet','name','active')

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:

        model   = Profession
        fields  = ('id','description')

class DatasheetSerializer(serializers.ModelSerializer):
    class Meta:

        model   =  DataSheet
        fields  = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:

        model   =  Document
        fields  =  ('id','dtype','doc_number','customer')
