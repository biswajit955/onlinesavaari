from rest_framework import serializers
from django.contrib.auth.models import User
from onlinesavaari.models import *
from wallet.models import *
from Hotel.models import *
from flight.models import Passenger
from adminpanel.models import *


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login','password')

	
class DocumentsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Documents
		fields = ('__all__')

class AgentSerializer(serializers.ModelSerializer):
	documents = DocumentsSerializer(many=True, read_only=True)
	class Meta:
		model = Agent
		fields = ('__all__')
	
class CustomerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Customer
		fields = ('__all__')
	
class CorporateCustSerializer(serializers.ModelSerializer):
	class Meta:
		model = CorporateCust
		fields = ('__all__')

	
class StateSerializer(serializers.ModelSerializer):
	class Meta:
		model = State
		fields = ('__all__')


class CountrySerializer(serializers.ModelSerializer):
	states = StateSerializer(many=True, read_only=True)

	class Meta:
		model = Country
		fields = ('__all__')

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletDetails
        fields = ('__all__')

	
class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields = ('__all__')

class KYCSerializer(serializers.ModelSerializer):
	class Meta:
		model = KYCDetails
		fields = ('__all__')

class RewardSerializer(serializers.ModelSerializer):
	class Meta:
		model = RewardPoints
		fields = ('__all__')
	
class HotelSerializer(serializers.ModelSerializer):
	class Meta:
		model = HotelRegister
		fields = ('__all__')



class PassengerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Passenger
		fields = ('__all__')
	
class BannerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Banner
		fields = ('id','big_banner',)

class SmallBanner1Serializer(serializers.ModelSerializer):
	class Meta:
		model = SmallBanner1
		fields = ('id','small_banner1',)

class SmallBanner2Serializer(serializers.ModelSerializer):
	class Meta:
		model = SmallBanner2
		fields = ('id','small_banner2',)

class PromocodeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Promocode
		fields = ('__all__')