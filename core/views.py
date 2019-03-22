from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import viewsets
from rest_framework.response import Response
from django.http.response import HttpResponseNotAllowed
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter,OrderingFilter

#return the Active users 
#override the default behaviours with 4 Methods. 
#creating custom Actions
class CustomerViewset(viewsets.ModelViewSet):
    #queryset            = Customer.objects.all()
    filter_backends  = (SearchFilter, OrderingFilter)
    serializer_class = CustomerSerializer
    filter_fields =('name', )
    search_fields = ('name','address', )
    ordering_fields =('id', 'name','address', )
    ordering =('id' )
    # search_fields = ('=name','=address', )Exact String search 
    # lookup_field = ('name') #but this field should be uniq
    def get_queryset(self):
        address = self.request.query_params.get('address',None)
        if address:
            customers = Customer.objects.filter(address__icontains=address, active=True)
        else:
            customers = Customer.objects.filter(active=True)
        return customers 
    # def list(self,request, *args,**kwargs):
    #     customers = self.get_queryset()
    #     #customers = Customer.objects.all()
    #     #customers = Customer.objects.filter(id=4)
    #     serializer = CustomerSerializer(customers,many=True)
    #     return Response(serializer.data)
    def retrieve(self,request, *args,**kwargs):
        #return HttpResponseNotAllowed('Not allowed')
        obj = self.get_object()
        serializer = CustomerSerializer(obj)
        return Response(serializer.data)
        #return Response({'message':'Not Allowed'})
    def create(self,request, *args,**kwargs):
        data = request.data
        customer = Customer.objects.create(
            name    = data['name'],
            address = data['address'],
            data_sheet_id = data['data_sheet'] 
        )
        profession = Profession.objects.get(id=data['professions'])
        customer.professions.add(profession)
        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    def update(self,request, *args,**kwargs):
        #customer = Customer.objects.get(pk=kwargs)
        customer = self.get_object()
        data = request.data
        customer.name = data['name']
        customer.address = data['address']
        customer.data_sheet_id = data['data_sheet']
        profession = Profession.objects.get(id=data['professions'])
        #Remove objects from admin panel.
        for p in customer.professions.all():
            customer.professions.remove(p) 

        customer.professions.add(profession)
        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    
    def partial_update(self,request, *args,**kwargs):
        customer = self.get_object()
        customer.name = request.data.get('name',customer.name)
        customer.address = request.data.get('address',customer.address)
        customer.data_sheet_id = request.data.get('data_sheet',customer.data_sheet_id)
        customer.save()
        
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)     

    def destroy(self,request, *args,**kwargs):
        customer = self.get_object()
        customer.delete()
        return Response('Object Removed')
    
    #Deactivate particular record when detail=True is enabled.
    @action(detail=True)
    def deactivate(self,request, *args,**kwargs):
        customer = self.get_object()
        customer.active = False
        customer.save()

        serializer = CustomerSerializer(customer,many=True)
        return Response(serializer.data)    

    @action(detail=False)
    def deactivate_all(self,request, *args,**kwargs):
        #customer = Customer.objects.all()
        customer = self.get_queryset()
        customer.update(active=False)
        
        serializer = CustomerSerializer(customer,many=True)
        return Response(serializer.data)    

    @action(detail=False)
    def activate_all(self,request, *args,**kwargs):
        #customer = Customer.objects.all()
        customer = self.get_queryset()
        customer.update(active=True)

        serializer = CustomerSerializer(customer,many=True)
        return Response(serializer.data)    
    @action(detail=False, methods=['POST'])
    def change_status(self,request, *args,**kwargs):
        status = True if request.data['active'] == 'True' else False

        customer = self.get_queryset()
        customer.update(active=status)

        serializer = CustomerSerializer(customer,many=True)
        return Response(serializer.data)    

class ProfessionViewset(viewsets.ModelViewSet):
    queryset            = Profession.objects.all()
    serializer_class    = ProfessionSerializer

class DatasheetViewset(viewsets.ModelViewSet):
    queryset            = DataSheet.objects.all()
    serializer_class    = DatasheetSerializer

class DocumentViewset(viewsets.ModelViewSet):
    queryset            = Document.objects.all()
    serializer_class    = DocumentSerializer
