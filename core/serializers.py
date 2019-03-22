from rest_framework import serializers
from .models import *

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:

        model   = Profession
        fields  = ('id','description')


class CustomerSerializer(serializers.ModelSerializer):
    
    num_professions = serializers.SerializerMethodField()
    data_sheet   = serializers.StringRelatedField()
    #professions  = serializers.StringRelatedField(many=True)
    professions = ProfessionSerializer(many=True)

    class Meta:
        model  = Customer
        fields = ('id','address','professions','data_sheet',
        'name','active','status_message','num_professions')
        
    def get_num_professions(self, obj):
        return obj.num_professions()

class DatasheetSerializer(serializers.ModelSerializer):
    class Meta:

        model   =  DataSheet
        fields  = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:

        model   =  Document
        fields  =  ('id','dtype','doc_number','customer')
