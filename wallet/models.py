from email.policy import default
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
Type = (
    ("Credit", "Credit"),
    ("Debit", "Debit"),
)

class WalletDetails(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="wallet_user")
    email = models.EmailField(max_length=100,null=True)
    amount = models.FloatField(max_length=10, default = 0,null=True, blank=True)
    tds = models.FloatField(max_length=10, default = 0,null=True)
    wallet_balance = models.FloatField(max_length=10, default = 0,null=True)
    is_kyc_done = models.BooleanField(default = True,null=True)
    last_balance_added = models.DateTimeField(auto_now=True)
    wallet_activated_on =models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default = True,null=True)
    trasc_type = models.CharField(max_length=32,null=True)
    transaction_date = models.DateTimeField(auto_now=True,null=True)
    transaction_mode =models.CharField(max_length=32,null=True)
    transaction_status = models.CharField(max_length=32,null=True)
    transaction_id = models.CharField(max_length=32,null=True)
    booking_id  = models.CharField(max_length=32,null=True,blank=True)
    note =models.TextField(max_length=250,null=True)
    def __str__(self):
        return str(self.username)

# Specifying the choices

class Transaction(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="transaction_user")
    email = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="transaction_email")
    amount = models.FloatField(max_length=10, default = 0)
    def __str__(self):
        return str(self.username)

KYCStatus = (
	("NotStarted", "NotStarted"),
	("Pending", "Pending"),
    ("Success", "Success"),
    ("Fail", "Fail"),
    
)
class KYCDetails(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="kyc_user")
    email = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="kyc_email")
    pancard = models.FileField(upload_to="media/kycdocuments", max_length=254,)
    aadharcard = models.FileField(upload_to="media/kycdocuments", max_length=254,)
    photo = models.ImageField(upload_to="media/kycdocuments")
    address =models.TextField(max_length=350)
    kyc_status = models.CharField(max_length=32,choices=KYCStatus)
    def __str__(self):
        return str(self.username)

Reward_Type = (
    ("Promotional", "Promotional"),
    ("Non-Promotional", "Non-Promotional"),    
)

class RewardPoints(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="reward_user")
    reward_points  = models.IntegerField()
    reward_type  = models.CharField(max_length=32,choices=Reward_Type)
    credit_date  = models.DateTimeField(auto_now=True)
    expiry_date  = models.DateTimeField(null=True)
    operation_type  =models.CharField(max_length=32,choices=Type)
    note = models.TextField(max_length=350)
    def __str__(self):
        return str(self.username)
        