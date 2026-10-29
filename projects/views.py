from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from django.contrib.auth.models import User

from projects import serializers
from projects import models

### Users CRUD
#List
class UserListAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        data = serializers.UserSerializerList(users, many=True).data
        return Response(data)

#detail
class UserDetailAPIView(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        data = serializers.UserSerializerDetail(user).data
        return Response(data)


### Banks CRUD

#create
class BankCreateAPIView(generics.CreateAPIView):
    queryset = models.Bank.objects.all()
    serializer_class = serializers.BankSerializerCreate

class createUserApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    #llamado al serializador
    serializer_class = serializers.CreateUserSerializer

#retrieve

#list
class BankListAPIView(APIView):
    def get(self, request):
        banks = models.Bank.objects.all()
        data = serializers.BankSerializerList(banks, many=True).data
        return Response(data)


#detail
class BankDetailAPIView(APIView):
    def get(self, request, pk):
        bank = models.Bank.objects.get(pk=pk)
        data = serializers.BankSerializerDetail(bank, many=False).data
        return Response(data)
    
#update
class BankUpdateAPIView(APIView):
    def put(self, request, pk):
        bank = models.Bank.objects.get(pk=pk)
        data = serializers.BankSerializerUpdate(bank, data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data)
        return Response(data.errors, status=400)

#delete

class BankDeleteAPIView(APIView):
    def delete(self, request, pk):
        bank = models.Bank.objects.get(pk=pk)
        bank.delete()
        return Response({"message": "Banco eliminado correctamente"})

### Accounts CRUD
class AccountListAPIView(APIView):
    def get(self, request):
        accounts = models.Account.objects.all()
        data = serializers.AccountSerializerList(accounts, many=True).data
        return Response(data)

class AccountDetailAPIView(APIView):
    def get(self, request, pk):
        account = models.Account.objects.get(pk=pk)
        data = serializers.AccountSerializerDetail(account).data
        return Response(data)

class AccountCreateAPIView(generics.CreateAPIView):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializerCreate

class AccountUpdateAPIView(APIView):
    def put(self, request, pk):
        account = models.Account.objects.get(pk=pk)
        data = serializers.AccountSerializerUpdate(account, data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data)
        return Response(data.errors, status=400)


class ProviderListAPIView(APIView):
    def get(self, request):
        providers = models.Provider.objects.all()
        data = serializers.ListProviderSerializer(providers, many=True).data
        return Response(data)

class ProviderDetailAPIView(APIView):
    def get(self, request, pk):
        provider = models.Provider.objects.get(pk=pk)
        data = serializers.DetailProviderSerializer(provider).data
        return Response(data)

class ProviderCreateAPIView(generics.CreateAPIView):
    queryset = models.Provider.objects.all()
    serializer_class = serializers.CreateProviderSerializer

class ProviderUpdateAPIView(APIView):
    def put(self, request, pk):
        provider = models.Provider.objects.get(pk=pk)
        data = serializers.UpdateProviderSerializer(provider, data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data)
        return Response(data.errors, status=400)

class ProviderDeleteAPIView(APIView):
    def delete(self, request, pk):
        provider = models.Provider.objects.get(pk=pk)
        provider.delete()
        return Response({"message": "Proveedor eliminado correctamente"})