from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime
# Create your models here.

Passenger_Type = (
	("1", "Adult"),
	("2", "Child"),
	("3", "Infant"),
)

class Passenger(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="passenger_user")
	title = models.CharField(max_length=7, null=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(max_length=100,null=True)
	mobile = models.CharField(max_length=10)
	promo_code = models.CharField(max_length=100, null=True)
	insurance_pdf = models.CharField(max_length=1500, null=True)
	insurance_policy = models.BooleanField(default = True)
	insurance_policy1 = models.BooleanField(default = True)
	passenger_type = models.CharField(max_length=9,choices=Passenger_Type,default="Adult",null=True)
	date_of_birth = models.DateField(null=True)
	src = models.CharField(max_length=100,default=None)
	dest = models.CharField(max_length=100,default=None)
	meal = models.CharField(max_length=100,null=True)
	baggage = models.CharField(max_length=100,null=True)
	seat_no = models.CharField(max_length=100,null=True)
	panno = models.CharField(max_length=10,null=True)
	bookingId = models.CharField(max_length=1000,null=True)
	os_bookingId = models.CharField(max_length=15,null=True)
	passport_no =  models.CharField(max_length=100,null=True)
	airline_name = models.CharField(max_length=100,default=None)
	origin_airport = models.CharField(max_length=100,default=None)
	destination_airport = models.CharField(max_length=100,default=None)
	origin_terminal = models.CharField(max_length=100,default=None, null=True,blank=True)
	destination_terminal = models.CharField(max_length=100,default=None, null=True,blank=True)
	flight_code = models.CharField(max_length=100,default=None)
	flight_number = models.CharField(max_length=100,default=None)
	departure_date = models.DateField(null=True)
	departure_time = models.TimeField(null=True)
	arrival_date = models.DateField(null=True)
	arrival_time =models.TimeField(null=True)
	duration = models.CharField(max_length=100,default=None)
	flight_status = models.CharField(max_length=100,default=None)
	stop = models.BooleanField(default = False)
	pnr = models.CharField(max_length=100,null=True)
	flight_class = models.CharField(max_length=100,default=None)
	base_price = models.FloatField(max_length=100,default=None)
	taf = models.FloatField(max_length=100,default=None)
	meal_charges = models.FloatField(max_length=100, null=True,default=0)
	insurance_charges =models.FloatField(max_length=100,null=True,default=0)
	baggage_charges = models.FloatField(max_length=100,null=True,default=0)
	total_fare = models.FloatField(max_length=100,default=None)
	paid_amount = models.FloatField(max_length=100,default=None)
	gstno = models.CharField(max_length=100,null=True)
	company_name = models.CharField(max_length=100,null=True)
	gst_email = models.CharField(max_length=100,null=True)
	gst_mobile = models.CharField(max_length=100,null=True)
	address = models.CharField(max_length=1000,null=True)
	err_code = models.CharField(max_length=1000,null=True)
	err_desc = models.CharField(max_length=1000,null=True)
	transaction_id = models.CharField(max_length=1000,null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	def __str__(self):
		return str(self.first_name)


class Booking(models.Model):
	payment_id = models.CharField(max_length=100)
	order_id = models.CharField(max_length=100)
	signature = models.CharField(max_length=100)

class Search_History(models.Model):
	origin = models.CharField(max_length=100, null=True)
	destination = models.CharField(max_length=100, null=True)
	journey_date = models.CharField(max_length=100, null=True)
			

class Insurance(models.Model):
	name = models.CharField(max_length=100, null=True)
	mobileno = models.CharField(max_length=100, null=True)
	emailaddress = models.CharField(max_length=100, null=True)
	totalcharges = models.FloatField(max_length=100, null=True)
	arrival_date = models.DateField(null=True)
	departure_date = models.DateField(null=True)
	
	@property
	def reference(self):
		if self.pk:
			return "{}{:05d}".format('SavariInc', self.pk)
		else:
			return ""

class Product(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="product_user")
	bookingId = models.CharField(max_length=15,null=True)
	paymentid = models.CharField(max_length=15,null=True)
    # delivery_email = models.EmailField(max_length=100, null=True, blank=True,)
	delivery_email = models.EmailField(max_length=100,null=True,blank=True)
	phone = models.CharField(max_length=10, null=True, blank=True,)
	amount = models.FloatField(max_length=100,default=None)
	api_amount = models.FloatField(max_length=100,default=None)
	rtype = models.CharField(max_length=10, null=True, blank=True,)
	isBooked = models.BooleanField(default=False)

class Product_traveller(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="product_travel_info")
	title = models.CharField(max_length=7, null=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	passenger_type = models.CharField(max_length=9,choices=Passenger_Type,default="Adult",null=True)
	date_of_birth = models.DateField(null=True)
	passport_no =  models.CharField(max_length=100,null=True)
	passport_ed = models.CharField(max_length=100,null=True)
	passport_issue_date = models.CharField(max_length=100,null=True)

class Ssrbagg(models.Model):
	traveller = models.ForeignKey(Product_traveller, on_delete=models.CASCADE, null=True, related_name="traveller_bag")
	bag_id = models.CharField(max_length=15,null=True)
	bag_code = models.CharField(max_length=10,null=True)

class Ssrmeal(models.Model):
	traveller = models.ForeignKey(Product_traveller, on_delete=models.CASCADE, null=True, related_name="traveller_meal")
	meal_id = models.CharField(max_length=15,null=True)
	meal_code = models.CharField(max_length=10,null=True)
	
class Ssrseat(models.Model):
	traveller = models.ForeignKey(Product_traveller, on_delete=models.CASCADE, null=True, related_name="traveller_seat")
	seat_id = models.CharField(max_length=15,null=True)
	seat_code = models.CharField(max_length=10,null=True)

class gst_info(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="product_gst_info")
	gstno = models.CharField(max_length=100,null=True)
	company_name = models.CharField(max_length=100,null=True)
	gst_email = models.CharField(max_length=100,null=True)
	gst_mobile = models.CharField(max_length=100,null=True)
class ExtraMarkup(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="user_extra")
	agent_id = models.ForeignKey(Passenger, on_delete=models.CASCADE, null=True, related_name="agent_id_markup")
	bookingId = models.ForeignKey(Passenger, on_delete=models.CASCADE, null=True, related_name="bookingId_markup")
	mark_up_value = models.CharField(max_length=100,null=True)
	os_bookingId = models.ForeignKey(Passenger, on_delete=models.CASCADE, null=True, related_name="os_bookingId_markup")

class Akasa_token(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="Akasa_user")
	bookingId = models.CharField(max_length=30,null=True)
	token = models.CharField(max_length=300, null=True)
