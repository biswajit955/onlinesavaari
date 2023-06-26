from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Customer
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = User
        fields = ('first_name','last_name','username','email','password',)
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
