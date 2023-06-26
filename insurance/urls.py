from django.urls import path,include
from . import views
from .views import *


urlpatterns = [
	path('', views.insurance_claim, name="insurance_claim"),
	path('insurance_policy/', views.insurance_policy, name="insurance_policy"),
	path('insurance_policy_history/', views.insurance_policy_history, name="insurance_policy_history"),
	path('insurance_payment/', views.insurance_payment, name="insurance_payment"),
	path('insurance_booking/', views.insurance_booking, name="insurance_booking"),
]
