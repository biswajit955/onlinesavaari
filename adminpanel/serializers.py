from rest_framework import serializers
from django.contrib.auth.models import User
from onlinesavaari.models import *
from wallet.models import *
from Hotel.models import *
from adminpanel.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login','password', 'is_superuser')


class UserdataSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserData
		fields = ('__all__')       