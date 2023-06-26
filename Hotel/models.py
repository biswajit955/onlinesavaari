from django.db import models
from django.contrib.auth.models import User
from onlinesavaari.models import State,Country
from django.core.validators import MaxValueValidator, MinValueValidator


class RoomCategory(models.Model):
    room_category_name = models.CharField(max_length=300)

    def __str__(self):
        return self.room_category_name

    # class Meta:
    #     db_table = ''
    #     managed = True
    #     verbose_name = 'RoomCategory'
    #     verbose_name_plural = 'RoomCategorys'

class RoomType(models.Model):
    room_type = models.CharField(max_length=300)

    def __str__(self):
        return self.room_type

    # class Meta:
    #     db_table = ''
    #     managed = True
    #     verbose_name = 'RoomType'
    #     verbose_name_plural = 'RoomTypes'

class MealBaseType(models.Model):
    name  = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    # class Meta:
    #     db_table = ''
    #     managed = True
    #     verbose_name = 'MealBaseType'
    #     verbose_name_plural = 'MealBaseTypes'


class Address(models.Model):
    address_details = models.CharField(max_length=300)
    city_name = models.CharField(max_length=255)    
    state_name = models.CharField(max_length=255)
    country_name = models.CharField(max_length=255)
    pin_code = models.IntegerField()

    def __str__(self):
        return self.city_name
    
    def save(self, *args, **kwargs):
        self.city_name = self.city_name.lower()
        return super(Address, self).save(*args, **kwargs)

    # class Meta:
    #     db_table = ''
    #     managed = True
    #     verbose_name = 'Address'
    #     verbose_name_plural = 'Addresss'

class PropertyType(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    # class Meta:
    #     db_table = ''
    #     managed = True
    #     verbose_name = 'propertyType'
    #     verbose_name_plural = 'propertyTypes'

class Room(models.Model):
    room_key = models.CharField(max_length=250,help_text="room_id", unique=True)
    room_category = models.ForeignKey(RoomCategory, on_delete=models.SET_NULL,null=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL,null=True)
    adults_no = models.IntegerField()
    child_no = models.IntegerField()
    meal_base_type = models.ForeignKey(MealBaseType, on_delete=models.SET_NULL,null=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=5)
    description = models.TextField(blank=True, null=True)
    pan_card_required = models.BooleanField()
    pan_card = models.FileField(blank=True, null=True)
    passport_required = models.BooleanField()
    passport = models.FileField(blank=True, null=True)
    available = models.BooleanField(default=True)


    def __str__(self):
        return f'Room category={self.room_category}'

    # class Meta:
    #     db_table = ''
    #     managed = True
    #     verbose_name = 'Room'
    #     verbose_name_plural = 'Rooms'

class HotelRegister(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="hotel_user")
    hotel_id = models.CharField(max_length=250,help_text="Hotel_id", unique=True)
    hotel_name = models.CharField(max_length=250)
    hotel_description = models.CharField(max_length=400)
    hotel_rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    longitude = models.DecimalField(max_digits=20, decimal_places=15)
    latitude = models.DecimalField(max_digits=20, decimal_places=15)
    Address = models.ForeignKey(Address, on_delete=models.SET_NULL,null=True)
    phone = models.CharField(max_length=15)
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL,null=True)
    room = models.ManyToManyField(Room, related_name='rooms')
    image1 = models.ImageField(upload_to='hotel/', null=True)
    image3 = models.ImageField(upload_to='hotel/', null=True,blank=True)
    image2 = models.ImageField(upload_to='hotel/', null=True,blank=True)
    image4 = models.ImageField(upload_to='hotel/', null=True,blank=True)

    available = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "hotel_createdby", null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "hotel_updatedby", null=True, blank=True)

    def __str__(self):
        return f'id={self.hotel_id} , name={self.hotel_name}'
        

class HotelBookingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=7, null=True,blank=True)
    first_name = models.CharField(max_length=100,blank=True)
    last_name = models.CharField(max_length=100,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    mobile = models.CharField(max_length=10,null=True,blank=True)
    hotel_name = models.CharField(max_length=250)
    hotel_description = models.CharField(max_length=400,null=True,blank=True)
    hotel_rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    longitude = models.DecimalField(max_digits=20, decimal_places=15,null=True,blank=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=15,null=True,blank=True)
    address_details = models.CharField(max_length=300,null=True,blank=True)
    city_name = models.CharField(max_length=255,null=True,blank=True)    
    state_name = models.CharField(max_length=255,null=True,blank=True)
    bookingId = models.CharField(max_length=50,null=True,blank=True)
    osh_bookingId = models.CharField(max_length=15,null=True,blank=True)
    booking_status = models.CharField(max_length=100,default=None,null=True,blank=True)
    country_name = models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(upload_to='hotel/booking_hotel', null=True,blank=True)
    pin_code = models.IntegerField(null=True,blank=True)
    hotel_ph = models.CharField(max_length=15,null=True,blank=True)
    room_id = models.CharField(max_length=250,help_text="room_id",null=True,blank=True)
    room_category = models.CharField(max_length=250,null=True,blank=True)
    room_type = models.CharField(max_length=250,null=True,blank=True)
    adults_no = models.IntegerField(null=True,blank=True)
    child_no = models.IntegerField(null=True,blank=True)
    meal_base = models.CharField(max_length=250,null=True,blank=True)
    total_price = models.CharField(max_length=250,null=True,blank=True)
    taxes_fees = models.CharField(max_length=250,null=True,blank=True)
    base_price = models.CharField(max_length=250,null=True,blank=True)
    total_day = models.CharField(max_length=250,null=True,blank=True)
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "hotel_booking_history_createdby", null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "hotel_booking_history_updatedby", null=True, blank=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    @property
    def full_address(self):
        return f'{self.address_details},{self.city_name},{self.state_name},{self.pin_code}'
    
    @property
    def roomInfo(self):
        if self.child_no ==0:
            return f'Adults {self.adults_no}'
        else:
            return f'Adults {self.adults_no} & Child {self.child_no}'
        
    @property
    def total_day_night(self):
        night = int(self.total_day) - 1
        return f'{self.total_day} Days & {night} Nights'

    def __str__(self):
        return str(self.osh_bookingId)