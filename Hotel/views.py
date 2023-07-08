import json
import random
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
import requests
from datetime import datetime
from django.contrib import messages
import json
from easebuzz_lib.easebuzz_payment_gateway import Easebuzz
import string, random
from decouple import config
from wallet.models import WalletDetails
from adminpanel.models import HotelMarkup
from .models import *
from .utils import *
from flight.views import find_group , percentage

headers={"Content-Type": "application/json",'apikey':config("apikey")}
hotel_listing_api = 'https://apitest.tripjack.com/hms/v1/hotel-searchquery-list'
hotel_details_api = 'https://apitest.tripjack.com/hms/v1/hotelDetail-search'
hotel_review_url = 'https://apitest.tripjack.com/hms/v1/hotel-review'
hotel_cancellation_policy_url = 'https://apitest.tripjack.com/hms/v1/hotel-cancellation-policy'
hotel_booking_details_url = 'https://apitest.tripjack.com/oms/v1/hotel/booking-details'
hotel_booking_url = 'https://apitest.tripjack.com/oms/v1/hotel/book'

# def HotelMarkup(price,grp):
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

class HotelHomeView(View):
    def get(self, request, *args, **kwargs):
        result = request.GET.get('result', None)
        request.session['no_of_rooms'] = result
        return render(request, 'savaari_hotel/index.html')

    def post(self, request, *args, **kwargs):
        data= {}
        grp = find_group(request.user)

        if request.method == 'POST':
            no_of_rooms = request.session.get('no_of_rooms')
            if no_of_rooms is None:
                no_of_rooms = 1
            city_name = request.POST.get('city_name')
            check_in_date = request.POST.get('check_in_date')
            check_in_time = request.POST.get('check_in_time')
            check_out_date = request.POST.get('check_out_date')
            check_out_time = request.POST.get('check_out_time')
            no_of_adultes = request.POST.get('no_of_adulte')
            no_of_childs = request.POST.get('no_of_child')
            no_of_day = datetime.strptime(check_out_date, "%d-%m-%Y")-datetime.strptime(check_in_date, "%d-%m-%Y")
            check_in_date = datetime.strptime(check_in_date, "%d-%m-%Y").strftime('%Y-%m-%d')
            check_out_date = datetime.strptime(check_out_date, "%d-%m-%Y").strftime('%Y-%m-%d')
            print(no_of_adultes)
            if no_of_childs == None:
                no_of_childs = 0

            city_name = city_name.split(',')[0]
            
            
            with open("static/hotel/tripjack_City_hotel_Data2.json") as json_file:
                json_data = json.load(json_file)
                for item in json_data:
                    cityName = item['cityName']
                    if cityName == city_name.upper():
                        city_id = item['id']
            print(city_id)
            # try:
            if Address.objects.filter(city_name = city_name.lower()).exists():
                address_obj = Address.objects.get(city_name = city_name.lower())
                hotel_obj = HotelRegister.objects.filter(Address =address_obj,available=True)
                print(hotel_obj)
                data = []
                for obj in hotel_obj:
                    room = [int(i.current_price) for i in obj.room.all()]
                    data.append({
                        'source':'savaari_data',
                        'id': obj.hotel_id,
                        'img': obj.image1,
                        'name': obj.hotel_name,
                        'rating': obj.hotel_rating,
                        'city_name': obj.Address.city_name,
                        'country_name': obj.Address.country_name,
                        'price': min(room),
                    })
            if data is not None:
                data2 = {'all_data': data}

            if check_in_date >= check_out_date:
                messages.error(request, f"Checkout date can't be prior to checkin date ")
                return render(request, 'savaari_hotel/index.html')
            
            else:
                roomInfo= []
                age_of_child = []
                print(no_of_rooms,"no_of_rooms")
                if no_of_rooms is not None:
                    for room in range(1,int(no_of_rooms)+1):
                        a =request.POST.get(f"no_of_child{room}")
                        if int(a)> 0:
                            for i in range(int(request.POST.get(f"no_of_child{room}"))):
                                age_of_child.append(10)
                            one_roomInfo = {"numberOfAdults": request.POST.get(f"no_of_adulte{room}"),"numberOfChild": request.POST.get(f"no_of_child{room}"),"childAge": age_of_child}
                            roomInfo.append(one_roomInfo)
                            age_of_child = []
                        else:
                            one_roomInfo = {"numberOfAdults": request.POST.get(f"no_of_adulte{room}"),"numberOfChild": request.POST.get(f"no_of_child{room}")}
                            roomInfo.append(one_roomInfo)
                print(roomInfo)

                body= {
                "searchQuery": {
                    "checkinDate": check_in_date,
                    "checkoutDate": check_out_date,
                    "roomInfo": roomInfo,
                    "searchCriteria": {
                        "city": city_id,
                        "nationality": "106",
                        "currency": "INR"
                    },
                    "searchPreferences": {
                        "ratings": [
                            1,
                            2,
                            3,
                            4,
                            5
                        ],
                        "fsc": False
                    }
                },
                "sync": True
                }
                print(body)
                resp = requests.post(url = hotel_listing_api, data=json.dumps(body),headers=headers)
                grp = find_group(request.user)

                if resp.status_code == 200:
                    json_data = resp.json()
                    hotel_data = json_data['searchResult']['his'][0:100]
                    data = {'all_data': []}

                    for i in hotel_data:
                        temp_dict = {}
                        temp_dict['source'] = 'tripjack_data'
                        temp_dict['id'] = i['id']
                        temp_dict['img'] = i['img'][0].get('url', i['img'][0].get('tns')) if 'img' in i else ''
                        temp_dict['name'] = i['name']
                        temp_dict['rating'] = i['rt']
                        markup_data = hotel_markup_filters_for_all_hotel(int(i['pops'][0]['tpc']),grp,i['rt'])
                        print(markup_data)
                        if i['rt'] in markup_data:
                            temp_dict['price'] =  markup_data[i['rt']]
                        else:
                            temp_dict['price'] = i['pops'][0]['tpc'] 
                        temp_dict['city_name'] = i['ad']['ctn']
                        temp_dict['country_name'] = i['ad']['cn']
                        
                        
                        data['all_data'].append(temp_dict)


                    if data2 is not None:
                        data['all_data'].extend(data2['all_data'])

                    return render(request, 'savaari_hotel/hotel-listing.html',context={'data':data,
                                                                                    'no_of_day':no_of_day.days,
                                                                                    'check_in_date':check_in_date,
                                                                                    'check_out_date':check_out_date,
                                                                                    'no_of_adultes':no_of_adultes,
                                                                                    'no_of_child':no_of_childs})
                elif resp.status_code == 400:
                    json_data = resp.json()
                    hotel_data = json_data['errors'][0]['message']
                    messages.error(request, f"{hotel_data}")
                    return render(request, 'savaari_hotel/index.html')
    

class OfferDetails(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'savaari_hotel/offers.html')

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')
    
class HotelListView(View):
    def get(self, request,ids, *args, **kwargs):
        body = {"id": ids}

        resp = requests.post(url = hotel_details_api, data=json.dumps(body),headers=headers)
        data = resp.json()
        with open("one_hotel.json", 'w') as file:
            json.dump({}, file)

        with open("one_hotel.json", "w") as file:
            json.dump(data, file)
        if resp.status_code == 200:
            try:
                des = json.loads(data['hotel']["des"])
                des_keys = [k.upper() for k in des.keys() if k != "attractions" and k != "dining"]
                des_values = [v for k, v in des.items() if k != "attractions"and k != "dining"]
                des_list = zip(des_keys, des_values)
            except:
                des_list =""

            insts = data['hotel']["inst"]
            inst_list = []
            for inst in insts:
                inst_dict = json.loads(inst["msg"])
                inst_dict["type"] = inst["type"]
                inst_list.append(inst_dict)

            a = des['attractions'].split('.  ')
            locations_list = (a[1].split('  '))
            Nearest_Airport = locations_list[-1]


            tripjack_Standard_imgs = []
            for img in data['hotel']['img']:
                try:
                    if img['sz'] == 'Standard':
                        tripjack_Standard_imgs.append(img['url'])
                except:
                    tripjack_Standard_imgs.append(img['url'])
                    
            tripjack_Standard_imgs = [img['url'] for img in data['hotel']['img'] if 'sz' not in img or img['sz'] == 'XL']
                    
            # print(tripjack_Standard_imgs)
            check_in_date = data['searchQuery']['checkinDate']
            check_out_date = data['searchQuery']['checkoutDate']
            # print(check_out_date)
            no_of_day = datetime.strptime(check_out_date, "%Y-%m-%d")-datetime.strptime(check_in_date, "%Y-%m-%d")
            
            grp = find_group(request.user)
            for price in data['hotel']['ops']:
                price['ris'][0]['tp'] = hotel_markup_filter_for_detail_page(price['ris'][0]['tp'],grp,data['hotel']['rt'])
            

            return render(request, 'savaari_hotel/hotel-details.html',context={'data':data,
                                                                           'no_of_day':no_of_day.days,
                                                                           'tripjack_Standard_imgs':tripjack_Standard_imgs,
                                                                           'des_list':des_list,
                                                                           'hotel_des':des,
                                                                           'inst_list':inst_list,
                                                                           'locations_list':locations_list,
                                                                           'Nearest_Airport':Nearest_Airport
                                                                           })       
        else:
            # it's local data base hotel    

            # database_img = []
            # hotel = HotelRegister.objects.get(hotel_id=ids)
            # if hotel.image1:
            #     database_img.append(hotel.image1.url)
            # if hotel.image2:
            #     database_img.append(hotel.image2.url)
            # if hotel.image3:
            #     database_img.append(hotel.image3.url)
            # if hotel.image4:
            #     database_img.append(hotel.image4.url)

            # rooms = [checked_object for checked_object in hotel.room.all()]
            # Price = min([int(i.current_price) for i in hotel.room.all()])
            json_data = resp.json()
            hotel_data = json_data['errors'][0]['message']
            messages.error(request, f"{hotel_data}")
            return render(request, 'savaari_hotel/index.html')
        

    def post(self, request, *args, **kwargs):
        return render(request, 'savaari_hotel/hotel-listing.html')
    
class HotelDetailsView(View):
    def get(self, request,ids,ops_ids, *args, **kwargs):
        print(ops_ids,ids)
        hotel_review_body = {"hotelId": ids,"optionId":ops_ids}
        hotel_cancellation_policy_body = {"id": ids,"optionId":ops_ids}


        hotel_review_resp = requests.post(url = hotel_review_url, data=json.dumps(hotel_review_body),headers=headers)
        hotel_review_data = hotel_review_resp.json()
        if hotel_review_data['status']['httpStatus'] == 200:
            check_in = datetime.strptime(hotel_review_data['query']['checkinDate'], '%Y-%m-%d')
            check_out = datetime.strptime(hotel_review_data['query']['checkoutDate'], '%Y-%m-%d')
            date_diff = check_out.day - check_in.day

            hotel_cancellation_policy_resp = requests.post(url = hotel_cancellation_policy_url, data=json.dumps(hotel_cancellation_policy_body),headers=headers)
            hotel_cancellation_policy_data = hotel_cancellation_policy_resp.json()

            grp = find_group(request.user)

            hotel_review_data['hInfo']['ops'][0]['ris'][0]['tfcs']['BF'] = hotel_markup_filter_one_hotel(hotel_review_data['hInfo']['ops'][0]['ris'][0]['tfcs']['BF'],grp,hotel_review_data['hInfo']['rt'])
            hotel_review_data['hInfo']['ops'][0]['ris'][0]['tp'] = hotel_markup_filter_one_hotel(hotel_review_data['hInfo']['ops'][0]['ris'][0]['tp'],grp,hotel_review_data['hInfo']['rt'])

            total_rs = sum(room['tfcs']['BF'] for room in hotel_review_data['hInfo']['ops'][0]['ris'] if room['tfcs']['BF'])
            total_tax = sum(room['tfcs']['TAF'] for room in hotel_review_data['hInfo']['ops'][0]['ris'] if room['tfcs']['TAF'])
            return render(request, 'savaari_hotel/hotel_payment_review.html',context={'data':hotel_review_data,
                                                                                    "hotel_review_data": json.dumps(hotel_review_data),
                                                                                    'cancellation_data':hotel_cancellation_policy_data,
                                                                                    'check_out':check_out,
                                                                                    'check_in':check_in,
                                                                                    'date_diff':date_diff,
                                                                                    'total_rs':total_rs,
                                                                                    'total_tax':total_tax})
        else:
            messages.error(request, f"Requested Room is no longer available. Please try different option")
            return redirect('hotel_home')

    def post(self, request,ids,ops_ids, *args, **kwargs):
        review_body = {"hotelId": ids,"optionId":ops_ids}

        resp = requests.post(url = hotel_review_url, data=json.dumps(review_body),headers=headers)
        review_data = resp.json()
        travellerInfo =[]
        for num in range(1,len(review_data['hInfo']['ops'][0]['ris'])+1):
            traveller = {"fN": request.POST.get(f'first_name{num}'),"lN": request.POST.get(f'first_name{num}'),"ti": request.POST.get(f'title{num}'),"pt": "ADULT","pan": "ABCDE1234F"}
            travellerInfo.append(traveller)

        email = request.POST.get('email')
        mobile = request.POST.get('mobile')


        booking_body = {
            "bookingId": review_data['bookingId'],
            "roomTravellerInfo": [
                {
                    "travellerInfo":travellerInfo
                }
            ],
            "deliveryInfo": {
                "emails": [
                    email
                ],
                "contacts": [
                    mobile
                ],
                "code": [
                    "+91"
                ]
            },
            "type": "HOTEL",
            "paymentInfos": [
                {
                    "amount": review_data['hInfo']['ops'][0]['tp']
                }
            ]
        }
        request.session['first_name'] = request.POST.get('first_name1')
        request.session['email'] = email
        request.session['mobile'] = mobile
        request.session['review_data'] = review_data
        request.session['booking_body'] = booking_body
        return redirect('hotel_payments')


class HotelPaymentView(View):
    def get(self, request, *args, **kwargs):
        first_name = request.session.get('first_name')
        email = request.session.get('email')
        mobile = request.session.get('mobile')
        review_data = request.session.get('review_data')
        with open("one_hotel.json", 'w') as file:
            json.dump({}, file)

        with open("one_hotel.json", "w") as file:
            json.dump(review_data, file)
        try:
            wallet_balance = (WalletDetails.objects.filter(username=request.user)).latest('id').wallet_balance
        except:
            wallet_balance = 0
        MERCHANT_KEY = "2PBP7IABZ2";
        SALT = "DAH88E3UWQ";
        ENV = "test"

        grp = find_group(request.user)
        review_data['hInfo']['ops'][0]['ris'][0]['tp'] = hotel_markup_filter_one_hotel(review_data['hInfo']['ops'][0]['ris'][0]['tp'],grp,review_data['hInfo']['rt'])

        total_rs = sum(room['tfcs']['BF'] for room in review_data['hInfo']['ops'][0]['ris'] if room['tfcs']['BF'])
        total_tax = sum(room['tfcs']['TAF'] for room in review_data['hInfo']['ops'][0]['ris'] if room['tfcs']['TAF'])

        print(review_data['bookingId'])
        amount1 = review_data['hInfo']['ops'][0]['tp']
        email = email
        mobile = mobile
        bookingId= review_data['hInfo']['id']
        conv_fee = 0
        amount = float(amount1)+float(conv_fee)

        easebuzzObj = Easebuzz(MERCHANT_KEY, SALT, ENV)

        txnid = ''.join(random.choices(string.ascii_uppercase +
                                            string.digits, k = 15))
        pay_hash = '2PBP7IABZ2'+'|'+txnid+'|'+str(amount1)+'|'+'Online Savaari'+'|'+first_name+'|'+email+'|||||||||||'+'DAH88E3UWQ'
        # pay_hash = 'M3YR2SW37O'+'|'+ txnid+'|'+str(amt)+'|'+'Online Savaari'+'|'+first_name+'|'+email+'|||||||||||'+'HHWBRBCYTT'
        hashed_form = encrypt_pay(pay_hash)
        print(hashed_form)
        amount1 = str(amount1)
        easebuzzObj = Easebuzz(MERCHANT_KEY, SALT, ENV)
        postDict = {
            'txnid': txnid,
            'firstname': f'{first_name}',
            'phone': f'{mobile}',
            'email': f'{email}',
            'amount': f'{amount}',
            'productinfo': 'Online Savaari',
            'surl': f'https://onlinesavaari.website/Pay_success/hotel:{txnid}/',
            'furl': f'https://onlinesavaari.website/Pay_failed/{bookingId}/',
            'hash': hashed_form
        }
        final_response = easebuzzObj.initiatePaymentAPI(postDict)
        result = json.loads(final_response)
        print(result)


        return render(request, 'savaari_hotel/hotel-payments.html',context={'data':review_data,
                                                                            "review_data": json.dumps(review_data),
                                                                            "easebuzzjson":json.dumps(result),
                                                                             'email':email,
                                                                             'mobile':mobile,
                                                                             'wallet_balance':wallet_balance,
                                                                             'total_rs':total_rs,
                                                                             'total_tax':total_tax})

    def post(self, request, *args, **kwargs):
        review_data = request.session.get('review_data')
        payment =  request.POST.get('payment')
        booking_body = request.session.get('booking_body')

        booking_Id = review_data['bookingId']
        booking_id_body ={
                            "bookingId":booking_Id
                        }
        resp = requests.post(url = hotel_booking_details_url, data=json.dumps(booking_id_body),headers=headers)

        if resp.status_code == 400:
            resp = requests.post(url = hotel_booking_url, data=json.dumps(booking_body),headers=headers)
            with open("one_hotel.json", 'w') as file:
                json.dump({}, file)

            with open("one_hotel.json", "w") as file:
                json.dump(resp.json(), file)
            if resp.status_code == 200:
                booking_data = resp.json()
                print(booking_data,",,,,,,,,,,,,,,,,,,,,")

                amount = review_data['hInfo']['ops'][0]['tp']
                print(amount)
                wallet = (WalletDetails.objects.filter(username=request.user)).latest('id')
                final =int(wallet.wallet_balance) - int(amount)
                wallet.wallet_balance = final
                wallet.save()

                booking_Id = booking_data['bookingId']
                booking_id_body ={
                                "bookingId":booking_Id
                            }
                resp = requests.post(url = hotel_booking_details_url, data=json.dumps(booking_id_body),headers=headers)
                data= resp.json()

                is_unique = False
                while not is_unique:
                    new_booking_id = generate_random_os_booking_id()
                    if not HotelBookingHistory.objects.filter(osh_bookingId=new_booking_id).exists():
                        is_unique = True


                no_of_day = datetime.strptime(data['itemInfos']['HOTEL']['query']['checkoutDate'], "%Y-%m-%d")-datetime.strptime(data['itemInfos']['HOTEL']['query']['checkinDate'], "%Y-%m-%d")
                HotelBookingHistory.objects.create( user=request.user,
                                                    title = data['itemInfos']['HOTEL']['hInfo']['ops'][0]['ris'][0]['ti'][0]['ti'],
                                                    first_name = data['itemInfos']['HOTEL']['hInfo']['ops'][0]['ris'][0]['ti'][0]['fN'],
                                                    last_name = data['itemInfos']['HOTEL']['hInfo']['ops'][0]['ris'][0]['ti'][0]['lN'],
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
                                                    adults_no = data['itemInfos']['HOTEL']['hInfo']['ops'][0]['ris'][0]['adt'],
                                                    child_no = data['itemInfos']['HOTEL']['hInfo']['ops'][0]['ris'][0]['chd'],
                                                    meal_base = data['itemInfos']['HOTEL']['hInfo']['ops'][0]['ris'][0]['mb'],
                                                    total_price = data['itemInfos']['HOTEL']['hInfo']['ops'][0]['ris'][0]['tp'],
                                                    taxes_fees = data['itemInfos']['HOTEL']['hInfo']['ops'][0]['ris'][0]['tfcs']['TAF'],
                                                    base_price =data['itemInfos']['HOTEL']['hInfo']['ops'][0]['ris'][0]['tfcs']['BF'],
                                                    total_day = no_of_day.days,
                                                    check_in_date = datetime.strptime(data['itemInfos']['HOTEL']['query']['checkinDate'], "%Y-%m-%d"),
                                                    check_out_date = datetime.strptime(data['itemInfos']['HOTEL']['query']['checkoutDate'], "%Y-%m-%d")
                                                )

                return redirect('hotel_booking_history')
            else:
                booking_data = resp.json()
                print(booking_data)
                mgs = booking_data['errors'][0]['message']
                messages.error(request, f"{mgs}")
                return redirect('hotel_home')
        
        else:
            messages.error(request, f"This order is not allready completed")
            return redirect('hotel_home')


class HotelBookingHistoryView(View):
    def get(self, request, *args, **kwargs):
        obj = HotelBookingHistory.objects.filter(user=request.user)
        print(obj)
        return render(request, 'savaari_hotel/booking-history.html',context={'objects':obj})

    def post(self, request, *args, **kwargs):
        return render(request, 'savaari_hotel/booking-history.html')
    

class HotelBookingHistoryDetailsView(View):
    def get(self, request,ids, *args, **kwargs):
        print(ids)
        obj = HotelBookingHistory.objects.get(osh_bookingId=ids)
        print(obj.total_day_night)
        return render(request, 'savaari_hotel/Hotel_booking-invoice.html',context={'objects':obj})

    def post(self, request, *args, **kwargs):
        return render(request, 'savaari_hotel/Hotel_booking-invoice.html')


def hotel_cancel(request):
    if request.method == "POST":
        bookingId1 = request.POST.get("bookingId1")
        print(bookingId1)
    BookingId = request.GET.get('bookingId', "")
    context = {
		'bookingId': BookingId,
	}
    return render(request, "savaari_hotel/cancel.html", context=context)



    