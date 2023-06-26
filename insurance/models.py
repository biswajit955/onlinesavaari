from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Insurance_Policy(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="insurance_user")
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    passport_no = models.CharField(max_length=50, blank=True, null=True)
    pnr_no = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=70, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    pin_no = models.CharField(max_length= 10, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(max_length=70, blank=True, null=True)
    amount = models.CharField(max_length= 10, blank=True, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    total_days = models.IntegerField(blank=True, null=True)
    depart_from = models.CharField(max_length=70, blank=True, null=True)
    going_to = models.CharField(max_length= 70, blank=True, null=True)
    category = models.CharField(max_length= 100, blank=True, null=True)
    plan_code = models.CharField(max_length= 100, blank=True, null=True)
    
    pdf_url = models.CharField(max_length=100, blank=True, null=True)
    reference_id = models.CharField(max_length=50, blank=True, null=True)
    policy_no = models.CharField(max_length=20, blank=True, null=True)
    err_code = models.CharField(max_length =20, blank=True, null=True)
    err_desc = models.CharField(max_length= 100, blank=True, null=True)
    insurance_status = models.CharField(max_length= 20, blank=True, null=True)
    
    
    
    
    def __str__(self):
        return str(self.first_name)

