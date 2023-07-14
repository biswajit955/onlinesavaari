from hashlib import sha512
import string, random
from .models import *
from flight.views import  percentage
from datetime import datetime


def generate_random_os_booking_id():
    os_booking_id = 'OSH' + str(random.randint(100000000, 9999999999))
    return os_booking_id

def encrypt_pay(pay_hash):
    size = 32
    res = bytes(pay_hash, 'utf-8')
    hashed = sha512(res).hexdigest()
    return hashed

def hotel_markup_filters_for_all_hotel(price,grp,rating):
    markup_data = {}
    # for markup in HotelMarkup.objects.all():
    for markup in HotelMarkup.objects.filter(user_type=grp):
        if markup.amount_type == 'fixed' and int(markup.hotel_rating)==int(rating):
            print(int(markup.amount) ,price,'fixed')
            markup_data[int(markup.hotel_rating)] =  int(markup.amount) +price
        elif markup.amount_type == 'percent' and int(markup.hotel_rating)==int(rating):
            markup_data[int(markup.hotel_rating)] = percentage(price,int(markup.amount))
        else:
            markup_data[int(markup.hotel_rating)] = price

    return markup_data

def hotel_markup_filter_for_detail_page(price,grp,rating):
    markup_data = 0
    
    for markup in HotelMarkup.objects.filter(user_type=grp):
        if markup.amount_type == 'fixed' and int(markup.hotel_rating)==int(rating):
            
            markup_data =  int(markup.amount) +price
        elif markup.amount_type == 'percent' and int(markup.hotel_rating)==int(rating):
            
            markup_data =   percentage(price,int(markup.amount))
        else:
            markup_data = price
    if markup_data == 0:
        markup_data = price

    return round(markup_data)


def hotel_markup_filter_one_hotel(price,grp,rating):
    markup_data = 0
    
    for markup in HotelMarkup.objects.filter(user_type=grp):
        if markup.amount_type == 'fixed' and int(markup.hotel_rating)==int(rating):
            
            markup_data =  int(markup.amount) +price
        elif markup.amount_type == 'percent' and int(markup.hotel_rating)==int(rating):
            
            markup_data =   percentage(price,int(markup.amount))
        else:
            markup_data = price
    if markup_data == 0:
        markup_data = price

    return round(markup_data)+00


def save_to_booking_details_database(data,user):
    is_unique = False
    while not is_unique:
        new_booking_id = generate_random_os_booking_id()
        if not HotelBookingHistory.objects.filter(osh_bookingId=new_booking_id).exists():
            is_unique = True
    no_of_adults = 0
    no_of_child = 0
    for count_ris, item in enumerate(data['itemInfos']['HOTEL']['hInfo']['ops'][0]['ris']):
        no_of_adults += item['adt']
        no_of_child += item['chd']

    no_of_day = datetime.strptime(data['itemInfos']['HOTEL']['query']['checkoutDate'], "%Y-%m-%d")-datetime.strptime(data['itemInfos']['HOTEL']['query']['checkinDate'], "%Y-%m-%d")
    booking_hotel = HotelBookingHistory.objects.create( user=user,
                                        email = data['order']['deliveryInfo']['emails'][0],
                                        mobile = data['order']['deliveryInfo']['contacts'][0],
                                        hotel_name = data['itemInfos']['HOTEL']['hInfo']['name'],
                                        hotel_rating = data['itemInfos']['HOTEL']['hInfo']['rt'],
                                        longitude = data['itemInfos']['HOTEL']['hInfo']['gl']['ln'],
                                        latitude =data['itemInfos']['HOTEL']['hInfo']['gl']['lt'],
                                        address_details = data['itemInfos']['HOTEL']['hInfo']['ad']['adr'],
                                        city_name = data['itemInfos']['HOTEL']['hInfo']['ad']['city']['name'],  
                                        state_name = data['itemInfos']['HOTEL']['hInfo']['ad']['state']['name'],
                                        bookingId =  data['order']['bookingId'],
                                        osh_bookingId = new_booking_id,
                                        booking_status =  data['order']['status'],
                                        country_name = data['itemInfos']['HOTEL']['hInfo']['ad']['country']['name'],
                                        pin_code = data['itemInfos']['HOTEL']['hInfo']['ad']['postalCode'],
                                        room_id = data['itemInfos']['HOTEL']['hInfo']['ops'][0]['ris'][0]['id'],
                                        room_category = data['itemInfos']['HOTEL']['hInfo']['ops'][0]['ris'][0]['rc'],
                                        room_type = data['itemInfos']['HOTEL']['hInfo']['ops'][0]['ris'][0]['rt'],
                                        adults_no = no_of_adults,
                                        child_no = no_of_child,
                                        meal_base = data['itemInfos']['HOTEL']['hInfo']['ops'][0]['ris'][0]['mb'],
                                        total_price = data['itemInfos']['HOTEL']['hInfo']['ops'][0]['ris'][0]['tp'],
                                        taxes_fees = data['itemInfos']['HOTEL']['hInfo']['ops'][0]['ris'][0]['tfcs']['TAF'],
                                        base_price =data['itemInfos']['HOTEL']['hInfo']['ops'][0]['ris'][0]['tfcs']['BF'],
                                        total_day = no_of_day.days,
                                        check_in_date = datetime.strptime(data['itemInfos']['HOTEL']['query']['checkinDate'], "%Y-%m-%d"),
                                        check_out_date = datetime.strptime(data['itemInfos']['HOTEL']['query']['checkoutDate'], "%Y-%m-%d")
                                    )
    for count , items in enumerate(data['itemInfos']['HOTEL']['hInfo']['ops'][0]['ris']):
        for item in items['ti']:
            TravellerInfo.objects.create(hotelBookingHistory=booking_hotel,
                                title = item['ti'],
                                first_name = item['fN'],
                                last_name = item['lN'],
                                type= item['pt'],
                                room_no = count+1)