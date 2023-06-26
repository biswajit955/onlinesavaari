from django.urls import path,include
from . import views
from .views import *
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView


urlpatterns = [
	path('get_countries/', GetCountriesListAPI.as_view(), name='get_countries'),
	path('get_countries/<int:pk>/', GetCountriesListAPI.as_view(), name='get_countries'),

	path('register_agent/', RegisterAgentAPI.as_view(), name='register_agent'),
	path('register_agent/<int:pk>/', RegisterAgentAPI.as_view(), name='register_agent'),

	path('register_customer/', RegisterCustomerAPI.as_view(), name='register_customer'),
	path('register_customer/<int:pk>/', RegisterCustomerAPI.as_view(), name='register_customer'),

	path('register_corporatecust/', RegisterCorporateCustAPI.as_view(), name='register_corporatecust'),
	path('register_corporatecust/<int:pk>/', RegisterCorporateCustAPI.as_view(), name='register_corporatecust'),

	path('get_hotel/', RegisterHotelAPI.as_view(), name='get_hotel'),
	path('get_hotel/<int:pk>/', RegisterHotelAPI.as_view(), name='get_hotel'),


	path('logout/', User_logout),

    # path('accounts/', include('allauth.urls')),

    path('walletdetails/', WalletDetailsAPI.as_view(), name='walletdetails'),
	path('walletdetails/<int:pk>/', WalletDetailsAPI.as_view(), name='walletdetails'),

	path('transaction/', TransactionAPI.as_view(), name='transaction'),
	path('transaction/<int:pk>/', TransactionAPI.as_view(), name='transaction'),

	path('reward/', RewardPointAPI.as_view(), name='reward'),
	path('reward/<int:pk>/', RewardPointAPI.as_view(), name='reward'),

	path('flight_price/', GetFlightPriceAPI.as_view(), name='flight_price'),
	path('flight_book/', GetFlightBookAPI.as_view(), name='flight_book'),
	path('flight_info/', GetFlightInfoAPI.as_view(), name='flight_info'),
	path('flight_details/', GetFlightDetailsAPI.as_view(), name='flight_details'),
	path('flight_timetable/', GetFlightTTAPI.as_view(), name='flight_timetable'),
	path('flight_fare/', GetFlightFareAPI.as_view(), name='flight_fare'),

	#by biswajit paloi
	path('profilelist-api/', ProfileListApi.as_view(), name='profilelist_api'),
	path('allbookinghistory-api/', AllBookingHistoryAPI.as_view(), name='allbookinghistory_api'),
	path('bookinghistory-api/<str:booking_id>/', BookingHistoryAPI.as_view(), name='bookinghistory_api'),
	path('allairlines-api/', AllAirlinesAPI.as_view(), name='allairlines_api'),
	path('allairports-api/', AllAirportsAPI.as_view(), name='allairports_api'),
	path('allbanners-api/', AllBannersAPI.as_view(), name='allbanners_api'),
	path('allpromocode-api/', AllPromocodeAPI.as_view(), name='allpromocode_api'),


	
]