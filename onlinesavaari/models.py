from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100)
    gst_state = models.CharField(max_length=100, null=True, blank=True,)

    def __str__(self):
        return self.name

class PinCodes(models.Model):
    pincode = models.CharField(max_length=50)
    taluk = models.CharField(max_length=50)
    office_name = models.CharField(max_length=100)
    district_name = models.CharField(max_length=100)
    gst_state = models.CharField(max_length=100, null=True, blank=True,)

    def __str__(self):
        return "{0}, {1}, {2}, {3}".format(self.office_name, self.district_name, self.pincode, self.state)

class Documents(models.Model):
    username = models.CharField(max_length=100, null=True)
    doc = models.FileField(upload_to="media/documents/")

class Agent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="agent_user")
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    agent_id = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=10)
    agency_name = models.CharField(max_length=100)

    agency_logo = models.ImageField(upload_to='agent/logo/', null=True, blank=True)

    agency_address = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE , null=True, blank=True)
    gstin = models.CharField(max_length=100, null=True, blank=True)
    gst_state = models.CharField(max_length=100, null=True, blank=True,)
    annual_spent = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to="images/customer/", null=True, blank=True)
    documents = models.ManyToManyField(Documents)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "agent_createdby", null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "agent_updatedby", null=True, blank=True)

    def __str__(self):
        return str(self.user.username)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="customer_user")
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100,)
    mobile = models.CharField(max_length=10)
    address = models.CharField(max_length=250,null=True, blank=True)
    pincode =models.CharField(max_length=6,null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,null=True, blank=True)
    gstin = models.CharField(max_length=100, null=True, blank=True,)
    gst_state = models.CharField(max_length=100, null=True, blank=True,)
    image = models.ImageField(upload_to="images/customer/", null=True, blank=True)
    login_form = models.CharField(max_length=250, default = "EMail" )
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user.username)


class CorporateCust(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="corporate_user")
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=10)
    address = models.CharField(max_length=250,null=True, blank=True)
    pincode =models.CharField(max_length=6,null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,null=True, blank=True)
    gstin = models.CharField(max_length=100, null=True)
    gst_state = models.CharField(max_length=100, null=True, blank=True,)
    annual_spent = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="images/corporate_customer/", null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user.username)