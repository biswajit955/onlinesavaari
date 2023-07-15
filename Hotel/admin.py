from django.contrib import admin

from .models import RoomCategory, RoomType, MealBaseType, Address, PropertyType, Room, HotelRegister ,HotelBookingHistory ,TravellerInfo


@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_category_name')


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_type')


@admin.register(MealBaseType)
class MealBaseTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'address_details',
        'city_name',
        'state_name',
        'country_name',
        'pin_code',
    )


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'room_key',
        'room_category',
        'room_type',
        'adults_no',
        'child_no',
        'meal_base_type',
        'current_price',
        'description',
        'pan_card_required',
        'pan_card',
        'passport_required',
        'passport',
        'available',
    )
    list_filter = (
        'room_category',
        'room_type',
        'meal_base_type',
        'pan_card_required',
        'passport_required',
        'available',
    )


@admin.register(HotelRegister)
class HotelRegisterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'hotel_id',
        'hotel_name',
        'hotel_description',
        'hotel_rating',
        'longitude',
        'latitude',
        'Address',
        'phone',
        'property_type',
        'image1',
        'image3',
        'image2',
        'image4',
        'available',
        'created_on',
        'updated_on',
        'created_by',
        'updated_by',
    )
    list_filter = (
        'Address',
        'property_type',
        'available',
        'created_on',
        'updated_on',
        'created_by',
        'updated_by',
    )
    # raw_id_fields = ('room',)

    def get_room(self, obj):
        return "\n".join([p.room_category for p in obj.rooms.all()])


@admin.register(HotelBookingHistory)
class HotelBookingHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'email',
        'mobile',
        'hotel_name',
        'hotel_description',
        'hotel_rating',
        'longitude',
        'latitude',
        'address_details',
        'city_name',
        'state_name',
        'country_name',
        'pin_code',
        'hotel_ph',
        'room_id',
        'room_category',
        'room_type',
        'adults_no',
        'child_no',
        'meal_base',
        'total_price',
        'total_day',
        'check_in_date',
        'created_on',
        'updated_on',
        'created_by',
        'updated_by',
    )
    list_filter = (
        'user',
        'check_in_date',
        'created_on',
        'updated_on',
        'created_by',
        'updated_by',
    )


@admin.register(TravellerInfo)
class TravellerInfoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'hotelBookingHistory',
        'first_name',
        'last_name',
        'type',
        'room_no',
    )
