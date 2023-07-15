from django.urls import path,include
from .views import *
from django.views.generic import TemplateView


urlpatterns = [
	path('', HotelHomeView.as_view(), name='hotel_home'),
	path('offer-details/', OfferDetails.as_view(), name='offer_details'),
	path('hotel-listing/<str:ids>', HotelListView.as_view(), name='hotel_listing'),
	path('hotel-details/<str:ids>/<str:ops_ids>', HotelDetailsView.as_view(), name='hotel_details'),
    
	path('hotel-payments/', HotelPaymentView.as_view(), name='hotel_payments'),
	path('booking-history/', HotelBookingHistoryView.as_view(), name='hotel_booking_history'),
    
	path('booking-history-details/<str:ids>/', HotelBookingHistoryDetailsView.as_view(), name='hotel_booking_history_details'),
    
	path('hotel-cancel/<str:ids>/', HotelCancel.as_view(), name='hotel_cancel'),
    
	path('hotel_get_data/', hotel_get_data, name='hotel_get_data'),
    
]