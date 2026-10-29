from rest_framework import serializers

from django.contrib.auth.models import User

from projects import models

### Users serializers

#List
class UserSerializerList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'username',  
            'first_name', 
            'last_name',
            'email'
        ]

#Detail
class UserSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

### Banks serializers

#Create
class BankSerializerCreate():
    pass

'''esta clase es para validar antes de enviar a la BD

'''
class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only = True,
        min_length = 8,
        style ={
            "input_type": "password"
        },
    )
    password_confirm = serializers.CharField(
        write_only = True,
        style ={
            "input_type": "password"
        },
    )
    class Meta:
        model = User
        fields = [
            'id', 
            'username',
            'first_name', 
            'last_name',
            'email',
            'password',
            'password_confirm'
        ]
        #dejamos la coma en readonlyfield en caso de que haga falta agregar otro dato
        read_only_field = ("id",)

#dejamos el metodo de validación fuera de la clase meta

    def validate_email(self, value):
        #necesitamos validar de la BD los usuarios que existen y que sean exactos al valor que estamos validando
        #por lo tanto necesitamos acceder a la BD filtrar y comparar
        if User.objects.filter(username__iexact = value).exists():
            #en caso de encontrar un usuario que ya esté registrado mandamos el error:
            raise serializers.ValidationError("Username ya existe!!, Registrar uno diferente")
        return value

    def validate_user(self,value):
        if value and User.objects.filter(email__iexact = value).exists():
            raise serializers.ValidationError("Email ya existe, registrar uno diferente")
        return value

### este metodo es para validar el password:
### en lugar de pasar el password directamente, pasamos los atributos como método de seguridad
    def validate(self, attrs):
        if attrs["password"]!= attrs["password_confirm"]:
            #el validation error lo regresamos como Json ya que estamos validando un json completo también
            raise serializers.ValidationError({
                "password_confirm": "los passwords no coinciden"
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        return User.objects.create_user(
            username= validated_data["username"],
            email=validated_data.get("email",),
            password= validated_data["password"],
            first_name = validated_data.get("first_name",""),
            last_name = validated_data.get("last_name","")
        )
        
##Retrieve

#List

class BankSerializerList(serializers.ModelSerializer):
    class Meta:
        model = models.Bank
        fields = [
            'id', 
            'name',  
            'status',
        ]

# Create
class BankSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = models.Bank
        fields = [
            'name',
            'address'
        ]

#Detail

class BankSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = models.Bank
        fields = '__all__'

#Update

class BankSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.Bank
        fields = '__all__'

#Delete

class BankSerializerDelete(serializers.ModelSerializer):
    class Meta:
        model = models.Bank
        fields = '_all_'


### Accounts serializers
class AccountSerializerList(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = [
            "name",
            "bank",
            "user",
            "status"
        ]

class AccountSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = [
            "name",
            "bank",
            "user",
            "currency"
        ]

class AccountSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = "__all__"

class AccountSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = "__all__"


"SaaS as a SaaS"


# # DELETE

## PRovider serializers

##PROVIDER CRUD

#CREATE
class CreateProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = [
            "name",
            "address"
        ]

##RETRIEVE

#LIST
class ListProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = [
            "name",
            "status"
        ]

#DETAIL
class DetailProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = "__all__"

#UPDATE

class UpdateProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = "__all__"

#DELETE

class DeleteProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = "__all__"


##PAYMENT SERIALIZERS

###PAYMENT CRUD


##CREATE
class CreatePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = [
            "name",
            "account",
            "user",
            "provider"
        ]

##UPEDATE
class UpdatePaymentSerializer(serializers.ModelSerializer):
        class Meta:
         model = models.Payment
        fields = [
            "name",
            "account",
            "user",
            "provider"
        ]

#LIST
class ListPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = [
            "id",
            "name",
            "account"
        ]

#DETAIL
class DetailPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = "__all__"

#DELETE
class DeletePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = "__all__"