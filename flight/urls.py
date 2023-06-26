from django.urls import path,include
from . import views
from .views import *
from django.views.generic import TemplateView


urlpatterns = [

	path('', TemplateView.as_view(template_name="main.html")),
	path('data', TemplateView.as_view(template_name="data.html")),
	path('select_seat/', views.select_seat, name="select_seat"),
    path('select_gds_seat/', views.select_gds_seat, name="select_gds_seat"),
	path('instant_booking/', views.instant_booking, name="instant_booking"),
	path('get_payment/', views.get_payment, name="get_payment"),
	path('spice_data/', views.spice_data, name="spice_data"),
	path('flight_data/', views.flight_data, name="flight_data"),
	path('search_flight/', views.search_flight, name="search_flight"),
	path('review_flight/', views.review_flight, name="review_flight"),
    path('booking_history/',booking_history,name="booking_history"),
	path('booking_history_api/',BookingHistory.as_view(),name="booking_history_api"),
    path('login_user_booking_history/<int:id>/',login_user_booking_history,name="login_user_booking_history"),
	path('get_details/',views.get_details,name="get_details"),
	path('cancel_booking/',views.cancel_booking,name="cancel_booking"),
	path('get_data/',views.get_data,name="get_data"),
	path('get_insured/',views.get_insured,name="get_insured"),
	path('paymenthandler/',views.get_insured,name="paymenthandler"),
	path('loader/', views.loader_list,name="loader"),
	path('newinvoice/', views.newinvoice,name="newinvoice"),
	path('GeneratePDF/', views.GeneratePDF,name="GeneratePDF"),
	path('newbooking/', views.newbooking, name="newbooking"),
	path('send_ticket_email/', views.send_ticket_email, name="send_ticket_email"),
]





