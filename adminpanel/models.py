from django.db import models
from django.contrib.auth.models import User
from datetime import date
from onlinesavaari.models import Agent
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Markup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="admin")
    user_type = models.CharField(max_length=100, null=True)
    amount_type = models.CharField(max_length=100, null=True)
    amount = models.CharField(max_length=100, null=True)
    airline_type = models.CharField(max_length=100, null=True)
    markup_type = models.CharField(max_length=100, null=True)

class SeriesMarkup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="series")
    amount_type = models.CharField(max_length=100, null=True)
    amount = models.CharField(max_length=100, null=True)
    airport_name = models.CharField(max_length=100, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
     
class RescheduleFlight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="admin_reschedule")
    Reschedule_bookingid = models.CharField(max_length=100, null=True)
    Reschedule_flight_date = models.CharField(max_length=100, null=True)
    Reschedule_query = models.CharField(max_length=100, null=True)
    Reschedule_status = models.CharField(max_length=100, null=True)

class RefundFlight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="admin_refund")
    Refund_bookingid = models.CharField(max_length=100, null=True)
    Refund_flight_date = models.CharField(max_length=100, null=True)
    Refund_query = models.CharField(max_length=100, null=True)
    Refund_status = models.CharField(max_length=100, null=True)
    Refund_amount = models.FloatField(max_length=100,default=0)
    
class Promocode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="admin_promo")
    promo_code = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    amount = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=1000, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

class Banner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="admin_banner_big")
    big_banner = models.ImageField(upload_to='banner/', null=True)

class SmallBanner1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="admin_banner_small1")
    small_banner1 = models.ImageField(upload_to='banner/', null=True)

class SmallBanner2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="admin_banner_small2")
    small_banner2 = models.ImageField(upload_to='banner/', null=True)
    
class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="admin_data")
    email = models.EmailField(max_length=100,null=True)
    mobile = models.CharField(max_length=10,null=True)
    designation = models.CharField(max_length=100,null=True)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    user_status = models.CharField(max_length=100,null=True)
    @property
    def reference(self):
        if self.pk:
            return "{}{:04d}".format('OSTAFF', self.pk)
        else:
            return ""

class APIbalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="admin_apibalance")
    company_name = models.CharField(max_length=1000, null=True)
    balance = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100,null=True)
    mobile = models.CharField(max_length=10,null=True)

class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="admin_deposit")
    email_or_phone = models.CharField(max_length=100, null=True)
    deposit_type = models.CharField(max_length=100, null=True)
    amount = models.CharField(max_length=100, null=True)
    bank_name = models.CharField(max_length=1000, null=True)
    deposite_branch = models.CharField(max_length=1000, null=True)
    trasaction_num = models.CharField(max_length=100, null=True)
    dep_status = models.CharField(max_length=100, null=True)
    deposit_slip = models.ImageField(upload_to='adminpanel_img/deposit_slip/', null=True)

class Commission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="Commission")
    user_type = models.CharField(max_length=100, null=True)
    amount_type = models.CharField(max_length=100, null=True)
    amount = models.CharField(max_length=100, null=True)
    airline_type = models.TextField(max_length=50000, null=True)
    commission_type = models.CharField(max_length=100, null=True)
    email = models.TextField(max_length=50000, null=True)
    route = models.CharField(max_length=100, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)


class AgentCredit(models.Model):
    agent = models.ForeignKey(Agent,null=True, on_delete=models.CASCADE)
    agent_excepting_airlines = models.CharField(max_length=500)
    amount = models.FloatField(blank=True,null=True,default=0)
    credit_balance = models.FloatField(blank=True,null=True,default=0)
    start_date = models.DateField(blank=True,null=True)
    deduct_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)
    start_time = models.TimeField(blank=True,null=True)
    end_time = models.TimeField(blank=True,null=True)
    hours = models.TimeField(blank=True,null=True)
    due_date = models.DateField(blank=True,null=True)
    status = models.CharField(max_length=100, null=True)
    trasaction_num = models.CharField(max_length=100, null=True)

    # def save(self, *args, **kwargs):
    #     start_date = datetime.strptime(self.start_date, "%Y-%m-%d") 
    #     end_date = datetime.strptime(self.end_date, "%Y-%m-%d") 
    #     day = end_date - start_date
    #     self.hours = (day.days)*24
    #     super(AgentCredit, self).save(*args, **kwargs)
    
    


class Card(models.Model):
    cardholder_name = models.CharField(max_length=100, null=True, blank=True)
    card_number = models.CharField(max_length=20, null=True, blank=True)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=5, null=True, blank=True)
    card_status = models.CharField(max_length=10, null=True, blank=True, default="inactive")
    

class Pcc(models.Model):
    pcc = models.CharField(max_length=100, null=True, blank=True)
    purpose = models.CharField(max_length=10, null=True, blank=True)
    pcc_status = models.CharField(max_length=10, null=True, blank=True, default="inactive")
    