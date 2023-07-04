import json
from pickletools import read_uint1
from time import perf_counter
import requests
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from flight.models import Product
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from onlinesavaari.models import *
import datetime
from datetime import date
from datetime import time ,timedelta
from .models import *
from wallet.models import *
from adminpanel.models import *
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from datetime import datetime as dt
# Create your views here.
from rest_framework import status
import json
import smtplib
from smtplib import SMTPException
from random import randint
import xmltodict
from Crypto.Cipher import AES
import base64
from rest_framework.decorators import api_view
import xml.etree.ElementTree as ET
import razorpay
import string
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import os
from onlinesavaari.models import Agent,Customer,CorporateCust
from django.views.generic import View
from django.template.loader import get_template                
from easebuzz_lib.easebuzz_payment_gateway import Easebuzz
import string, random
from hashlib import sha512
from django.views.decorators.csrf import csrf_exempt
from datetime import date
import xmltodict
import pyqrcode
import png
from pyqrcode import QRCode

from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from rest_framework.generics import ListAPIView
from .serializers import  PassengerSerializer
from rest_framework.permissions import IsAuthenticated

def encrypt_pay(pay_hash):
    size = 32
    res = bytes(pay_hash, 'utf-8')
    hashed = sha512(res).hexdigest()
    return hashed
from django.views.generic import View
from django.template.loader import get_template                



# def get_flight(request):
#     with open("static/flight/FlightSearchResponse.json", "r") as f:
#         data = json.loads(f.read())['Envelope']['Body']['LowFareSearchRsp']['AirSegmentList']['AirSegment']


#     departFrom = request.GET.get('departFrom')
#     departTo = request.GET.get('departTo')
    
#     result = [d for d in data if d['Origin'] == departFrom and d['Destination'] == departTo]
#     adult = request.GET.get('adult')
#     child = request.GET.get('child')
#     infant = request.GET.get('infant')
#     num =[int(adult),int(child),int(infant)]
#     Person = sum(num)
#     context= {
#         "data":result, 
#         "Person":Person, 
#         "departFrom":departFrom,
#         "departTo":departTo,
#         "adult" : adult,
#         "child" : child,
#         "infant" : infant     
#     }
#     return render(request, "online_savaari/listing.html", context)


# def flight_details(request):
    
#     key = request.GET.get('key', None)
#     if key:
#         key = key.replace(" ", "+")

#     with open("static/flight/FlightSearchResponse.json", "r") as f:
#         data = json.loads(f.read())['Envelope']['Body']['LowFareSearchRsp']['AirSegmentList']['AirSegment']

#     result = [d for d in data if d['Key'] == key]
#     price = request.GET.get('amount')
#     # adult = request.POST.get('adult')
#     # child = request.POST.get('child')
#     # infant = request.POST.get('infant')
#     # num =[int(adult),int(child),int(infant)]
#     # Person = sum(num)
   
#     return render(request, "online_savaari/details.html", {"data":result,"price":price})

def percentage(amt, markup):
    return round(amt + amt*(markup/100))


def booking_history(request):
    login_user = request.user

    if not login_user.is_authenticated:
        return JsonResponse({'status':False, 'msg':"User is not logged In!"})

    login_user = request.user

    passengers = Passenger.objects.filter(user=login_user)
    return render(request, "online_savaari/booking-history.html", {'passenger':passengers})

class BookingHistory(ListAPIView):
    # queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        login_user = self.request.user.id
        query = Passenger.objects.filter(user=login_user)
        return query

    def get(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        print( response.data)
        return self.list(request, *args, **kwargs)

def login_user_booking_history(request,id):

    passengers = Passenger.objects.get(id=id)
    return render(request, "online_savaari/login-user-booking-history.html", {'pas':passengers})
    

# def get_payment(request):
#     login_user = request.user

#     if not login_user.is_authenticated:
#         return JsonResponse({'status':False, 'msg':"User is not logged In!"})
        
#     bookingId = request.POST.get('bookingId')
#     cabinClass = request.POST.get('cabinClass')
#     key = request.POST.get('key')
#     Person = request.POST.get('Person')
#     amount = request.POST.get('amount')
#     email=request.POST.get('email', None)
#     origin=request.POST.get('origin', None)
#     mobile=request.POST.get('mobile', None)
#     destination=request.POST.get('destination', None)
#     meal=request.POST.get('meal', None)
#     baggage=request.POST.get('baggage', None)
#     seat_no=request.POST.get('seat_no', None)
#     panno=request.POST.get('panno', None)
#     flightcode=request.POST.get('flightcode', None)
#     flightno=request.POST.get('flightno', None)

#     t = []
#     for i in range(int(Person)):
#         title=request.POST.get(f'title{i + 1}', None)
#         first_name=request.POST.get(f'first_name{i + 1}',None)
#         last_name=request.POST.get(f'last_name{i + 1}',None)
#         pt=request.POST.get(f'pp{i + 1}',None)
#         date_of_birth = request.POST.get(f'date_of_birth{i + 1}', "01-01-1950")
#         passport_no = request.POST.get(f'date_of_birth{i + 1}', None)
#         expiry_date = request.POST.get(f'expiry_date{i + 1}', None)
#         issue_date = request.POST.get(f'issue_date{i + 1}', None)
#         t.append(
#             {
#                 "ti": title,
#                 "fN": first_name,
#                 "lN": last_name,
#                 "pt": pt,
#                 "dob": date_of_birth,
#                 "pNum" :passport_no,
#                 "eD" : expiry_date,
#                 "pid" : issue_date
#             }
#         )

#     # print(t)
        

#     context={
#     "bookingId" : bookingId,
#     "key" : key,
#     "Person" :Person,
#     "amount" :amount,
#     # "title" :title,
#     # "first_name" :first_name,
#     # "last_name" :last_name,
#     "email" :email,
#     "origin" :origin,
#     "mobile" :mobile,
#     "destination" :destination,
#     "meal" :meal,
#     "baggage" :baggage,
#     "seat_no" :seat_no,
#     "panno" :panno,
#     # "passport_no" :passport_no,
#     "flightcode" :flightcode,
#     "flightno" :flightno,
#     "cabinClass" :cabinClass,
#     "trav": t,

#     }
#     # return JsonResponse()
   
#     return render(request, "online_savaari/payments.html", context)
def find_group(user):
    if user.groups.filter(name='Agent').exists():
        return 'Agent'
    elif user.groups.filter(name='Corporate').exists():
        return 'Corporate'
    else:
        return 'Customer'

from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

akasa_url = "https://tbnk-reyalrb.qp.akasaair.com"
def akasa_passenger(akasa_url, akasa_endpoint, akasa_request, akasa_header): 
    akasa_url= akasa_url + akasa_endpoint
    response = requests.put(akasa_url, data=json.dumps(akasa_request), headers=akasa_header)
    print(response)
    return response
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def get_payment(request):
    # return JsonResponse(json.loads(request.POST.get('route').replace("\'", "\"")), safe=False)
    # return JsonResponse(request.POST)

    login_user = request.user
    grp = find_group(request.user)


    if not login_user.is_authenticated:
        return JsonResponse({'status':False, 'msg':"User is not logged In!"})
    if grp ==  'Agent' or grp == 'Corporate':
        MERCHANT_KEY = "2PBP7IABZ2";
        SALT = "DAH88E3UWQ";
        ENV = "test"
    else:
        MERCHANT_KEY = "2PBP7IABZ2";
        SALT = "DAH88E3UWQ";
        ENV = "test"

    # if grp ==  'Agent' or grp == 'Corporate':
    #     MERCHANT_KEY = "2PBP7IABZ2";
    #     SALT = "DAH88E3UWQ";
    #     ENV = "test"
    # else:
    #     MERCHANT_KEY = "2PBP7IABZ2";
    #     SALT = "DAH88E3UWQ";
    #     ENV = "test"
        
    if request.method == 'GET':
        if request.GET.get('ajax') == 'ajax':
            amount1 = request.GET.get('amount') 
            bookingId = request.GET.get("bookingid")
            txnid = ''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k = 15))
            first_name = str(request.user.first_name)
            email = str(request.user)
            pay_hash = MERCHANT_KEY+'|'+ txnid+'|'+str(amount1)+'|'+'Online Savaari'+'|'+'first_name'+'|'+'email@gmail.com'+'|||||||||||'+SALT
            # pay_hash = 'M3YR2SW37O'+'|'+ txnid+'|'+str(amt)+'|'+'Online Savaari'+'|'+first_name+'|'+email+'|||||||||||'+'HHWBRBCYTT'
            hashed_form = encrypt_pay(pay_hash)
            print(hashed_form)
            amount1 = str(amount1)        
            ENV = "test"; 
            email = 'email@gmail.com'
            easebuzzObj = Easebuzz(MERCHANT_KEY, SALT, ENV)
            postDict = {
                'txnid': txnid,
                'firstname': 'first_name',
                'phone': '9873344868',
                'email': 'email@GMAIL.COM',
                'amount': amount1,
                'productinfo': 'Online Savaari',
                'surl': f'https://onlinesavaari.com/Pay_success/{bookingId}/',
                'furl': f'https://onlinesavaari.com/Pay_failed/{bookingId}/',
                'hash': hashed_form
            }

            final_response = easebuzzObj.initiatePaymentAPI(postDict)
            result = json.loads(final_response)
            print(result)
            if result['status'] == 1:
                print("Success")
                print(result)
                if Product.objects.filter(bookingId=bookingId).exists():
                    cust1 = Product.objects.filter(bookingId=bookingId)
                    cust1.paymentid = txnid
                # note: result['data'] - contain payment link. 
                return JsonResponse({'result':result,'key':MERCHANT_KEY})
            else:
                return JsonResponse(result)
                
        if request.GET.get('ajax') == 'payment':         
            ENV = "test"; 
            easebuzzObj = Easebuzz(MERCHANT_KEY, SALT, ENV)
            txnid = request.GET.get('txnid')
            amount1 = request.GET.get('amount')
            amount1 = float(amount1)
            amount1 = str(amount1)
            email = request.GET.get('email')
            postDict = {
            'txnid':txnid,
            'amount':amount1,
            'phone':'9873344868',
            'email':email
            }

            final_response = easebuzzObj.transactionAPI(postDict)
            final_response = json.loads(final_response)

    bookingId = request.POST.get('bookingId')
    src = request.POST.get('src')
    dest = request.POST.get('dest')
    seataddon = request.POST.get('seataddon')
    cabinClass = request.POST.get('cabinClass')
    key = request.POST.get('key')
    insurance_data = request.POST.get('insurance_data')
    amount1 = request.POST.get('amount')
    title=request.POST.get('title', None)
    insurance_checked=request.POST.get('insurance_checked', None)
    bid=request.POST.get('bid', None)
    addon = request.POST.get('addon')
    bagaddon = request.POST.get('bagaddon')
    seat_no=request.POST.get('seat_no', None)
    first_name=request.POST.get('first_name',None)
    last_name=request.POST.get('last_name',None)
    akasa_token=request.POST.get('akasa_token',None)
    passengerkey=request.POST.get('passengerkey',None)
    if passengerkey != None:
        passengerkey = json.loads(passengerkey.replace("\'", "\""))
    route = request.POST.get('route', None)
    if route != None and route != "undefined":
        route = json.loads(route.replace("\'", "\""))
    pp=request.POST.get('pp', None)
    email=request.POST.get('email', None)
    origin=request.POST.get('origin', None)
    mobile=request.POST.get('mobile', None)
    destination=request.POST.get('destination', None)
    meal=request.POST.get('meal', None)
    baggage=request.POST.get('baggage', None)
    seat_no=request.POST.get('seat_no', None)
    panno=request.POST.get('panno', None)
    rtype=request.POST.get('rtype', None)
    passport_no=request.POST.get('passport', None)
    flightcode=request.POST.get('flightcode', None)
    flightno=request.POST.get('flightno', None)
    apiamount=request.POST.get('apiamount', None)
    departure_date=request.POST.get('departure_date', None)
    arrival_date=request.POST.get('arrival_date', None)
    adult=request.POST.get('adult')
    child=request.POST.get('child', None)
    infant=request.POST.get('infant', None)
    token=request.POST.get('token', None)
    ticketid=request.POST.get('ticketid', None)
    Person=request.POST.get('Person', None)
    flight_num=request.POST.get('flight_num', None)
    meal_code=request.POST.get('meal_code', None)
    bagg_code=request.POST.get('bagg_code', None)
    bid = request.POST.get('bid',None)
    gstno = request.POST.get('gstno', None)
    company_name = request.POST.get('company_name', None)
    gst_mobile = request.POST.get('gst_mobile', None)
    gst_email = request.POST.get('gst_email', None)
    address = request.POST.get('address', None)
    spice_token = request.POST.get('spice_token', None)
    print(departure_date,destination,src,dest)
    with open("static/flight/airlines.json", "r") as f:
        airline = json.loads(f.read())

    with open("static/flight/airport_list.json", "r") as f:
        airport = json.loads(f.read())
        l = []
        k = []
        for i in airport:
            if(i['country'] == 'India'):
                air_domestic = i['code']
                l.append(air_domestic)

        for j in airport:
            if(j['country'] != 'India'):
                air_international = j['code']
                k.append(air_international)
    print("ssr", bid, bagg_code,meal_code)
    print(Person)
    amount1 = float(amount1)
    currency = 'INR'
    if rtype == "spicejet":
        spice_token = request.POST.get('spice_token', None)
        spice_request = """<?xml version="1.0" encoding="UTF-8"?> <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"> <s:Header> <h:ContractVersion xmlns:h="http://schemas.navitaire.com/WebServices">420</h:ContractVersion> <h:EnableExceptionStackTrace xmlns:h="http://schemas.navitaire.com/WebServices">false</h:EnableExceptionStackTrace> <h:MessageContractVersion xmlns:h="http://schemas.navitaire.com/WebServices" xmlns:i="http://www.w3.org/2001/XMLSchema-instance" i:nil="true"/> <h:Signature xmlns:h="http://schemas.navitaire.com/WebServices">"""+spice_token+"""</h:Signature> </s:Header> <s:Body> <UpdatePassengersRequest xmlns="http://schemas.navitaire.com/WebServices/ServiceContracts/BookingService"> <updatePassengersRequestData xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns:a="http://schemas.navitaire.com/WebServices/DataContracts/Booking"> <a:Passengers> <a:Passenger> <State xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Common">New</State> <a:PassengerPrograms i:nil="true"/> <a:CustomerNumber i:nil="true"/> <a:PassengerNumber>0</a:PassengerNumber> <a:FamilyNumber>0</a:FamilyNumber> <a:PaxDiscountCode i:nil="true"/> <a:Names> <a:BookingName> <State xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Common">New</State> <a:FirstName>THREE</a:FirstName> <a:MiddleName i:nil="true"/> <a:LastName>TEST</a:LastName> <a:Suffix i:nil="true"/> <a:Title>MR</a:Title> </a:BookingName> </a:Names> <a:Infant i:nil="true"/> <a:PassengerInfo> <State xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Common">New</State> <a:BalanceDue>0</a:BalanceDue> <a:Gender>Male</a:Gender> <a:Nationality i:nil="true"/> <a:ResidentCountry i:nil="true"/> <a:TotalCost>0</a:TotalCost> <a:WeightCategory>Male</a:WeightCategory> </a:PassengerInfo> <a:PassengerProgram i:nil="true"/> <a:PassengerFees i:nil="true"/> <a:PassengerAddresses i:nil="true"/> <a:PassengerTravelDocuments i:nil="true"/> <a:PassengerBags i:nil="true"/> <a:PassengerID>0</a:PassengerID> <a:PassengerTypeInfos> <a:PassengerTypeInfo> <a:State>New</a:State> <a:DOB>0001-01-01T00:00:00</a:DOB> <a:PaxType>ADT</a:PaxType> </a:PassengerTypeInfo> </a:PassengerTypeInfos> <a:PassengerInfos i:nil="true"/> <a:PassengerInfants i:nil="true"/> <a:PseudoPassenger>false</a:PseudoPassenger> <a:PassengerTypeInfo i:nil="true"/> <a:PassengerEMDCouponList i:nil="true"/> </a:Passenger> </a:Passengers> <a:WaiveNameChangeFee>false</a:WaiveNameChangeFee> </updatePassengersRequestData> </UpdatePassengersRequest> </s:Body> </s:Envelope>"""
        update_pax = spice_data(spice_url,'/Bookingmanager.svc',spice_request,spice_header={"Content-Type":"text/xml; charset=utf-8", "SOAPAction":"http://schemas.navitaire.com/WebServices/IBookingManager/UpdatePassengers","Accept-Encoding":"gzip, deflate"})  
        with open("update_pax.txt", "w") as file:
            file.write(str(update_pax))
            file.close()
        update_pax = xmltodict.parse(update_pax, attr_prefix='')
        update_pax = json.dumps(update_pax)
        update_pax = json.loads(update_pax)
        due_amount = update_pax['s:Envelope']['s:Body']['UpdatePassengerResponse']['BookingUpdateResponseData']['Success']['PNRAmount']['BalanceDue']
        with open("inp_update_pax.txt", "w") as file:
            file.write(str(spice_request))
            file.close()

        spice_request = """<?xml version="1.0" encoding="UTF-8"?> <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"> <s:Header> <h:ContractVersion xmlns:h="http://schemas.navitaire.com/WebServices">420</h:ContractVersion> <h:EnableExceptionStackTrace xmlns:h="http://schemas.navitaire.com/WebServices">false</h:EnableExceptionStackTrace> <h:MessageContractVersion xmlns:h="http://schemas.navitaire.com/WebServices" xmlns:i="http://www.w3.org/2001/XMLSchema-instance" i:nil="true"/> <h:Signature xmlns:h="http://schemas.navitaire.com/WebServices">"""+spice_token+"""</h:Signature> </s:Header> <s:Body> <AddPaymentToBookingRequest xmlns="http://schemas.navitaire.com/WebServices/ServiceContracts/BookingService"> <addPaymentToBookingReqData xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Booking"> <MessageState>New</MessageState> <WaiveFee>false</WaiveFee> <ReferenceType>Default</ReferenceType> <PaymentMethodType>AgencyAccount</PaymentMethodType> <PaymentMethodCode>AG</PaymentMethodCode> <QuotedCurrencyCode>INR</QuotedCurrencyCode> <QuotedAmount>"""+apiamount+"""</QuotedAmount> <Status>New</Status> <AccountNumberID>0</AccountNumberID> <AccountNumber>APITESTID</AccountNumber> <Expiration>0001-01-01T00:00:00</Expiration> <ParentPaymentID>0</ParentPaymentID> <Installments>0</Installments> <PaymentText i:nil="true"/> <Deposit>false</Deposit> <PaymentFields i:nil="true"/> <PaymentAddresses i:nil="true"/> <AgencyAccount i:nil="true"/> <CreditShell i:nil="true"/> <CreditFile i:nil="true"/> <PaymentVoucher i:nil="true"/> <ThreeDSecureRequest i:nil="true"/> <MCCRequest i:nil="true"/> <AuthorizationCode i:nil="true"/> </addPaymentToBookingReqData> </AddPaymentToBookingRequest> </s:Body> </s:Envelope>"""
        spice_payment = spice_data(spice_url,'/Bookingmanager.svc',spice_request,spice_header={"Content-Type":"text/xml; charset=utf-8", "SOAPAction":"http://schemas.navitaire.com/WebServices/IBookingManager/AddPaymentToBooking","Accept-Encoding":"gzip, deflate"})  
        with open("update_pay.txt", "w") as file:
            file.write(str(spice_payment))
            file.close()
        spice_payment = xmltodict.parse(spice_payment, attr_prefix='')
        spice_payment = json.dumps(spice_payment)
        spice_payment = json.loads(spice_payment)
        with open("inp_update_pay.txt", "w") as file:
            file.write(str(spice_request))
            file.close()
    if(rtype == "akasa"):
        addon = json.loads(request.POST.get('addon').replace("\'", "\""))
        bagg = json.loads(request.POST.get('bagaddon').replace("\'", "\""))
        val = []
        for i, v in addon.items():
            for a in v['unitkey'].values():
                val.append(a['ssrKey'])
        for i, v in bagg.items():
            for a in v['unitkey'].values():
                val.append(a['ssrKey'])
        res = []
        null = None
        print(akasa_token,first_name,last_name,title)
        ak_pax = 0
        for x in passengerkey:
            ak_pax += 1
            if ak_pax == 1:
                akasa_request ={
                    "name": {
                        "first": first_name,
                        "middle": null,
                        "last": last_name,
                        "title": title,
                        "suffix": null
                    },
                    "info": {
                        "nationality": null,
                        "residentCountry": null,
                        "gender": null,
                        "dateOfBirth": null
                    }
                }
            else:
                title_sr = {
                    "Master": "Mr",
                    "Miss": "Ms",
                    "Mr": "Mr",
                    "Mrs": "Mrs",
                    "Ms": "Ms",
                    None: "Mr",
                }
                akasa_request ={
                    "name": {
                        "first": request.POST.get(f'first_name{ak_pax}', None),
                        "middle": null,
                        "last": request.POST.get(f'last_name{ak_pax}', None),
                        "title": title_sr[request.POST.get(f'title{ak_pax}', None)],
                        "suffix": null
                    },
                    "info": {
                        "nationality": null,
                        "residentCountry": null,
                        "gender": null,
                        "dateOfBirth": null
                    }
                }
            # res.append(akasa_request)
        # return JsonResponse(res, safe=False)
            akasa_endpoint = '/api/nsk/v3/booking/passengers/'+ x
            akasa_token1 = 'Bearer '+ akasa_token
            akasaa_data = akasa_passenger(akasa_url, akasa_endpoint, akasa_request,akasa_header={"Authorization":akasa_token1})
            res.append(akasaa_data.json())
            for i in val:
                ssr_endpoint = '/api/nsk/v2/booking/ssrs/' + i
                akasa_ssr = {"count":1,"note":"Pax","forceWaveOnSell":'false',"currencyCode":"INR","ssrSellMode":0}
                akasa_req_srr = akasa_data(akasa_url, ssr_endpoint, akasa_ssr,akasa_header={"Authorization":akasa_token})
            # JsonResponse(akasaa_data, safe=False)
            akasa_request ={"paymentMethodCode":"AG","amount":apiamount,"paymentFields":{"ACCTNO":"QPBOM6061B","AMT":apiamount},"currencyCode":"INR","installments":1}

            akasaa_pay = akasa_data(akasa_url, '/api/nsk/v2/booking/payments', akasa_request,akasa_header={"Authorization":akasa_token})

        # return JsonResponse(res, safe=False)

    # res = ''.join(random.choices(string.ascii_uppercase +
    #                          string.digits, k = 15))
    

    
    # client = razorpay.Client(auth=("rzp_test_cbUIs2vrl3R0RD", "Mmj071WgNxhb2W8lToZ2frRT"))

    # rzordata = { "amount": ramount, "currency": "INR", "receipt": res }
    # payment = client.order.create(data=rzordata)
    checkid = ''
    if bookingId:
        checkid = bookingId
    elif ticketid:
        checkid = ticketid

    prevamount = None
    conv_fee = None
    if(arrival_date):
        arrival_date = arrival_date.strip()
        departure_date = departure_date.strip()
    grp = find_group(request.user)
    amount = float(amount1)
    if((src in l) and (dest in l)):
        print("locla")
        dest = dest.strip()
        if(grp == 'Customer'):
            conv_fee = 300 * int(Person)
        elif(grp == 'Agent'):
            conv_fee = 0 
        else:
            conv_fee = 150 * int(Person)
        prevamount= amount1
        print(prevamount)
        amount = float(amount1)+float(conv_fee)
    if((src in k) or (dest in k)):
        print("international")
        dest = dest.strip()
        if(grp == 'Customer'):
            conv_fee = 900 * int(Person)
        elif(grp == 'Agent'):
            conv_fee = 0
        else:
            conv_fee = 450 * int(Person)
        prevamount= amount1
        amount = float(amount1)+float(conv_fee)
    
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
        'surl': f'http://35.200.223.78/Pay_success/{checkid}/',
        'furl': f'http://35.200.223.78/Pay_failed/{bookingId}/',
        'hash': hashed_form
    }

    final_response = easebuzzObj.initiatePaymentAPI(postDict)
    result = json.loads(final_response)
    print(result)
    # if result['status'] == 1:
    #     print("Success")
    #     print(result)
    #     # note: result['data'] - contain payment link. 
    #     return JsonResponse(result)
    # else:
    #     return render(request, 'online_savaari/response.html', {'response_data': final_response})
    if Product.objects.filter(bookingId=checkid).exists():
        cust1 = Product.objects.filter(bookingId=checkid)
        cust1.paymentid = txnid
    else:
        cust1=Product.objects.create(user=request.user,bookingId=checkid,paymentid=txnid,delivery_email=email,phone=mobile,amount=amount,api_amount=apiamount,rtype=rtype)
        for i in range(int(Person)):
            if i>0:
                pd_title = request.POST.get(f'title{i+1}', None)
                pd_first_name = request.POST.get(f'first_name{i+1}', None)
                pd_last_name = request.POST.get(f'last_name{i+1}', None)
                pd_pt = request.POST.get(f'pp{i+1}', None)
                pd_passport =request.POST.get(f'passport{i+1}', None)
                pd_seat =request.POST.get(f'seat_no{i+1}', None)
                if(request.POST.get(f'pp{i+1}') == 'INFANT'):
                    pd_dob =request.POST.get(f'dob{i+1}', None)
                    pd_cust = Product_traveller.objects.create(product=cust1,title=pd_title,first_name=pd_first_name,last_name=pd_last_name,passenger_type=pd_pt,passport_no=pd_passport,date_of_birth=pd_dob)
                pd_cust = Product_traveller.objects.create(product=cust1,title=pd_title,first_name=pd_first_name,last_name=pd_last_name,passenger_type=pd_pt,passport_no=pd_passport)
                seat_cust = Ssrseat(traveller=pd_cust,seat_code=pd_seat)
            else:
                pd_cust = Product_traveller.objects.create(product=cust1,title=title,first_name=first_name,last_name=last_name,passenger_type=pp,passport_no=passport_no)
                seat_cust = Ssrseat(traveller=pd_cust,seat_code=seat_no)
        # if route and route != "undefined":
        #     for i in route:
        #         src = i['da']['code']
        #         dest = i['aa']['code']
        #         airline_name = i['airdetails']['aI']['name']
        #         flight_code = i['airdetails']['aI']['code']
        #         flight_number = i['airdetails']['fN']
        #         departure_date = i['dt'].split("T")[0]
        #         departure_time = i['dt'].split("T")[1]
        #         arrival_date = i['at'].split("T")[0]
        #         arrival_time = i['at'].split("T")[1]
        #         route_cust = Product_route.objects.create(product=cust1,src=src,dest=dest,airline_name=airline_name,flight_code=flight_code,flight_number=flight_number,departure_date=departure_date,departure_time=departure_time,arrival_date=arrival_date,arrival_time=arrival_time)

    print(departure_date,arrival_date)
    context={
    "easebuzzjson":json.dumps(result),
    "razorpay_amount" : amount1,
    "gstno" : gstno,
    "company_name" : company_name,
    "gst_email" : gst_email,
    "gst_mobile" : gst_mobile,
    "address" : address,
    "bookingId" : bookingId,
    "apiamount" : apiamount,
    "key" : key,
    "Person" :Person,
    "amount" :amount,
    "title1" :title,
    "first_name1" :first_name,
    "last_name1" :last_name,
    "pp1": pp,
    "email" :email,
    "prevamount" :prevamount,
    "src" :src,
    "dest" :dest,
    "origin" :origin,
    "mobile" :mobile,
    "bid" :bid,
    "destination" :destination,
    "meal" :meal,
    "baggage" :baggage,
    "bid" :bid,
    "seat_no" :seat_no,
    "meal_code" :meal_code,
    "bagg_code" :bagg_code,
    "panno" :panno,
    "passport_no" :passport_no,
    "flightcode" :flightcode,
    "flightno" :flightno,
    "cabinClass" :cabinClass,
    "conv_fee" :conv_fee,
    "departure_date" :departure_date,
    "arrival_date" :arrival_date,
    "flight_num" :flight_num,
    "adult" :adult,
    "child" :child,
    "infant" :infant,
    "token" :token,
    "ticketid" :ticketid,
    "rtype" :rtype,
    "akasa_token" :akasa_token,
    "insurance_checked" :insurance_checked,
    "addon":addon,
    "bagaddon":bagaddon,
    "insurance_data":insurance_data,
    "seataddon": seataddon,
    "spice_token": spice_token,
    "addPerson": {},
    }

    for i in range(int(Person)):
        if i>0:
            context['addPerson'][f'title{i+1}'] = request.POST.get(f'title{i+1}', None)
            context['addPerson'][f'first_name{i+1}'] = request.POST.get(f'first_name{i+1}', None)
            context['addPerson'][f'last_name{i+1}'] = request.POST.get(f'last_name{i+1}', None)
            context['addPerson'][f'pp{i+1}'] = request.POST.get(f'pp{i+1}', None)
            context['addPerson'][f'passport_no{i+1}'] =request.POST.get(f'passport{i+1}', None)
            context['addPerson'][f'seat_no{i+1}'] =request.POST.get(f'seat_no{i+1}', None)
            if(request.POST.get(f'pp{i+1}') == 'INFANT'):
                context['addPerson'][f'dob{i+1}'] =request.POST.get(f'dob{i+1}', None)
   
    return render(request, "online_savaari/payments.html", context)

     
def encrypt(xml_policy):
    key = b'e663ecc7-7e40-4eec-a2be-56d95272'
    iv = b'5e74074a-91d4-45'
    xml_policy = _pad(xml_policy)
    cipher = AES.new(key, AES.MODE_CBC,iv)
    encode_data1 = base64.b64encode(cipher.encrypt(xml_policy.encode("ascii")))
    encode_data=encode_data1.decode("ascii")
    return encode_data


def _pad(s):
    return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)

import xml.etree.ElementTree as ET
url_inc = 'https://asegotravel.in/trawelltag/v2/CreatePolicy.aspx'
Ref = '5e74074a-91d4-45ee-bfdc-1299585584f3'

def insurance(url_inc,data,Ref,headers=None):
    res = 'data='+data+'&ref='+Ref
    response = requests.post(url_inc,data={'data':data,'ref':Ref})
    return response

@api_view(["GET","POST"])
def get_insured(request):
    insurance_checked=request.POST.get('insurance_checked', None)
    with open("flight/insurance.xml") as xml_file:
        xml_policy = xml_file.read() 
    data = encrypt(xml_policy)
    result = insurance(url_inc,data,Ref)
    result = result.text
    return HttpResponse(result)

api_key= "NTMzNDUwMDpBSVJJUSBURVNUIEFQSToxODkxOTMwMDM1OTk2OlFRYjhLVjNFMW9UV05RY1NWL0VtcnNnb3dGV0o3SzJ1cVptbzJ1bFp1cEE9"
series_url='https://omairiq.azurewebsites.net'
def series_data(series_url, seriesendpoint, search_series,header): 
    seriesurl= series_url + seriesendpoint
    response = requests.post(seriesurl, data=json.dumps(search_series), headers=header)
    return response

akasa_url = "https://tbnk-reyalrb.qp.akasaair.com"
def akasa_data(akasa_url, akasa_endpoint, akasa_request, akasa_header): 
    akasa_url= akasa_url + akasa_endpoint
    response = requests.post(akasa_url, data=json.dumps(akasa_request), headers=akasa_header)
    return response

def akasa_seat(akasa_url, akasa_endpoint, akasa_header): 
    akasa_url= akasa_url + akasa_endpoint
    response = requests.get(akasa_url, headers=akasa_header)
    return response
def akasa_details(akasa_url, akasa_endpoint, akasa_request, akasa_header): 
    akasa_url= akasa_url + akasa_endpoint
    response = requests.get(akasa_url, data=json.dumps(akasa_request), headers=akasa_header)
    return response

spice_url = "https://sgtestr4xapi.navitaire.com"

def spice_data(spice_url, spice_endpoint, spice_request, spice_header):
    
    print(spice_url + spice_endpoint)
    spice_url_new = spice_url + spice_endpoint
    response = requests.post(spice_url_new, data=spice_request, headers=spice_header).text
    return response

apikey= "2120183a3d1670-91ac-4f08-8026-db803a04fbdc"
api_url='https://apitest.tripjack.com/'
headers={"apikey":apikey, "Content-Type":"application/json"}

def flight_data(baseurl, apikey, endpoint, search_request): 
    url= api_url + endpoint
    response = requests.post(url, data=json.dumps(search_request), headers=headers)
    return response
    
def find_group(user):
    if user.groups.filter(name='Agent').exists():
        return 'Agent'
    elif user.groups.filter(name='Corporate').exists():
        return 'Corporate'
    else:
        return 'Customer'

def editmarkup(data, all_markup, all_airline_type):
    for key, onwards in data["searchResult"]["tripInfos"].items():
        for amt in all_markup:
            fix_air_air = amt["airline_type"]
            markup_amount = amt["amount"]
            onwards_temp = []
            for x in data["searchResult"]["tripInfos"][key]:
                for y in x['sI']:
                    flightname= y['fD']['aI']['name']
                    if fix_air_air:
                        add = True
                        if (flightname == fix_air_air):
                            for p in x["totalPriceList"]:
                                tf = p["fd"]["ADULT"]["fC"]["TF"]
                                taf = p["fd"]["ADULT"]["fC"]["TAF"]
                                if amt["amount_type"] == 'fixed':
                                    tf= round(float(tf) + float(markup_amount), 1)
                                    p["fd"]["ADULT"]["fC"]["TF"] = tf
                                    p["fd"]["ADULT"]["fC"]["TAF"] = taf + float(markup_amount)
                                if amt["amount_type"] == 'percent':
                                    newtf = percentage(float(tf), float(markup_amount))
                                    p["fd"]["ADULT"]["fC"]["TF"] = newtf
                                    p["fd"]["ADULT"]["fC"]["TAF"] = taf + newtf - tf
                        break
                    else:
                        add = True
                        if (flightname not in all_airline_type):
                            for p in x["totalPriceList"]:
                                tf = p["fd"]["ADULT"]["fC"]["TF"]
                                taf = p["fd"]["ADULT"]["fC"]["TAF"]
                                if amt["amount_type"] == 'fixed':
                                    tf= float(tf) + float(markup_amount)
                                    p["fd"]["ADULT"]["fC"]["TF"] = tf
                                    p["fd"]["ADULT"]["fC"]["TAF"] = taf + float(markup_amount)
                                if amt["amount_type"] == 'percent':
                                    newtf = percentage(float(tf), float(markup_amount))
                                    p["fd"]["ADULT"]["fC"]["TF"] = newtf
                                    p["fd"]["ADULT"]["fC"]["TAF"] = taf + newtf - tf
                        break
                                    
                onwards_temp.append(x)
            data["searchResult"]["tripInfos"][key] = onwards_temp
    return data

def encrypt_gds(gds_request):
    CREDENTIALS = 'Universal API/uAPI4848615841-06cd9b7b:k*6FHz/29M'
    message_bytes = CREDENTIALS.encode('ascii')
    auth = base64.b64encode(message_bytes)
    auth = 'Basic ' + auth.decode('utf-8')
    headers = {"Authorization": auth, "Content-Type":"text/xml;charset=UTF-8"}
    gds_url= "https://apac.universal-api.pp.travelport.com/B2BGateway/connect/uAPI/AirService"
    response = requests.post(gds_url, data=gds_request, headers=headers).text
    print(requests.post(gds_url, data=gds_request, headers=headers).status_code)
    return response

def remove_air(data, airlist):
    onwards_temp = []
    for val in data["searchResult"]["tripInfos"]['ONWARD']:
        for y in val['sI']:
            flightname= y['fD']['aI']['name']
            if flightname not in airlist:
                onwards_temp.append(val)
                break
    data["searchResult"]["tripInfos"]['ONWARD'] = onwards_temp
    return data

@api_view(["GET"])
def loader_list(request):
    radio1 = request.GET.get('radio1', None)
    token = request.GET.get('token', None)
    akasa_token = request.GET.get('akasa_token', None)
    spice_token = request.GET.get('spice_token', None)
    print(token)
    fromCityOrAirport = request.GET.get('fromCityOrAirport', None)
    toCityOrAirport = request.GET.get('toCityOrAirport', None)
    fromCityOrAirport1 = request.GET.get('fromCityOrAirport1')
    toCityOrAirport1 = request.GET.get('toCityOrAirport1')
    fromCityOrAirport2 = request.GET.get('fromCityOrAirport2')
    toCityOrAirport2 = request.GET.get('toCityOrAirport2')
    fromCityOrAirport3 = request.GET.get('fromCityOrAirport3')
    toCityOrAirport3 = request.GET.get('toCityOrAirport3')
    fromCityOrAirport4 = request.GET.get('fromCityOrAirport4')
    toCityOrAirport4 = request.GET.get('toCityOrAirport4')
    toCityOrAirport5 = request.GET.get('toCityOrAirport5')
    adult = request.GET.get('ADULT', None)
    adult = int(adult)
    child = request.GET.get('CHILD', None)
    child = int(child)
    infant = request.GET.get('INFANT', None)
    infant = int(infant)
    cabinClass = request.GET.get('cabinClass')
    isDirectFlight = request.GET.get('isDirectFlight')
    travelDate = request.GET.get('travelDate', None)
    travelDate1 = request.GET.get('travelDate1')
    travel1Date = request.GET.get('travel1Date')
    travel2Date = request.GET.get('travel2Date')
    travel3Date = request.GET.get('travel3Date')
    travel4Date = request.GET.get('travel4Date')
    travel5Date = request.GET.get('travel5Date')
    Special = request.GET.get('Special')
    start_price = request.GET.get('start_price')
    end_price = request.GET.get('end_price')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    print(travelDate)
    conv = travelDate.split("-")
    dd= int(conv[0])
    mm = int(conv[1])
    yy= int(conv[2])
    if travelDate != None :
        cust1=Search_History.objects.create(origin=fromCityOrAirport,destination=toCityOrAirport,journey_date=travelDate)
    
    
    travelDateseries = date(yy,mm,dd)
    travelDate_akasa= travelDateseries.strftime("%Y-%m-%d")
    travelDateseries = travelDateseries.strftime("%Y/%m/%d")
    num =[int(adult),int(child),int(infant)]
    Person = sum(num)
    print("Person",Person)
    # akasaa_data = None
    if (radio1 == "one-way"):
        search_series = {
            "origin":fromCityOrAirport,
            "destination":toCityOrAirport,
            "departure_date":travelDateseries,
            "adult":adult,
            "child":child,
            "infant":infant,
            "airline_code":""
        }
        seriess_data = series_data(series_url, '/search',search_series,header={"api-key":api_key,"Authorization":token, "Content-Type":"application/json"})
        search_sdata=seriess_data.json()
        print("search_sdata",search_sdata)
        reflist = []
        gds_ref = {}
        gds_ref['ADT'] = []
        for adt in range(adult):
            gds_ref['ADT'].append('OS' + str(randint(1000000000, 9999999999)))
        if child != 0:
            gds_ref["CNN"] = []
            for adt in range(child):
                gds_ref['CNN'].append('OS' + str(randint(1000000000, 9999999999)))
        if infant != 0:
            gds_ref["INF"] = []
            for adt in range(infant):
                gds_ref['INF'].append('OS' + str(randint(1000000000, 9999999999)))
        reflist = [f'<com:SearchPassenger Code="{ky}" BookingTravelerRef="{v}"/>' 
           for ky, val in gds_ref.items() for v in val]
        # """<com:SearchPassenger Code="ADT" BookingTravelerRef="OS0000000001"/>
        # <com:SearchPassenger Code="INF" BookingTravelerRef="OS0000000002" Age="1" PricePTCOnly="true"/>
        # <com:SearchPassenger Code="CNN" BookingTravelerRef="OS0000000003" Age="10"/>"""
        gds_request = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"> <soapenv:Header/> <soapenv:Body> <air:LowFareSearchReq TraceId="trace" AuthorizedBy="user" SolutionResult="true" TargetBranch="P7189273" xmlns:air="http://www.travelport.com/schema/air_v51_0" xmlns:com="http://www.travelport.com/schema/common_v51_0"> <com:BillingPointOfSaleInfo OriginApplication="UAPI"/> <air:SearchAirLeg> <air:SearchOrigin> <com:Airport Code="""+"'"+fromCityOrAirport+"'"+"""/> </air:SearchOrigin> <air:SearchDestination> <com:Airport Code="""+"'"+toCityOrAirport+"'"+"""/> </air:SearchDestination> <air:SearchDepTime PreferredTime="""+"'"+travelDate_akasa+"'"+"""> </air:SearchDepTime> </air:SearchAirLeg> <air:AirSearchModifiers> <air:PreferredProviders> <com:Provider Code="1G"/> </air:PreferredProviders> </air:AirSearchModifiers>"""+''.join(reflist)+"""</air:LowFareSearchReq> </soapenv:Body> </soapenv:Envelope>"""
        gds_data = encrypt_gds(gds_request)
        gds_data = xmltodict.parse(gds_data, attr_prefix='')  
        gds_data = json.dumps(gds_data)
        # return Response(gds_ref)

        # spice_request="""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"> <s:Header> <h:ContractVersion xmlns:h="http://schemas.navitaire.com/WebServices">420</h:ContractVersion> <h:EnableExceptionStackTrace xmlns:h="http://schemas.navitaire.com/WebServices">false</h:EnableExceptionStackTrace> </s:Header> <s:Body> <LogonRequest xmlns="http://schemas.navitaire.com/WebServices/ServiceContracts/SessionService"> <logonRequestData xmlns:a="http://schemas.navitaire.com/WebServices/DataContracts/Session" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"> <a:DomainCode>WWW</a:DomainCode> <a:AgentName>APITESTID</a:AgentName> <a:Password>Spice@123</a:Password> <a:LocationCode i:nil="true"></a:LocationCode> <a:RoleCode i:nil="true"></a:RoleCode> <a:TerminalInfo i:nil="true"></a:TerminalInfo> <a:ClientName i:nil="true"></a:ClientName> </logonRequestData> </LogonRequest> </s:Body> </s:Envelope>"""
        # spice_token = spice_data(spice_url,'/Sessionmanager.svc',spice_request,spice_header={"Content-Type":"text/xml; charset=utf-8", "SOAPAction":"http://schemas.navitaire.com/WebServices/ISessionManager/Logon","Accept-Encoding":"gzip, deflate"})
        # with open("logon.txt", "w") as file:
        #     file.write(str(spice_token))
        #     file.close()
        # data_dict = xmltodict.parse(spice_token, attr_prefix='')
        # data_dict = json.dumps(data_dict)
        # data_dict = json.loads(data_dict)
        # spice_token = data_dict['s:Envelope']['s:Body']['LogonResponse']['Signature']
        # with open("inp_logon.txt", "w") as file:
        #     file.write(str(spice_request))
        #     file.close()

        # spice_request = """<?xml version="1.0" encoding="UTF-8"?> <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"> <s:Header> <h:ContractVersion xmlns:h="http://schemas.navitaire.com/WebServices">420</h:ContractVersion> <h:EnableExceptionStackTrace xmlns:h="http://schemas.navitaire.com/WebServices">false</h:EnableExceptionStackTrace> <h:MessageContractVersion xmlns:h="http://schemas.navitaire.com/WebServices" xmlns:i="http://www.w3.org/2001/XMLSchema-instance" i:nil="true"/> <h:Signature xmlns:h="http://schemas.navitaire.com/WebServices">"""+spice_token+"""</h:Signature> </s:Header> <s:Body> <GetAvailabilityRequest xmlns="http://schemas.navitaire.com/WebServices/ServiceContracts/BookingService"> <TripAvailabilityRequest xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Booking"> <AvailabilityRequests> <AvailabilityRequest> <DepartureStation>DEL</DepartureStation> <ArrivalStation>BOM</ArrivalStation> <BeginDate>2023-02-10T00:00:00</BeginDate> <EndDate>2023-02-10T00:00:00</EndDate> <CarrierCode>SG</CarrierCode> <FlightNumber i:nil="true"/> <FlightType>All</FlightType> <PaxCount>1</PaxCount> <Dow>Daily</Dow> <CurrencyCode>INR</CurrencyCode> <DisplayCurrencyCode i:nil="true"/> <DiscountCode i:nil="true"/> <PromotionCode i:nil="true"/> <AvailabilityType>Default</AvailabilityType> <SourceOrganization i:nil="true"/> <MaximumConnectingFlights>4</MaximumConnectingFlights> <AvailabilityFilter>Default</AvailabilityFilter> <FareClassControl>CompressByProductClass</FareClassControl> <MinimumFarePrice>0</MinimumFarePrice> <MaximumFarePrice>0</MaximumFarePrice> <ProductClassCode i:nil="true"/> <SSRCollectionsMode>None</SSRCollectionsMode> <InboundOutbound>None</InboundOutbound> <NightsStay>0</NightsStay> <IncludeAllotments>false</IncludeAllotments> <BeginTime i:nil="true"/> <EndTime i:nil="true"/> <DepartureStations i:nil="true" xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/> <ArrivalStations i:nil="true" xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/> <FareTypes xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"> <a:string>R</a:string> <a:string>MX</a:string> <a:string>IO</a:string> </FareTypes> <ProductClasses i:nil="true" xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/> <FareClasses i:nil="true" xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/> <PaxPriceTypes> <PaxPriceType> <PaxType>ADT</PaxType> <PaxDiscountCode i:nil="true"/> <PaxCount>0</PaxCount> </PaxPriceType> </PaxPriceTypes> <JourneySortKeys i:nil="true" xmlns:a="http://schemas.navitaire.com/WebServices/DataContracts/Common/Enumerations"/> <TravelClassCodes i:nil="true" xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/> <IncludeTaxesAndFees>true</IncludeTaxesAndFees> <FareRuleFilter>Default</FareRuleFilter> <LoyaltyFilter>MonetaryOnly</LoyaltyFilter> <PaxResidentCountry i:nil="true"/> <TravelClassCodeList i:nil="true" xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/> <SystemCode i:nil="true"/> <CurrentSourceOrganization i:nil="true"/> <PaxPriceDetailList i:nil="true"/> <ServiceBundleControl>Disabled</ServiceBundleControl> <BookingStatus>Default</BookingStatus> </AvailabilityRequest> </AvailabilityRequests> <LoyaltyFilter>MonetaryOnly</LoyaltyFilter> <SourceOrganization i:nil="true"/> <SourceAgentCode i:nil="true"/> <SourceDomainCode i:nil="true"/> <SourceLocationCode i:nil="true"/> <SourceIOSCountryCode i:nil="true"/> <SourceSystemCode i:nil="true"/> <LowFareMode>false</LowFareMode> </TripAvailabilityRequest> </GetAvailabilityRequest> </s:Body> </s:Envelope>"""
        # spice_serach = spice_data(spice_url,'/Bookingmanager.svc',spice_request,spice_header={"Content-Type":"text/xml; charset=utf-8", "SOAPAction":"http://schemas.navitaire.com/WebServices/IBookingManager/GetAvailability","Accept-Encoding":"gzip, deflate"})  
        # with open("search.txt", "w") as file:
        #     file.write(str(spice_serach))
        #     file.close()
        # spice_serach = xmltodict.parse(spice_serach, attr_prefix='')
        # spice_serach = spice_serach['s:Envelope']['s:Body']['GetAvailabilityByTripResponse']['GetTripAvailabilityResponse']['Schedules']['ArrayOfJourneyDateMarket']['JourneyDateMarket']
        # with open("inp_search.txt", "w") as file:
        #     file.write(str(spice_request))
        #     file.close()
        # return JsonResponse(spice_serach)

        # spice_serach = xmltodict.parse(spice_serach, attr_prefix='')
        # return Response(spice_serach)
        # with open("inp_price_iti.txt", "w") as file:
        #     file.write(str(spice_request))
        #     file.close()
        
        # with open("static/flight/gds_search.xml") as xml_file:
        #     gds_request = xml_file.read()
        
        
        # print(gds_data)
        # try:
        #     temp = []
        #     type = [{"type":"ADT","count":adult}]
        #     if child != 0:
        #         type.append({"type":"CHD","count":child})
        #     if infant != 0:
        #         type.append({"type":"INFT","count":infant})

        #     akasa_request ={"origin":fromCityOrAirport,"destination":toCityOrAirport,"searchDestinationMacs":True,"searchOriginMacs":True,"beginDate":travelDate_akasa,"endDate":None,"getAllDetails":True,"taxesAndFees":"TaxesAndFees","passengers":{"types": type},"codes":{"currencyCode":"INR","promotionCode":""},"numberOfFaresPerJourney":4,"filters":{"compressionType":1,"groupByDate":False,"carrierCode":"QP","type":"ALL","maxConnections":4,"productClasses":["EC","AV","SP"],"sortOptions":["NoSort"],"fareTypes":["R","V","S"]}}
        #     akasaa_data = akasa_data(akasa_url, '/api/nsk/v4/availability/search/simple', akasa_request,akasa_header={"Authorization":akasa_token})
        #     akasaa_data=akasaa_data.json()
        #     with open("static/flight/airport_list.json", "r") as f:
        #         airport = json.loads(f.read())
        #     print('errors' not in akasaa_data)
        #     if('errors' not in akasaa_data):
        #         for i in akasaa_data['data']['results']:
        #             for a in i['trips']: 
        #                 for b in a['journeysAvailableByMarket'].values():
        #                     for c in b:
        #                         for d in c['segments']:
        #                             for e in d['legs']:
        #                                 origin = e['designator']['origin']
        #                                 destination = e['designator']['destination']
        #                                 for i in airport:
        #                                     if(origin in i['code']):
        #                                         e['designator']['origin'] = i['name']
        #                                     if(destination in i['code']):
        #                                         e['designator']['destination'] = i['name']
        #                         fare_key = c['fares'][0]['fareAvailabilityKey']
        #                         print(fare_key)
        #                         result = [d for d in akasaa_data['data']['faresAvailable'].values() if d['fareAvailabilityKey'] == fare_key]
        #                         for e in result:
        #                             price = e['totals']['fareTotal']
        # except:
        #     akasa_data = []

    route = [
        {
            "fromCityOrAirport": {
                "code": fromCityOrAirport
            },
            "toCityOrAirport": {
                "code": toCityOrAirport
            },
            "travelDate": travelDate
        }
    ]

    if (toCityOrAirport5):
        num = 5
    elif(toCityOrAirport4):
        num = 4
    elif(toCityOrAirport3):
        num = 3
    else:
        num = 2
        
    if (radio1 == "multi-way"):
        route = []
        for i in range(num):
            addroute = {
                "fromCityOrAirport": {
                    "code": request.GET.get(f'fromCityOrAirport{i+1}')
                },
                "toCityOrAirport": {
                    "code": request.GET.get(f'toCityOrAirport{i+1}')
                },
                "travelDate": request.GET.get(f'travel{i+1}Date')
            }
            route.append(addroute)
    elif (radio1 == "two-way"):
        addroute ={
            "fromCityOrAirport": {
                "code": toCityOrAirport
            },
            "toCityOrAirport": {
            "code": fromCityOrAirport
            },
            
            "travelDate": travelDate1
        }
        route.append(addroute)

    search_request = {
        "searchQuery": {
            "cabinClass": cabinClass,
                "paxInfo": {
                    "ADULT": adult,
                    "CHILD": child,
                    "INFANT": infant
                },
            "searchModifiers": {
                "pft": Special,
                "isDirectFlight": True,
                "isConnectingFlight": not isDirectFlight,
                },
            "routeInfos":route,
        "preferredAirline": None
        }
    }

    result = flight_data(api_url, apikey, '/fms/v1/air-search-all',search_request)
    data=result.json()
    # return Response(data)
    if result.status_code != 200:
        return render(request, "online_savaari/listing_two.html", {'status':False, 'data':data})

    # if "COMBO" in data["searchResult"]["tripInfos"]:
    #     context={
    #         'data': data,
    #         'search_request': search_request,
    #     }
    #     return JsonResponse(context)

    with open("static/flight/airlines.json", "r") as f:
        airline = json.loads(f.read())

    with open("static/flight/airport_list.json", "r") as f:
        airport = json.loads(f.read())
        l = []
        k = []
        for i in airport:
            if(i['country'] == 'India'):
                air_domestic = i['code']
                l.append(air_domestic)

        for j in airport:
            if(j['country'] != 'India'):
                air_international = j['code']
                k.append(air_international)
    grp_checker = ['COUPON', 'SME', 'CORPORATE', 'CORP_CONNECT', 'OFFER_FARE_WITHOUT_PNR', 'TACTICAL']
    if request.user:
        grp = find_group(request.user)
    else:
        grp = 'Customer'

    if grp == 'Customer':
        for key, onwards in data["searchResult"]["tripInfos"].items():
            onwards_temp = []
            for x in data["searchResult"]["tripInfos"][key]:
                price_list = []
                for y in x["totalPriceList"]:
                    if y["fareIdentifier"] not in grp_checker:
                        price_list.append(y)
                if price_list:
                    x["totalPriceList"] = price_list
                    onwards_temp.append(x)
            data["searchResult"]["tripInfos"][key] = onwards_temp
            
    markup_fix = []
    markup_per = []
    all_markup = []
    all_airline_type = []
    all_airline_type_int = []
    markup_fix = list(Markup.objects.filter(markup_type="domestic", user_type=grp,amount_type= 'fixed').values())
    markup_per = list(Markup.objects.filter(markup_type="domestic", user_type=grp,amount_type='percent').values())
    all_markup = markup_fix + markup_per
    
    for air_name in all_markup:
        test_air = air_name["airline_type"]
        if test_air:
            all_airline_type.append(test_air)

    markup_fix_int = list(Markup.objects.filter(markup_type="international", user_type=grp,amount_type= 'fixed').values())
    markup_per_int = list(Markup.objects.filter(markup_type="international", user_type=grp,amount_type='percent').values())
    all_markup_int = markup_fix_int + markup_per_int
    for air_name_int in all_markup_int:
        test_air = air_name_int["airline_type"]
        if test_air:
            all_airline_type_int.append(test_air)
    print(all_airline_type_int)
        
    if (radio1 == "one-way"):
        airlist = []
        data = remove_air(data, airlist)
        if((toCityOrAirport in l) and (fromCityOrAirport in l)):
            data = editmarkup(data, all_markup, all_airline_type)
        else:
            data = editmarkup(data, all_markup_int, all_airline_type_int)

        grp = find_group(request.user)
        if(grp == "Agent"):
            if('data' in search_sdata):
                sdata = search_sdata['data']
                d_list = [toCityOrAirport, fromCityOrAirport]
                smarkup_none = list(SeriesMarkup.objects.filter(airport_name=None).values())
                smarkup_with_airport = []
                for j in d_list:
                    if SeriesMarkup.objects.filter(airport_name=j).exists():
                        smark = list(SeriesMarkup.objects.filter(airport_name=j).values())
                        smarkup_with_airport.append(smark)
                        break
                
                if smarkup_with_airport:
                    series_mark_up = smarkup_with_airport[0]
                    start_date = series_mark_up[0]['start_date']
                    end_date = series_mark_up[0]['end_date']
                    mark_type = series_mark_up[0]['amount_type']
                    markup_amount = series_mark_up[0]["amount"]
                    temp = []
                    for x in sdata:
                        add = True
                        departure_date = x['departure_date']
                        d_date = departure_date.split("/")
                        yy = int(d_date[0])
                        mm = int(d_date[1])
                        dd = int(d_date[2])
                        departure_date = date(yy,mm,dd)
                        if ((start_date <= departure_date) and (end_date >= departure_date)):
                            tf = x['price']
                            if (mark_type == "fixed"):
                                tf= float(tf) + float(markup_amount)
                                x['price'] = tf
                                x['markup'] = float(markup_amount)
                            if (mark_type == "percent"):
                                addedmarkup = tf*(markup_amount/100)
                                tf= percentage(float(tf), float(markup_amount))
                                x['price'] = tf
                                x['markup'] = addedmarkup
                            # start_date += delta
                        temp.append(x)

                    search_sdata['data'] = temp
                elif smarkup_none:
                    series_mark_up = smarkup_none[0]
                    start_date = smarkup_none[0]['start_date']
                    end_date = smarkup_none[0]['end_date']
                    mark_type = smarkup_none[0]['amount_type']
                    markup_amount = smarkup_none[0]["amount"]
                    temp = []
                    for x in sdata:
                        add = True
                        departure_date = x['departure_date']
                        d_date = departure_date.split("/")
                        yy = int(d_date[0])
                        mm = int(d_date[1])
                        dd = int(d_date[2])
                        departure_date = date(yy,mm,dd)
                        if ((start_date <= departure_date) and (end_date >= departure_date)):
                            tf = x['price']
                            if (mark_type == "fixed"):
                                tf= float(tf) + float(markup_amount)
                                x['price'] = tf
                                x['markup'] = float(markup_amount)
                            if (mark_type == "percent"):
                                addedmarkup = tf*(markup_amount/100)
                                tf= percentage(float(tf), float(markup_amount))
                                x['price'] = tf
                                x['markup'] = addedmarkup
                            # start_date += delta
                        temp.append(x)

                    search_sdata['data'] = temp


    else:
        if "COMBO" not in data["searchResult"]["tripInfos"]:
            data = editmarkup(data, all_markup, all_airline_type)
        else:
            data = editmarkup(data, all_markup_int, all_airline_type_int)
        

    with open("static/flight/airport_list.json", "r") as f:
        airport = json.loads(f.read())
    
    list_comm = []
    # if User.objects.filter(username=request.user).exists():
    #     if((toCityOrAirport in l) and (fromCityOrAirport in l)):
    #         comm = list(Commission.objects.filter(user_type=find_group(request.user),commission_type="Domestic").values())
    #     else:
    #         comm = list(Commission.objects.filter(user_type=find_group(request.user),commission_type="International").values())
    #     email = User.objects.get(username=request.user).email
    #     for i in comm:
    #         if 'All' in i['email'] or email in i['email']:
    #             if((toCityOrAirport in i['route']) and (fromCityOrAirport in i['route'])):
    #                 list_comm.append(i)


    if(radio1 == "one-way"):
        context= {
            "status":True,
            "data":data, 
            "gds_data": json.loads(gds_data),
            "fromCityOrAirport":fromCityOrAirport,
            "toCityOrAirport":toCityOrAirport,
            "adult" : adult,
            "child" : child,
            "infant" : infant,
            "travelDate":travelDate,
            "Person": Person,
            "airport": airport,
            "radio1" : radio1,
            "search_sdata" : search_sdata,
            "token" : token,
            # "akasaa_data":akasaa_data,
            "travelDate_akasa":travelDate_akasa,
            "akasa_token":akasa_token,
            "comm": list_comm,
            # "spice_serach": spice_serach,
            "gds_ref": json.dumps(gds_ref),
            "spice_token": spice_token,
        }
    else:
        context= {
        "status":True,
        "data":data,
        'search_request': search_request,  
        "fromCityOrAirport":fromCityOrAirport,
        "toCityOrAirport":toCityOrAirport,
        "adult" : adult,
        "child" : child,
        "infant" : infant,
        "travelDate":travelDate,
        "Person": Person,
        "airport": airport,
        "radio1" : radio1,
        "token" : token,
        "num" : num,
        "akasa_token" : akasa_token,
        # "akasaa_data" : akasaa_data
    }
    return JsonResponse(context)

@api_view(["GET"])
def search_flight(request):
    login_user = request.user


    data = {}
    for key, value in request.GET.items():
        data[key] = value
    promo = list(Promocode.objects.all().values())
    num = [int(data['ADULT']),int(data['CHILD']),int(data['INFANT'])]
    Person = sum(num)
    token = None
    adult = request.GET.get('ADULT', None)
    child = request.GET.get('CHILD', None)
    infant = request.GET.get('INFANT', None)
    token= None
    akasa_token= None
    grp = find_group(request.user)

    if(grp == 'Agent'):
        search_series = {
                    "Username":"9555202202",
                    "Password":"9800830000@api"
                }
        token_series = series_data(series_url, '/login',search_series,header={"api-key":api_key, "Content-Type":"application/json"})
        series_token=token_series.json()
        print(series_token)
        token = series_token['token']
        
        

    akasa_request = {
                    "credentials": {
                        "username": "QPBOM6061B_01",
                        "password":"New@1234",
                        "domain":"EXT"}
                    }
    token_akasa = akasa_data(akasa_url, '/api/nsk/v2/token',akasa_request,akasa_header={"Content-Type":"application/json"})
    akasa_token=token_akasa.json()
    try:
        akasa_token = akasa_token['data']['token']
        print("akasa_token",akasa_token)
        data['akasa_token'] = akasa_token
    except:
        pass
    data['token'] = token

    context={
        'data': data,
        'akasa_token': akasa_token,
        'Person': Person,
        'adult': adult,
        'child': child,
        'infant': infant,
        'promo': promo,
        'jsondata': json.dumps(data),
        'token':token
    }
    return render(request, "online_savaari/listing_two.html", context)
def func1(data):
    if type(data) == type(dict()):
        res = {}
        for key, val in data.items():
            if (type(val) == type(dict())) or (type(val) == type(list())):
                res[key] = func1(val)
            else:
                res['@' + str(key)] = func1(val)
        return res
        # return {'@' + str(key): func1(val) for key, val in data.items()}
    elif type(data) == type(list()):
        return [func1(val) for val in data]
    return data
def func2(data):
    return xmltodict.unparse(data,full_document=False, pretty=True)
    # return data

def clean_json_keys(obj):
    if isinstance(obj, dict):
        cleaned_obj = {}
        for key, value in obj.items():
            cleaned_key = key.replace('@', '')
            cleaned_obj[cleaned_key] = clean_json_keys(value)
        return cleaned_obj
    elif isinstance(obj, list):
        return [clean_json_keys(item) for item in obj]
    else:
        return obj
    

from lxml import etree
@api_view(["GET","POST"])
def review_flight(request):
    promo = list(Promocode.objects.all().values())
    # return Response(request.GET)
    if request.GET.get('ajax') == 'ajax':
        # allkey = json.load(request.GET.get('allkey'))
        allkey = json.loads(request.GET.get('allkey'))
        search_request = {
                "priceIds" : allkey
            }
        result = flight_data(api_url, apikey, '/fms/v1/review',search_request)
        data=result.json()
        return JsonResponse(data, safe=False)
    if request.method == "GET":
        radio1 = request.GET.get('radio1')
        Person = request.GET.get('Person')
        rtype = request.GET.get('rtype', None)
        key = request.GET.get('key')
        key1 = request.GET.get('key1')
        key2 = request.GET.get('key2')
        key3 = request.GET.get('key3')
        key4 = request.GET.get('key4')
        travelDate_akasa = request.GET.get('travelDate_akasa')
        akasa_token = request.GET.get('akasa_token')
        spice_token = request.GET.get('spice_token')
        jkey = request.GET.get('jkey')
        skey = request.GET.get('skey')
        fkey = request.GET.get('fkey')
        std = request.GET.get('STD')
        print(skey)
        fromCityOrAirport = request.GET.get('fromCityOrAirport', None)
        toCityOrAirport = request.GET.get('toCityOrAirport', None)
        toCityOrAirport= toCityOrAirport.strip()
    if request.method == "POST":
        radio1 = request.POST.get('radio1')
        key = request.POST.get('key')
        key1 = request.POST.get('key1')
        key2 = request.POST.get('key2')
        key3 = request.POST.get('key3')
        key4 = request.POST.get('key4')
        Person = request.POST.get('Person')
        rtype = request.POST.get('rtype', None)
        fromCityOrAirport = request.POST.get('fromCityOrAirport', None)
        toCityOrAirport = request.POST.get('toCityOrAirport', None)
    adult = request.GET.get('adult', None)
    child = request.GET.get('child', None)
    infant = request.GET.get('infant', None)
    token = request.GET.get('token', None)
    travelDateseries = request.GET.get('travelDateseries', None)
    reviewId = request.GET.get('key', None)
    print(child,adult,infant,".............................")


    account = [Agent,Customer,CorporateCust]
    gstdetail = []
    for i in account:
        check = i.objects.filter(user_id=request.user.id)
        if len(check) != 0:
            gstdetail.append(check.values())

    
    with open("static/flight/airport_list.json", "r") as f:
        airport = json.loads(f.read())
        l = []
        k = []
        for i in airport:
            if(i['country'] == 'India'):
                air_domestic = i['code']
                l.append(air_domestic)

        for j in airport:
            if(j['country'] != 'India'):
                air_international = j['code']
                k.append(air_international)
    print("rtype",rtype)
    context = {}
    num = 1
    if (radio1 == "one-way"):
        if rtype == "gds":
            sval = json.loads(request.GET.get('skey', None).replace("000 ","000+"))
            res = {'@' + str(key): val for key, val in sval.items()}
            svalue ={
                    'air:AirSegment':(res)
                    } 
            xmlval = xmltodict.unparse(svalue,full_document=False, pretty=True)
            with open("price_iti.txt", "w") as file:
                file.write(str(xmlval))
                file.close()
            
            Traveler =""
            for a in range(int(adult)):
                Traveler+="""<SearchTraveler xmlns='http://www.travelport.com/schema/air_v52_0' Code='ADT'>
                                <Name xmlns='http://www.travelport.com/schema/common_v52_0' First='Test' Last='Adult' />
                            </SearchTraveler>"""
            for a in range(int(child)):
                Traveler+="""<SearchTraveler xmlns='http://www.travelport.com/schema/air_v52_0' Code='CNN'>
                                        <Name xmlns='http://www.travelport.com/schema/common_v52_0' First='Test' Last='Child'/>
                                    </SearchTraveler>"""
                
            parser1 = etree.XMLParser(encoding="utf-8", recover=True)
            gds_request = """<?xml version="1.0"?> <soapenv:Envelope xmlns:com="http://www.travelport.com/schema/common_v52_0" xmlns:air="http://www.travelport.com/schema/air_v52_0" xmlns:ses="http://www.travelport.com/soa/common/security/SessionContext_v1" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"> <soapenv:Body> <air:AirPriceReq xmlns:air="http://www.travelport.com/schema/air_v52_0" FareRuleType="long" TraceId="trace" TargetBranch="P7189273" CheckOBFees="All" AuthorizedBy="user" xmlns:common="http://www.travelport.com/schema/common_v52_0"> <common:BillingPointOfSaleInfo xmlns:common="http://www.travelport.com/schema/common_v52_0" OriginApplication="UAPI"/> <air:AirItinerary>"""+xmlval+"""</air:AirItinerary> <air:AirPricingModifiers ETicketability="Yes" FaresIndicator="AllFares"> </air:AirPricingModifiers> <com:SearchPassenger BookingTravelerRef="1" Code="ADT"/> </air:AirPriceReq> </soapenv:Body> </soapenv:Envelope>"""
            
            with open("logon.xml", "w") as file:
                file.write(Traveler)
                file.close()



            gds_data = encrypt_gds(gds_request)
            gds_datas = xmltodict.parse(gds_data, attr_prefix='')  
            gds_json_data = json.dumps(gds_datas)
            with open("logon.json", "w") as file:
                file.write(gds_json_data)
                file.close()

            root = ET.fromstring(str(gds_data))
            host_token = root.find(".//{http://www.travelport.com/schema/common_v52_0}HostToken")
            host_token_key = host_token.attrib["Key"]
            host_token_str = ET.tostring(host_token, encoding="unicode").replace('ns0:', 'air:').replace('xmlns:ns0', 'xmlns:air')

            namespace = {'air': 'http://www.travelport.com/schema/air_v52_0'}
            air_segment = root.find('.//air:AirSegment', namespace)
            Baggage_AirSegment= ET.tostring(air_segment).decode().replace('ns0:', 'air:').replace(' xmlns:ns0="http://www.travelport.com/schema/air_v52_0"', '')
            
            air_segment.set("HostTokenRef", host_token_key)
            if "xmlns:ns0" in air_segment.attrib:
                del air_segment.attrib["xmlns:ns0"]
            Set_AirSegment= ET.tostring(air_segment).decode().replace('ns0:', 'air:').replace(' xmlns:ns0="http://www.travelport.com/schema/air_v52_0"', '')
            
            
            # with open("airSegment.xml", "w") as file:
            #     file.write(AirSegment)
            #     file.close()

            set_req = """<soapenv:Envelope
                    xmlns:ses="http://www.travelport.com/soa/common/security/SessionContext_v1"
                    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:common_v52_0="http://www.travelport.com/schema/common_v52_0">
                    <soapenv:Body>
                        <air:SeatMapReq xmlns:air="http://www.travelport.com/schema/air_v52_0"
                            ReturnSeatPricing='true'
                            ReturnBrandingInfo='true' AuthorizedBy="OnlineSavaari" TraceId="OS98789767"
                            TargetBranch="P7189273" xmlns:com="http://www.travelport.com/schema/common_v52_0">
                            <com:BillingPointOfSaleInfo OriginApplication="UAPI" />"""+Set_AirSegment+host_token_str+Traveler+"""
                            </air:SeatMapReq>
                    </soapenv:Body>
                </soapenv:Envelope>"""
            
            baggage_req = """<soapenv:Envelope xmlns:com="http://www.travelport.com/schema/common_v52_0"
                        xmlns:air="http://www.travelport.com/schema/air_v52_0"
                        xmlns:ses="http://www.travelport.com/soa/common/security/SessionContext_v1"
                        xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                        xmlns:common_v52_0="http://www.travelport.com/schema/common_v52_0">
                        <soapenv:Header />
                        <soapenv:Body>
                            <air:AirMerchandisingOfferAvailabilityReq TraceId="OS98789767" AuthorizedBy="OnlineSavaari"
                                TargetBranch="P7189273">
                                <common:BillingPointOfSaleInfo
                                    xmlns:common="http://www.travelport.com/schema/common_v52_0"
                                    OriginApplication="UAPI" />
                                <air:AirSolution>
                                    """+Traveler+Baggage_AirSegment+"""
                                </air:AirSolution>
                            </air:AirMerchandisingOfferAvailabilityReq>
                        </soapenv:Body>
                    </soapenv:Envelope>"""
            
            set_res = encrypt_gds(set_req)
            baggage_req = encrypt_gds(baggage_req)
            with open("seat.xml", "w") as file:
                file.write(baggage_req)
                file.close()
            
            gds_seat_data = xmltodict.parse(set_res, attr_prefix='') 
            gds_seat_datas = json.dumps(gds_seat_data)

            gds_baggage_data = xmltodict.parse(baggage_req, attr_prefix='') 
            gds_baggage_datas = json.dumps(gds_baggage_data)

            request.session['gds_seat_datas'] = gds_seat_datas
            with open("seat.json", "w") as file:
                file.write(gds_seat_datas)
                file.close()         
            
            context= {
                "radio1":radio1,
                "Person":Person,
                "rtype":rtype,
                "adult":adult,
                "child":child,
                "infant":infant,
                "gds_data": json.loads(gds_json_data.replace("SOAP:", "").replace("air:", "").replace("#", "").replace("INR", "")),
                "biswajit_data":gds_json_data,
                "gds_seat_data":gds_seat_datas,
                "gds_baggage_datas":gds_baggage_datas
                }
            return render(request, "online_savaari/gds_review.html", context)
        

        if(rtype == "spicejet"):
            chd_data = ""
            if int(child):
                chd_data = f"""<PaxPriceType>
                            <PaxType>CHD</PaxType>
                            <PaxDiscountCode i:nil="true"></PaxDiscountCode>
                            <PaxCount>{child}</PaxCount>
                        </PaxPriceType>"""
            print(spice_token)
            if spice_token:
                spice_token = spice_token.replace(" ", "+")

            new_key = key.split("^")
            new_key = new_key[0]
            with open("data.json", "w") as file:
                file.write(str(jkey))
                file.close()
            spice_request = """<?xml version="1.0" encoding="UTF-8"?> <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"> <s:Header> <h:ContractVersion xmlns:h="http://schemas.navitaire.com/WebServices">420</h:ContractVersion> <h:EnableExceptionStackTrace xmlns:h="http://schemas.navitaire.com/WebServices">false</h:EnableExceptionStackTrace> <h:MessageContractVersion xmlns:h="http://schemas.navitaire.com/WebServices" xmlns:i="http://www.w3.org/2001/XMLSchema-instance" i:nil="true"/> <h:Signature xmlns:h="http://schemas.navitaire.com/WebServices">"""+spice_token+"""</h:Signature> </s:Header> <s:Body> <PriceItineraryRequest xmlns="http://schemas.navitaire.com/WebServices/ServiceContracts/BookingService"> <ItineraryPriceRequest xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns:a="http://schemas.navitaire.com/WebServices/DataContracts/Booking"> <a:TypeOfSale i:nil="true"/> <a:SSRRequest i:nil="true"/> <a:SellRequest i:nil="true"/> <a:SellByKeyRequest> <a:ActionStatusCode>NN</a:ActionStatusCode> <a:JourneySellKeys> <a:SellKeyList> <a:JourneySellKey>"""+jkey+"""</a:JourneySellKey> <a:FareSellKey>"""+key+"""</a:FareSellKey> <a:StandbyPriorityCode i:nil="true"/> </a:SellKeyList> </a:JourneySellKeys> <a:PaxPriceTypes> <a:PaxPriceType> <a:PaxType>ADT</a:PaxType> <a:PaxDiscountCode i:nil="true"/> <a:PaxCount>"""+str(adult)+"""</a:PaxCount> </a:PaxPriceType>"""+chd_data+""" </a:PaxPriceTypes> <a:CurrencyCode>INR</a:CurrencyCode> <a:SourcePOS xmlns:b="http://schemas.navitaire.com/WebServices/DataContracts/Common"> <b:State>New</b:State> <b:AgentCode>AG</b:AgentCode> <b:OrganizationCode>APITESTID</b:OrganizationCode> <b:DomainCode>WWW</b:DomainCode> <b:LocationCode i:nil="true"/> </a:SourcePOS> <a:PaxCount>"""+str(int(adult) + int(child))+"""</a:PaxCount> <a:TypeOfSale i:nil="true"/> <a:LoyaltyFilter>MonetaryOnly</a:LoyaltyFilter> <a:IsAllotmentMarketFare>false</a:IsAllotmentMarketFare> <a:SourceBookingPOS i:nil="true" xmlns:b="http://schemas.navitaire.com/WebServices/DataContracts/Common"/> <a:PreventOverLap>false</a:PreventOverLap> <a:ReplaceAllPassengersOnUpdate>false</a:ReplaceAllPassengersOnUpdate> <a:ServiceBundleList i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/> <a:ApplyServiceBundle>No</a:ApplyServiceBundle> </a:SellByKeyRequest> <a:PriceJourneyWithLegsRequest i:nil="true"/> <a:PriceItineraryBy>JourneyBySellKey</a:PriceItineraryBy> <a:BookingStatus>Default</a:BookingStatus> </ItineraryPriceRequest> </PriceItineraryRequest> </s:Body> </s:Envelope>"""
            spice_serach = spice_data(spice_url,'/Bookingmanager.svc',spice_request,spice_header={"Content-Type":"text/xml", "SOAPAction":"http://schemas.navitaire.com/WebServices/IBookingManager/GetItineraryPrice","Accept-Encoding":"gzip, deflate"})  
            with open("price_iti.xml", "w") as file:
                file.write(str(spice_serach))
                file.close()
            with open("inp_price_iti.xml", "w") as file:
                file.write(str(spice_request))
                file.close()
            spice_serach = xmltodict.parse(spice_serach, attr_prefix='')
            spice_serach = json.dumps(spice_serach)
            spice_serach = json.loads(spice_serach)
            
            seg = spice_serach['s:Envelope']['s:Body']['PriceItineraryResponse']['Booking']['Journeys']['Journey']['Segments']['Segment']
            flight_no = ""
            if type(seg) == type(list()):
                flight_no = seg[0]['FlightDesignator']['a:FlightNumber']
            else:
                flight_no = seg['FlightDesignator']['a:FlightNumber']
            # flight_no = spice_serach['s:Envelope']['s:Body']['PriceItineraryResponse']['Booking']['Journeys']['Journey']['Segments']['Segment']['FlightDesignator']['a:FlightNumber']
            # return Response(spice_serach)

                
            spice_request = """<?xml version="1.0" encoding="UTF-8"?> <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"> <s:Header> <h:ContractVersion xmlns:h="http://schemas.navitaire.com/WebServices">420</h:ContractVersion> <h:EnableExceptionStackTrace xmlns:h="http://schemas.navitaire.com/WebServices">false</h:EnableExceptionStackTrace> <h:MessageContractVersion xmlns:h="http://schemas.navitaire.com/WebServices" xmlns:i="http://www.w3.org/2001/XMLSchema-instance" i:nil="true"/> <h:Signature xmlns:h="http://schemas.navitaire.com/WebServices">"""+spice_token+"""</h:Signature> </s:Header> <s:Body> <SellRequest xmlns="http://schemas.navitaire.com/WebServices/ServiceContracts/BookingService"> <SellRequestData xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns:a="http://schemas.navitaire.com/WebServices/DataContracts/Booking"> <a:SellBy>JourneyBySellKey</a:SellBy> <a:SellJourneyByKeyRequest> <a:SellJourneyByKeyRequestData> <a:ActionStatusCode>NN</a:ActionStatusCode> <a:JourneySellKeys> <a:SellKeyList> <a:JourneySellKey>"""+jkey+"""</a:JourneySellKey> <a:FareSellKey>"""+key+"""</a:FareSellKey> <a:StandbyPriorityCode i:nil="true"/> </a:SellKeyList> </a:JourneySellKeys> <a:PaxPriceTypes> <a:PaxPriceType> <a:PaxType>ADT</a:PaxType> <a:PaxDiscountCode i:nil="true"/> <a:PaxCount>"""+str(adult)+"""</a:PaxCount> </a:PaxPriceType>"""+chd_data+"""</a:PaxPriceTypes> <a:CurrencyCode>INR</a:CurrencyCode> <a:SourcePOS xmlns:b="http://schemas.navitaire.com/WebServices/DataContracts/Common"> <b:State>New</b:State> <b:AgentCode>AG</b:AgentCode> <b:OrganizationCode>APITESTID</b:OrganizationCode> <b:DomainCode>WWW</b:DomainCode> <b:LocationCode i:nil="true"/> </a:SourcePOS> <a:PaxCount>"""+str(int(adult) + int(child))+"""</a:PaxCount> <a:TypeOfSale i:nil="true"/> <a:LoyaltyFilter>MonetaryOnly</a:LoyaltyFilter> <a:IsAllotmentMarketFare>false</a:IsAllotmentMarketFare> <a:SourceBookingPOS i:nil="true" xmlns:b="http://schemas.navitaire.com/WebServices/DataContracts/Common"/> <a:PreventOverLap>false</a:PreventOverLap> <a:ReplaceAllPassengersOnUpdate>false</a:ReplaceAllPassengersOnUpdate> <a:ServiceBundleList i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/> <a:ApplyServiceBundle>No</a:ApplyServiceBundle> </a:SellJourneyByKeyRequestData> </a:SellJourneyByKeyRequest> <a:SellJourneyRequest i:nil="true"/> <a:SellSSR i:nil="true"/> <a:SellFee i:nil="true"/> </SellRequestData> </SellRequest> </s:Body> </s:Envelope>"""
            spice_review = spice_data(spice_url,'/Bookingmanager.svc',spice_request,spice_header={"Content-Type":"text/xml; charset=utf-8", "SOAPAction":"http://schemas.navitaire.com/WebServices/IBookingManager/Sell","Accept-Encoding":"gzip, deflate"})  
            with open("sell.txt", "w") as file:
                file.write(str(spice_review))
                file.close()
            spice_review = xmltodict.parse(spice_review, attr_prefix='')
            spice_review = json.dumps(spice_review)
            spice_review = json.loads(spice_review)
            # return Response(spice_review)
            
            # spice_request = """<?xml version="1.0" encoding="UTF-8"?> <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"> <s:Header> <h:ContractVersion xmlns:h="http://schemas.navitaire.com/WebServices">420</h:ContractVersion> <h:EnableExceptionStackTrace xmlns:h="http://schemas.navitaire.com/WebServices">false</h:EnableExceptionStackTrace> <h:MessageContractVersion xmlns:h="http://schemas.navitaire.com/WebServices" xmlns:i="http://www.w3.org/2001/XMLSchema-instance" i:nil="true"/> <h:Signature xmlns:h="http://schemas.navitaire.com/WebServices">"""+spice_token+"""</h:Signature> </s:Header> <s:Body> <SellRequest xmlns="http://schemas.navitaire.com/WebServices/ServiceContracts/BookingService"> <SellRequestData xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns:a="http://schemas.navitaire.com/WebServices/DataContracts/Booking"> <a:SellBy>SSR</a:SellBy> <a:SellJourneyByKeyRequest i:nil="true"/> <a:SellJourneyRequest i:nil="true"/> <a:SellSSR> <a:SSRRequest> <a:SegmentSSRRequests> <a:SegmentSSRRequest> <a:FlightDesignator xmlns:b="http://schemas.navitaire.com/WebServices/DataContracts/Common"> <b:CarrierCode>SG</b:CarrierCode> <b:FlightNumber>"""+flight_no+"""</b:FlightNumber> <b:OpSuffix i:nil="true"/> </a:FlightDesignator> <a:STD>"""+std+"""</a:STD> <a:DepartureStation>DEL</a:DepartureStation> <a:ArrivalStation>COK</a:ArrivalStation> <a:PaxSSRs> <a:PaxSSR> <State xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Common">New</State> <a:ActionStatusCode>NN</a:ActionStatusCode> <a:ArrivalStation>COK</a:ArrivalStation> <a:DepartureStation>DEL</a:DepartureStation> <a:PassengerNumber>0</a:PassengerNumber> <a:SSRCode>INFT</a:SSRCode> <a:SSRNumber>0</a:SSRNumber> <a:SSRDetail i:nil="true"/> <a:FeeCode i:nil="true"/> <a:Note i:nil="true"/> <a:SSRValue>0</a:SSRValue> <a:IsInServiceBundle>false</a:IsInServiceBundle> </a:PaxSSR> <a:PaxSSR> <State xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Common">New</State> <a:ActionStatusCode>NN</a:ActionStatusCode> <a:ArrivalStation>PNQ</a:ArrivalStation> <a:DepartureStation>DEL</a:DepartureStation> <a:PassengerNumber>1</a:PassengerNumber> <a:SSRCode>VGML</a:SSRCode> <a:SSRNumber>0</a:SSRNumber> <a:SSRDetail i:nil="true"/> <a:FeeCode i:nil="true"/> <a:Note i:nil="true"/> <a:SSRValue>0</a:SSRValue> <a:IsInServiceBundle>false</a:IsInServiceBundle> </a:PaxSSR> </a:PaxSSRs> </a:SegmentSSRRequest> </a:SegmentSSRRequests> <a:CurrencyCode>INR</a:CurrencyCode> <a:CancelFirstSSR>false</a:CancelFirstSSR> <a:SSRFeeForceWaiveOnSell>false</a:SSRFeeForceWaiveOnSell> <a:SellSSRMode>NonBundle</a:SellSSRMode> </a:SSRRequest> <a:OptimizationInputParameterList i:nil="true"/> </a:SellSSR> <a:SellFee i:nil="true"/> </SellRequestData> </SellRequest> </s:Body> </s:Envelope>"""
            
            spice_request = """<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Header><h:ContractVersion xmlns:h="http://schemas.navitaire.com/WebServices">420</h:ContractVersion><h:EnableExceptionStackTrace xmlns:h="http://schemas.navitaire.com/WebServices">false</h:EnableExceptionStackTrace><h:MessageContractVersion i:nil="true" xmlns:h="http://schemas.navitaire.com/WebServices" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"></h:MessageContractVersion><h:Signature xmlns:h="http://schemas.navitaire.com/WebServices">"""+spice_token+"""</h:Signature></s:Header><s:Body><GetSSRAvailabilityForBookingRequest xmlns="http://schemas.navitaire.com/WebServices/ServiceContracts/BookingService"><SSRAvailabilityForBookingRequest xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Booking" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><SegmentKeyList><LegKey><CarrierCode xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Common">SG</CarrierCode><FlightNumber xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Common">"""+flight_no+"""</FlightNumber><OpSuffix i:nil="true" xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Common"></OpSuffix><DepartureDate>"""+std+"""</DepartureDate><DepartureStation>"""+fromCityOrAirport+"""</DepartureStation><ArrivalStation>"""+toCityOrAirport+"""</ArrivalStation></LegKey></SegmentKeyList><PassengerNumberList xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"><a:short>"""+str(int(adult) + int(child) -1)+"""</a:short></PassengerNumberList><InventoryControlled>true</InventoryControlled><NonInventoryControlled>true</NonInventoryControlled><SeatDependent>true</SeatDependent><NonSeatDependent>true</NonSeatDependent><CurrencyCode>INR</CurrencyCode><OptimizationInputParameterList i:nil="true"></OptimizationInputParameterList><SSRAvailabilityMode>NonBundledSSRs</SSRAvailabilityMode></SSRAvailabilityForBookingRequest></GetSSRAvailabilityForBookingRequest></s:Body></s:Envelope>"""
            spice_ssr = spice_data(spice_url,'/Bookingmanager.svc',spice_request,spice_header={"Content-Type":"text/xml; charset=utf-8", "SOAPAction":"http://schemas.navitaire.com/WebServices/IBookingManager/GetSSRAvailabilityForBooking","Accept-Encoding":"gzip, deflate"})  

            with open("inp_spice_ssr.txt", "w") as file:
                file.write(str(spice_request))
                file.close()
            spice_ssr = xmltodict.parse(spice_ssr, attr_prefix='')
            spice_ssr = json.dumps(spice_ssr)
            with open("spice_ssr_out.txt", "w") as file:
                file.write(str(spice_ssr))
                file.close()
            spice_ssr = json.loads(json.dumps(spice_ssr).replace('s:', "").replace('a:', ""))
            apiamount = spice_serach['s:Envelope']['s:Body']['PriceItineraryResponse']['Booking']['BookingSum']['TotalCost']

            spice_request = """<?xml version="1.0" encoding="UTF-8"?> <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"> <s:Header> <h:ContractVersion xmlns:h="http://schemas.navitaire.com/WebServices">420</h:ContractVersion> <h:EnableExceptionStackTrace xmlns:h="http://schemas.navitaire.com/WebServices">false</h:EnableExceptionStackTrace> <h:MessageContractVersion xmlns:h="http://schemas.navitaire.com/WebServices" xmlns:i="http://www.w3.org/2001/XMLSchema-instance" i:nil="true"/> <h:Signature xmlns:h="http://schemas.navitaire.com/WebServices">"""+spice_token+"""</h:Signature> </s:Header> <s:Body> <GetSeatAvailabilityRequest xmlns="http://schemas.navitaire.com/WebServices/ServiceContracts/BookingService"> <SeatAvailabilityRequest xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Booking"> <STD>"""+std+"""</STD> <DepartureStation>"""+fromCityOrAirport+"""</DepartureStation> <ArrivalStation>"""+toCityOrAirport+"""</ArrivalStation> <IncludeSeatFees>true</IncludeSeatFees> <SeatAssignmentMode>PreSeatAssignment</SeatAssignmentMode> <FlightNumber>"""+flight_no+"""</FlightNumber> <CarrierCode>SG</CarrierCode> <OpSuffix i:nil="true"/> <CompressProperties>false</CompressProperties> <EnforceSeatGroupRestrictions>true</EnforceSeatGroupRestrictions> <PassengerIDs xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"> <a:long>0</a:long> </PassengerIDs> <PassengerSeatPreferences i:nil="true"/> <SeatGroup>0</SeatGroup> <SeatGroupSettings i:nil="true" xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/> <EquipmentDeviations i:nil="true"/> <IncludePropertyLookup>true</IncludePropertyLookup> <OverrideCarrierCode i:nil="true"/> <OverrideFlightNumber i:nil="true"/> <OverrideOpSuffix i:nil="true"/> <OverrideSTD>0001-01-01T00:00:00</OverrideSTD> <OverrideDepartureStation i:nil="true"/> <OverrideArrivalStation i:nil="true"/> <CollectedCurrencyCode i:nil="true"/> <ExcludeEquipmentConfiguration>false</ExcludeEquipmentConfiguration> <SeatAvailabilityFilter i:nil="true"/> <OptimizationInputParameterList i:nil="true"/> </SeatAvailabilityRequest> </GetSeatAvailabilityRequest> </s:Body> </s:Envelope>"""
            spice_seal_avail = spice_data(spice_url,'/Bookingmanager.svc',spice_request,spice_header={"Content-Type":"text/xml; charset=utf-8", "SOAPAction":"http://schemas.navitaire.com/WebServices/IBookingManager/GetSeatAvailability","Accept-Encoding":"gzip, deflate"})  
            with open("seat_avail.txt", "w") as file:
                file.write(str(spice_seal_avail))
                file.close()
            spice_seal_avail = xmltodict.parse(spice_seal_avail, attr_prefix='')
            spice_seal_avail = json.dumps(spice_seal_avail)
            spice_seal_avail = json.loads(json.dumps(spice_seal_avail).replace('s:', "").replace('a:', ""))

            with open("inp_seat_avail.txt", "w") as file:
                file.write(str(spice_request))
                file.close()
            context= {
                "radio1":radio1,
                "Person":Person,
                "rtype":rtype,
                "apiamount":apiamount,
                "adult":adult,
                "child":child,
                "infant":infant,
                "spice_data": json.loads(json.dumps(spice_serach).replace("s:", "")),
                "spice_ssr": json.loads(json.dumps(spice_ssr).replace("s:", "")),
                "spice_seat": json.loads(json.dumps(spice_seal_avail).replace("s:", "")),
                'spice_token': spice_token,
                }
            # return Response(context)
            with open("inp_sell.txt", "w") as file:
                file.write(str(spice_request))
                file.close()
            return render(request, "online_savaari/spice_review.html", context)

            # spice_request = """<?xml version="1.0" encoding="UTF-8"?> <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"> <s:Header> <h:ContractVersion xmlns:h="http://schemas.navitaire.com/WebServices">420</h:ContractVersion> <h:EnableExceptionStackTrace xmlns:h="http://schemas.navitaire.com/WebServices">false</h:EnableExceptionStackTrace> <h:MessageContractVersion xmlns:h="http://schemas.navitaire.com/WebServices" xmlns:i="http://www.w3.org/2001/XMLSchema-instance" i:nil="true"/> <h:Signature xmlns:h="http://schemas.navitaire.com/WebServices">"""+spice_token+"""</h:Signature> </s:Header> <s:Body> <GetSeatAvailabilityRequest xmlns="http://schemas.navitaire.com/WebServices/ServiceContracts/BookingService"> <SeatAvailabilityRequest xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Booking"> <STD>"""+std+"""</STD> <DepartureStation>DEL</DepartureStation> <ArrivalStation>BOM</ArrivalStation> <IncludeSeatFees>true</IncludeSeatFees> <SeatAssignmentMode>PreSeatAssignment</SeatAssignmentMode> <FlightNumber>8709</FlightNumber> <CarrierCode>SG</CarrierCode> <OpSuffix i:nil="true"/> <CompressProperties>false</CompressProperties> <EnforceSeatGroupRestrictions>true</EnforceSeatGroupRestrictions> <PassengerIDs xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"> <a:long>0</a:long> </PassengerIDs> <PassengerSeatPreferences i:nil="true"/> <SeatGroup>0</SeatGroup> <SeatGroupSettings i:nil="true" xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/> <EquipmentDeviations i:nil="true"/> <IncludePropertyLookup>true</IncludePropertyLookup> <OverrideCarrierCode i:nil="true"/> <OverrideFlightNumber i:nil="true"/> <OverrideOpSuffix i:nil="true"/> <OverrideSTD>0001-01-01T00:00:00</OverrideSTD> <OverrideDepartureStation i:nil="true"/> <OverrideArrivalStation i:nil="true"/> <CollectedCurrencyCode i:nil="true"/> <ExcludeEquipmentConfiguration>false</ExcludeEquipmentConfiguration> <SeatAvailabilityFilter i:nil="true"/> <OptimizationInputParameterList i:nil="true"/> </SeatAvailabilityRequest> </GetSeatAvailabilityRequest> </s:Body> </s:Envelope>"""
            # spice_seal_avail = spice_data(spice_url,'/Bookingmanager.svc',spice_request,spice_header={"Content-Type":"text/xml; charset=utf-8", "SOAPAction":"http://schemas.navitaire.com/WebServices/IBookingManager/GetSeatAvailability","Accept-Encoding":"gzip, deflate"})  
            # with open("seat_avail.txt", "w") as file:
            #     file.write(str(spice_seal_avail))
            #     file.close()
            # spice_seal_avail = xmltodict.parse(spice_seal_avail, attr_prefix='')
            # spice_seal_avail = json.dumps(spice_seal_avail)
            # spice_seal_avail = json.loads(spice_seal_avail)
            # with open("inp_seat_avail.txt", "w") as file:
            #     file.write(str(spice_request))
            #     file.close()

            # spice_request = """<?xml version="1.0" encoding="UTF-8"?> <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"> <s:Header> <h:ContractVersion xmlns:h="http://schemas.navitaire.com/WebServices">420</h:ContractVersion> <h:EnableExceptionStackTrace xmlns:h="http://schemas.navitaire.com/WebServices">false</h:EnableExceptionStackTrace> <h:MessageContractVersion xmlns:h="http://schemas.navitaire.com/WebServices" xmlns:i="http://www.w3.org/2001/XMLSchema-instance" i:nil="true"/> <h:Signature xmlns:h="http://schemas.navitaire.com/WebServices">"""+spice_token+"""</h:Signature> </s:Header> <s:Body> <UpdatePassengersRequest xmlns="http://schemas.navitaire.com/WebServices/ServiceContracts/BookingService"> <updatePassengersRequestData xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns:a="http://schemas.navitaire.com/WebServices/DataContracts/Booking"> <a:Passengers> <a:Passenger> <State xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Common">New</State> <a:PassengerPrograms i:nil="true"/> <a:CustomerNumber i:nil="true"/> <a:PassengerNumber>0</a:PassengerNumber> <a:FamilyNumber>0</a:FamilyNumber> <a:PaxDiscountCode i:nil="true"/> <a:Names> <a:BookingName> <State xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Common">New</State> <a:FirstName>THREE</a:FirstName> <a:MiddleName i:nil="true"/> <a:LastName>TEST</a:LastName> <a:Suffix i:nil="true"/> <a:Title>MR</a:Title> </a:BookingName> </a:Names> <a:Infant i:nil="true"/> <a:PassengerInfo> <State xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Common">New</State> <a:BalanceDue>0</a:BalanceDue> <a:Gender>Male</a:Gender> <a:Nationality i:nil="true"/> <a:ResidentCountry i:nil="true"/> <a:TotalCost>0</a:TotalCost> <a:WeightCategory>Male</a:WeightCategory> </a:PassengerInfo> <a:PassengerProgram i:nil="true"/> <a:PassengerFees i:nil="true"/> <a:PassengerAddresses i:nil="true"/> <a:PassengerTravelDocuments i:nil="true"/> <a:PassengerBags i:nil="true"/> <a:PassengerID>0</a:PassengerID> <a:PassengerTypeInfos> <a:PassengerTypeInfo> <a:State>New</a:State> <a:DOB>0001-01-01T00:00:00</a:DOB> <a:PaxType>ADT</a:PaxType> </a:PassengerTypeInfo> </a:PassengerTypeInfos> <a:PassengerInfos i:nil="true"/> <a:PassengerInfants i:nil="true"/> <a:PseudoPassenger>false</a:PseudoPassenger> <a:PassengerTypeInfo i:nil="true"/> <a:PassengerEMDCouponList i:nil="true"/> </a:Passenger> </a:Passengers> <a:WaiveNameChangeFee>false</a:WaiveNameChangeFee> </updatePassengersRequestData> </UpdatePassengersRequest> </s:Body> </s:Envelope>"""
            # update_pax = spice_data(spice_url,'/Bookingmanager.svc',spice_request,spice_header={"Content-Type":"text/xml; charset=utf-8", "SOAPAction":"http://schemas.navitaire.com/WebServices/IBookingManager/UpdatePassengers","Accept-Encoding":"gzip, deflate"})  
            # with open("update_pax.txt", "w") as file:
            #     file.write(str(update_pax))
            #     file.close()
            # update_pax = xmltodict.parse(update_pax, attr_prefix='')
            # update_pax = json.dumps(update_pax)
            # update_pax = json.loads(update_pax)
            # due_amount = update_pax['s:Envelope']['s:Body']['UpdatePassengerResponse']['BookingUpdateResponseData']['Success']['PNRAmount']['BalanceDue']
            # with open("inp_update_pax.txt", "w") as file:
            #     file.write(str(spice_request))
            #     file.close()

            # spice_request = """<?xml version="1.0" encoding="UTF-8"?> <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"> <s:Header> <h:ContractVersion xmlns:h="http://schemas.navitaire.com/WebServices">420</h:ContractVersion> <h:EnableExceptionStackTrace xmlns:h="http://schemas.navitaire.com/WebServices">false</h:EnableExceptionStackTrace> <h:MessageContractVersion xmlns:h="http://schemas.navitaire.com/WebServices" xmlns:i="http://www.w3.org/2001/XMLSchema-instance" i:nil="true"/> <h:Signature xmlns:h="http://schemas.navitaire.com/WebServices">"""+spice_token+"""</h:Signature> </s:Header> <s:Body> <AddPaymentToBookingRequest xmlns="http://schemas.navitaire.com/WebServices/ServiceContracts/BookingService"> <addPaymentToBookingReqData xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Booking"> <MessageState>New</MessageState> <WaiveFee>false</WaiveFee> <ReferenceType>Default</ReferenceType> <PaymentMethodType>AgencyAccount</PaymentMethodType> <PaymentMethodCode>AG</PaymentMethodCode> <QuotedCurrencyCode>INR</QuotedCurrencyCode> <QuotedAmount>"""+due_amount+"""</QuotedAmount> <Status>New</Status> <AccountNumberID>0</AccountNumberID> <AccountNumber>APITESTID</AccountNumber> <Expiration>0001-01-01T00:00:00</Expiration> <ParentPaymentID>0</ParentPaymentID> <Installments>0</Installments> <PaymentText i:nil="true"/> <Deposit>false</Deposit> <PaymentFields i:nil="true"/> <PaymentAddresses i:nil="true"/> <AgencyAccount i:nil="true"/> <CreditShell i:nil="true"/> <CreditFile i:nil="true"/> <PaymentVoucher i:nil="true"/> <ThreeDSecureRequest i:nil="true"/> <MCCRequest i:nil="true"/> <AuthorizationCode i:nil="true"/> </addPaymentToBookingReqData> </AddPaymentToBookingRequest> </s:Body> </s:Envelope>"""
            # spice_payment = spice_data(spice_url,'/Bookingmanager.svc',spice_request,spice_header={"Content-Type":"text/xml; charset=utf-8", "SOAPAction":"http://schemas.navitaire.com/WebServices/IBookingManager/AddPaymentToBooking","Accept-Encoding":"gzip, deflate"})  
            # with open("update_pay.txt", "w") as file:
            #     file.write(str(spice_payment))
            #     file.close()
            # spice_payment = xmltodict.parse(spice_payment, attr_prefix='')
            # spice_payment = json.dumps(spice_payment)
            # spice_payment = json.loads(spice_payment)
            # with open("inp_update_pay.txt", "w") as file:
            #     file.write(str(spice_request))
            #     file.close()

            # spice_request = """<?xml version="1.0" encoding="UTF-8"?> <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"> <s:Header> <h:ContractVersion xmlns:h="http://schemas.navitaire.com/WebServices">420</h:ContractVersion> <h:EnableExceptionStackTrace xmlns:h="http://schemas.navitaire.com/WebServices">false</h:EnableExceptionStackTrace> <h:MessageContractVersion xmlns:h="http://schemas.navitaire.com/WebServices" xmlns:i="http://www.w3.org/2001/XMLSchema-instance" i:nil="true"/> <h:Signature xmlns:h="http://schemas.navitaire.com/WebServices">"""+spice_token+"""</h:Signature> </s:Header> <s:Body> <BookingCommitRequest xmlns="http://schemas.navitaire.com/WebServices/ServiceContracts/BookingService"> <BookingCommitRequestData xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Booking"> <State>New</State> <RecordLocator i:nil="true"/> <CurrencyCode>INR</CurrencyCode> <PaxCount>1</PaxCount> <SystemCode i:nil="true"/> <BookingID>0</BookingID> <BookingParentID>0</BookingParentID> <ParentRecordLocator i:nil="true"/> <BookingChangeCode i:nil="true"/> <GroupName i:nil="true"/> <SourcePOS xmlns:a="http://schemas.navitaire.com/WebServices/DataContracts/Common"> <a:State>New</a:State> <a:AgentCode>AG</a:AgentCode> <a:OrganizationCode>APITESTID</a:OrganizationCode> <a:DomainCode>WWW</a:DomainCode> <a:LocationCode i:nil="true"/> </SourcePOS> <BookingHold i:nil="true"/> <ReceivedBy> <State xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Common">New</State> <ReceivedBy>APITESTID</ReceivedBy> <ReceivedReference i:nil="true"/> <ReferralCode i:nil="true"/> <LatestReceivedBy i:nil="true"/> <LatestReceivedReference i:nil="true"/> </ReceivedBy> <RecordLocators i:nil="true" xmlns:a="http://schemas.navitaire.com/WebServices/DataContracts/Common"/> <Passengers i:nil="true"/> <BookingComments i:nil="true"/> <BookingContacts> <BookingContact> <State xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Common">New</State> <TypeCode>P</TypeCode> <Names> <BookingName> <State xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Common">New</State> <FirstName>THREE</FirstName> <MiddleName i:nil="true"/> <LastName>TEST</LastName> <Suffix i:nil="true"/> <Title>MR</Title> </BookingName> </Names> <EmailAddress>TEST@TEST.COM</EmailAddress> <HomePhone>+919090909090</HomePhone> <WorkPhone i:nil="true"/> <OtherPhone i:nil="true"/> <Fax i:nil="true"/> <CompanyName>Online Savaari Pvt Ltd</CompanyName> <AddressLine1>A</AddressLine1> <AddressLine2>B</AddressLine2> <AddressLine3 i:nil="true"/> <City>GGN</City> <ProvinceState i:nil="true"/> <PostalCode i:nil="true"/> <CountryCode>IN</CountryCode> <CultureCode>en-GB</CultureCode> <DistributionOption>Email</DistributionOption> <CustomerNumber i:nil="true"/> <NotificationPreference>None</NotificationPreference> <SourceOrganization>APITESTID</SourceOrganization> </BookingContact> </BookingContacts> <NumericRecordLocator i:nil="true"/> <RestrictionOverride>false</RestrictionOverride> <ChangeHoldDateTime>false</ChangeHoldDateTime> <WaiveNameChangeFee>false</WaiveNameChangeFee> <WaivePenaltyFee>false</WaivePenaltyFee> <WaiveSpoilageFee>false</WaiveSpoilageFee> <DistributeToContacts>true</DistributeToContacts> <SourceBookingPOS i:nil="true" xmlns:a="http://schemas.navitaire.com/WebServices/DataContracts/Common"/> </BookingCommitRequestData> </BookingCommitRequest> </s:Body> </s:Envelope>"""
            # spice_booking = spice_data(spice_url,'/Bookingmanager.svc',spice_request,spice_header={"Content-Type":"text/xml; charset=utf-8", "SOAPAction":"http://schemas.navitaire.com/WebServices/IBookingManager/BookingCommit","Accept-Encoding":"gzip, deflate"})  
            # with open("booking.txt", "w") as file:
            #     file.write(str(spice_booking))
            #     file.close()
            # spice_booking = xmltodict.parse(spice_booking, attr_prefix='')
            # spice_booking = json.dumps(spice_booking)
            # spice_booking = json.loads(spice_booking)
            # with open("inp_booking.txt", "w") as file:
            #     file.write(str(spice_request))
            #     file.close()  
            
        
        if rtype == "akasa":
            adult = int(adult)
            child = int(child)
            infant = int(infant)
            type = [{"type":"ADT","count":adult}]
            if child != 0:
                type.append({"type":"CHD","count":child})
            # type.append({"type":"INFT","count":1})
            # return Response(type)
            akasa_request ={"keys":[{"journeyKey":jkey,"fareAvailabilityKey":fkey}],"passengers":{"types":type},"currencyCode":"INR"}

            akasaa_data = akasa_data(akasa_url, '/api/nsk/v4/trip/sell', akasa_request,akasa_header={"Authorization":akasa_token})
            akasaa_data=akasaa_data.json()
            # return Response(akasaa_data)
            passengerkey = list((akasaa_data['data']['breakdown']['passengers']).keys())
            apiamount = akasaa_data['data']['breakdown']['totalAmount']
            for c in akasaa_data['data']['journeys']:
                for d in c['segments']:
                    ak_id = d['identifier']['identifier']
                    carr_code = d['identifier']['carrierCode']
                    passengerKey = list(akasaa_data['data']['breakdown']['passengers'].keys())
            akasa_request = {"trips":[{"identifier":{"identifier":ak_id,"carrierCode":carr_code},"destination":toCityOrAirport,"origin":fromCityOrAirport,"departureDate":travelDate_akasa}],"passengerKeys":passengerKey,"currencyCode":"INR"}
            akasa_ssr = akasa_data(akasa_url, '/api/nsk/v2/booking/ssrs/availability', akasa_request,akasa_header={"Authorization":akasa_token})
            akasa_ssr=akasa_ssr.json()
            seat_list = []
            seat_map_endpoint = '/api/nsk/v2/booking/seatmaps/segment/'+skey
            akasa_seat_map = akasa_seat(akasa_url, seat_map_endpoint,akasa_header={"Authorization":akasa_token})
            akasa_seat_map = akasa_seat_map.json()
            seat_list.append(akasa_seat_map)
            if request.GET.get('skey1'):
                seat_map_endpoint = '/api/nsk/v2/booking/seatmaps/segment/'+request.GET.get('skey1')
                akasa_seat_map = akasa_seat(akasa_url, seat_map_endpoint,akasa_header={"Authorization":akasa_token})
                akasa_seat_map = akasa_seat_map.json()
                seat_list.append(akasa_seat_map)
            # return Response(seat_list)

            
            # with open("static/flight/airport_list.json", "r") as f:
            #     airport = json.loads(f.read())
            # for i in akasaa_data['data']['results']:
            #     for a in i['trips']: 
            #         for b in a['journeysAvailableByMarket'].values():
            #             for c in b:
            #                 for d in c['segments']:
            #                     for e in d['legs']:
            #                         origin = e['designator']['origin']
            #                         destination = e['designator']['destination']
            #                         for i in airport:
            #                             if(origin in i['code']):
            #                                 e['designator']['origin'] = i['name']
            #                             if(destination in i['code']):
            #                                 e['designator']['destination'] = i['name']
            
                  
            context= {
                "key" : key,
                "promo" : promo,
                "skey" : skey,
                "radio1":radio1, 
                "Person":Person,
                "akasaa_data":akasaa_data,
                "akasa_token":akasa_token,
                "akasa_ssr":json.dumps(akasa_ssr),
                # "pricelist":pricelist,
                "rtype":rtype,
                "apiamount":apiamount,
                "adult":adult,
                "child":child,
                "infant":infant,
                "passengerkey":passengerkey,
                "seat": json.dumps(seat_list),
                "l":l
                }
            # return Response(context)
            return render(request, "online_savaari/akasa_review.html", context)

        if(rtype == "series"):
            # if (reviewId != None):
            #     reviewId = int(reviewId)
            search_series = {
                "origin":fromCityOrAirport,
                "destination":toCityOrAirport,
                "departure_date":travelDateseries,
                "adult":adult,
                "child":child,
                "infant":infant,
                "airline_code":""
            }
            seriess_data = series_data(series_url, '/search',search_series,header={"api-key":api_key,"Authorization":token, "Content-Type":"application/json"})
            search_sdata=seriess_data.json()
            # return Response(reviewId)
            result = [d for d in search_sdata['data'] if d['ticket_id'] == reviewId]
            apiamount = result[0]['price']
            apiamount = float(apiamount)
            d_list = [toCityOrAirport, fromCityOrAirport]
            smarkup_none = list(SeriesMarkup.objects.filter(airport_name=None).values())
            smarkup_with_airport = []
            for j in d_list:
                if SeriesMarkup.objects.filter(airport_name=j).exists():
                    smark = list(SeriesMarkup.objects.filter(airport_name=j).values())
                    smarkup_with_airport.append(smark)
                    break
            
            if smarkup_with_airport:
                series_mark_up = smarkup_with_airport[0]
                start_date = series_mark_up[0]['start_date']
                end_date = series_mark_up[0]['end_date']
                mark_type = series_mark_up[0]['amount_type']
                markup_amount = series_mark_up[0]["amount"]
                temp = []
                for x in result:
                    add = True
                    departure_date = x['departure_date']
                    d_date = departure_date.split("/")
                    yy = int(d_date[0])
                    mm = int(d_date[1])
                    dd = int(d_date[2])
                    departure_date = date(yy,mm,dd)
                    if ((start_date <= departure_date) and (end_date >= departure_date)):
                        tf = x['price']
                        if (mark_type == "fixed"):
                            tf= float(tf) + float(markup_amount)
                            x['price'] = tf*int(Person)
                            x['markup'] = float(markup_amount)
                        if (mark_type == "percent"):
                            addedmarkup = tf*(markup_amount/100)
                            tf= percentage(float(tf), float(markup_amount))
                            x['price'] = tf
                            x['markup'] = addedmarkup
                        # start_date += delta
                    temp.append(x)

                search_sdata['data'] = temp
            elif smarkup_none:
                series_mark_up = smarkup_none[0]
                start_date = smarkup_none[0]['start_date']
                end_date = smarkup_none[0]['end_date']
                mark_type = smarkup_none[0]['amount_type']
                markup_amount = smarkup_none[0]["amount"]
                temp = []
                for x in result:
                    add = True
                    departure_date = x['departure_date']
                    d_date = departure_date.split("/")
                    yy = int(d_date[0])
                    mm = int(d_date[1])
                    dd = int(d_date[2])
                    departure_date = date(yy,mm,dd)
                    if ((start_date <= departure_date) and (end_date >= departure_date)):
                        tf = x['price']
                        if (mark_type == "fixed"):
                            tf= float(tf) + float(markup_amount)
                            x['price'] = tf
                            x['markup'] = float(markup_amount)
                        if (mark_type == "percent"):
                            addedmarkup = tf*(markup_amount/100)
                            tf= percentage(float(tf), float(markup_amount))
                            x['price'] = tf
                            x['markup'] = addedmarkup
                        # start_date += delta
                    temp.append(x)

                search_sdata['data'] = temp
            context= {
                "promo":promo, 
                "radio1":radio1, 
                "Person":Person,
                "result":result,
                "jsonresult": json.dumps(result),
                "token":token,
                "adult":adult,
                "child":child,
                "infant":infant,
                "rtype":rtype,
                "gstdetail": gstdetail,
                "apiamount": apiamount,
                "num": num,
            }
        if(rtype == "normal"):
            key = request.GET.get('key')
            

            search_request = {
                    "priceIds" : [key]
                }           
            result = flight_data(api_url, apikey, '/fms/v1/review',search_request)
            data=result.json()
            print(data)
            apiamount=data['totalPriceInfo']['totalFareDetail']['fC']['TF']
            apiamount = float(apiamount)

        
            with open("static/flight/airlines.json", "r") as f:
                airline = json.loads(f.read())

            if request.user:
                grp = find_group(request.user)
            else:
                grp = 'Customer'
            
            mtype = ""
            if data["searchQuery"]["isDomestic"]:
                mtype= "domestic"
            else:
                mtype="international"
            
            markup_none = list(Markup.objects.filter(airline_type=None, user_type=grp,markup_type=mtype).values())
            markup_with_airport = []
            for j in data['tripInfos'][0]['sI']:
                if Markup.objects.filter(airline_type=j['fD']['aI']['name'], user_type=grp,markup_type=mtype).exists():
                    mark = list(Markup.objects.filter(airport_name=j).values())
                    markup_with_airport.append(mark)
                    break
            
            if markup_with_airport:
                mark_up = markup_with_airport
                mark_type = mark_up[0]['amount_type']
                markup_amount = mark_up[0]["amount"]
                temp = []
                tf = data['totalPriceInfo']['totalFareDetail']['fC']['TF']
                if mark_type == 'fixed':
                    tf= float(tf) + float(markup_amount)*int(Person)
                    data['totalPriceInfo']['totalFareDetail']['fC']['TF'] = tf
                if mark_type == 'percent':
                    tf = percentage(float(tf), float(markup_amount)*int(Person))
                    data['totalPriceInfo']['totalFareDetail']['fC']['TF'] = tf

            elif markup_none:
                mark_up = markup_none
                mark_type = mark_up[0]['amount_type']
                markup_amount = mark_up[0]["amount"]
                temp = []
                tf = data['totalPriceInfo']['totalFareDetail']['fC']['TF']
                if mark_type == 'fixed':
                    tf= float(tf) + float(markup_amount)*int(Person)
                    data['totalPriceInfo']['totalFareDetail']['fC']['TF'] = tf
                if mark_type == 'percent':
                    tf = percentage(float(tf), float(markup_amount)*int(Person))
                    data['totalPriceInfo']['totalFareDetail']['fC']['TF'] = tf


            context= {
                "key" : key,
                "promo" : promo,
                "radio1":radio1, 
                "Person":Person,
                "data":data,
                "rtype":rtype,
                "gstdetail": gstdetail,
                "apiamount":apiamount,
                "num":num,
                "jsondata":json.dumps(data)
            } 
    if (radio1 == "two-way"):
        num = 1
        if((toCityOrAirport in l) and (fromCityOrAirport in l)):
            num = 2
            search_request = {
                    "priceIds" : [key,key1]
                }
        if((toCityOrAirport in k) or (fromCityOrAirport in k)):
            search_request = {
                    "priceIds" : [key]
                }
        result = flight_data(api_url, apikey, '/fms/v1/review',search_request)
        data=result.json()
        errs = False
        apiamount = 0
        if('errors' in data):
            for x in data['errors']:
                errs = x['message']
                print(errs)
        else:        
            apiamount= data['totalPriceInfo']['totalFareDetail']['fC']['TF']

        
            with open("static/flight/airlines.json", "r") as f:
                airline = json.loads(f.read())
                    
            if request.user:
                grp = find_group(request.user)
            else:
                grp = 'Customer'
            
            mtype = ""
            if data["searchQuery"]["isDomestic"]:
                mtype= "domestic"
            else:
                mtype="international"
            
            markup_none = list(Markup.objects.filter(airline_type=None, user_type=grp,markup_type=mtype).values())
            markup_with_airport = []
            for j in data['tripInfos'][0]['sI']:
                if Markup.objects.filter(airline_type=j['fD']['aI']['name'], user_type=grp,markup_type=mtype).exists():
                    mark = list(Markup.objects.filter(airline_type=j['fD']['aI']['name'],user_type=grp,markup_type=mtype).values())
                    markup_with_airport.append(mark)
                    break
            
            if markup_with_airport:
                mark_up = markup_with_airport
                mark_type = mark_up[0][0]['amount_type']
                markup_amount = mark_up[0][0]["amount"]
                temp = []
                tf = data['totalPriceInfo']['totalFareDetail']['fC']['TF']
                if mark_type == 'fixed':
                    tf= float(tf) + float(markup_amount)*num*int(Person)
                    data['totalPriceInfo']['totalFareDetail']['fC']['TF'] = tf
                if mark_type == 'percent':
                    tf = percentage(float(tf), float(markup_amount)*num*int(Person))
                    data['totalPriceInfo']['totalFareDetail']['fC']['TF'] = tf

            elif markup_none:
                mark_up = markup_none
                mark_type = mark_up[0]['amount_type']
                markup_amount = mark_up[0]["amount"]
                temp = []
                tf = data['totalPriceInfo']['totalFareDetail']['fC']['TF']
                if mark_type == 'fixed':
                    tf= float(tf) + float(markup_amount)*num*int(Person)
                    data['totalPriceInfo']['totalFareDetail']['fC']['TF'] = tf
                if mark_type == 'percent':
                    tf = percentage(float(tf), float(markup_amount)*num*int(Person))
                    data['totalPriceInfo']['totalFareDetail']['fC']['TF'] = tf

        context= {
            "key" : key,
            "promo" : promo,
            "radio1":radio1, 
            "Person":Person,
            "data":data,
            "rtype":rtype,
            "errs":errs,
            "apiamount":apiamount,
            "gstdetail": gstdetail,
            "num": num,
            "jsondata":json.dumps(data)
            }

    if (radio1 == "multi-way"):
        num = 1
        print((toCityOrAirport in k) or (fromCityOrAirport in k))
        print((toCityOrAirport in l) and (fromCityOrAirport in l))
        print((toCityOrAirport in l) and (fromCityOrAirport in l))
        search_request = {
            "priceIds" : [key]
        }
        if((toCityOrAirport in k) or (fromCityOrAirport in k)):
            print("enter")
            search_request = {
                    "priceIds" : [key]
                }
        if((toCityOrAirport in l) and (fromCityOrAirport in l)):
            print("key1")
            num = 2
            search_request = {
                    "priceIds" : [key,key1]
                }
            if (key2):
                num = 3
                search_request = {
                        "priceIds" : [key,key1,key2]
                    }
            if (key3):
                num = 4
                search_request = {
                        "priceIds" : [key,key1,key2,key3]
                    }
            if (key4):
                num = 5
                search_request = {
                        "priceIds" : [key,key1,key2,key3,key4]
                    }
        result = flight_data(api_url, apikey, '/fms/v1/review',search_request)
        data=result.json()
        errs = None
        if('errors' in data):
            for x in data['errors']:
                errs = x['message']
                print(errs)
        else:  
            apiamount=data['totalPriceInfo']['totalFareDetail']['fC']['TF']

        
            with open("static/flight/airlines.json", "r") as f:
                airline = json.loads(f.read())
                    
            if request.user:
                grp = find_group(request.user)
            else:
                grp = 'Customer'
            
            mtype = ""
            if data["searchQuery"]["isDomestic"]:
                mtype= "domestic"
            else:
                mtype="international"
            
            markup_none = list(Markup.objects.filter(airline_type=None, user_type=grp,markup_type=mtype).values())
            markup_with_airport = []
            for j in data['tripInfos'][0]['sI']:
                if Markup.objects.filter(airline_type=j['fD']['aI']['name'], user_type=grp,markup_type=mtype).exists():
                    mark = list(Markup.objects.filter(airline_type=j,user_type=grp,markup_type=mtype).values())
                    markup_with_airport.append(mark)
                    break
            
            if markup_with_airport:
                mark_up = markup_with_airport
                mark_type = mark_up[0]['amount_type']
                markup_amount = mark_up[0]["amount"]
                temp = []
                tf = data['totalPriceInfo']['totalFareDetail']['fC']['TF']
                if mark_type == 'fixed':
                    tf= float(tf) + float(markup_amount)*num*int(Person)
                    data['totalPriceInfo']['totalFareDetail']['fC']['TF'] = tf
                if mark_type == 'percent':
                    tf = percentage(float(tf), float(markup_amount)*num*int(Person))
                    data['totalPriceInfo']['totalFareDetail']['fC']['TF'] = tf

            elif markup_none:
                mark_up = markup_none
                mark_type = mark_up[0]['amount_type']
                markup_amount = mark_up[0]["amount"]
                temp = []
                tf = data['totalPriceInfo']['totalFareDetail']['fC']['TF']
                if mark_type == 'fixed':
                    tf= float(tf) + float(markup_amount)*num*int(Person)
                    data['totalPriceInfo']['totalFareDetail']['fC']['TF'] = tf
                if mark_type == 'percent':
                    tf = percentage(float(tf), float(markup_amount)*num*int(Person))
                    data['totalPriceInfo']['totalFareDetail']['fC']['TF'] = tf

        context= {
            "key" : key,
            "promo" : promo,
            "radio1":radio1, 
            "Person":Person,
            "data":data,
            "rtype":rtype,
            "errs":errs,
            "apiamount":apiamount,
            "gstdetail": gstdetail,
            "num": num,
            "jsondata":json.dumps(oo)
        }
    
    return render(request, "online_savaari/details.html", context)


@api_view(["GET", "POST"])
def select_gds_seat(request):
    gds_seat_data = request.session.get('gds_seat_datas')
    serialized_data = json.loads(gds_seat_data)
    return Response(serialized_data)


@api_view(["GET","POST"])
def select_seat(request):
    
    bookingId = request.GET.get('bookingId')
    
    search_request = {
        "bookingId" : [bookingId]
    }
    print(".................................")
    result = flight_data(api_url, apikey, '/fms/v1/seat',search_request)
    result = result.json()
    data = json.dumps(result)
    with open("PUBLISHED_seat.json", "w") as file:
        file.write(data)
        file.close()
    return JsonResponse(result)

import re
def change_date_format(dt):
        return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\2-\\3-\\1', dt)

@api_view(["GET","POST"])
def instant_booking(request):

    datatest = request.GET.get('datatest')
    # newdata = json.loads(datatest)
    # return JsonResponse(newdata, safe=False)

    login_user = request.user

    if not login_user.is_authenticated:
        return JsonResponse({'status':False, 'msg':"User is not logged In!"})
    # return JsonResponse(request.GET, safe=False)
    bookingId = request.GET.get('bookingId')
    key = request.GET.get('key')
    Person = request.GET.get('Person')
    amount = request.GET.get('amount')
    meal_code=request.GET.get('meal_code', None)
    bagg_code=request.GET.get('bagg_code', None)
    akasa_token=request.GET.get('akasa_token', None)
    insurance_checked=request.GET.get('insurance_checked', None)
    bid=request.GET.get('bid', None)
    title=request.GET.get('title', None)
    token=request.GET.get('token', None)
    rtype=request.GET.get('rtype', None)
    departure_date=request.GET.get('departure_date', None)
    arrival_date=request.GET.get('arrival_date', None)
    flight_num=request.GET.get('flight_num', None)
    first_name=request.GET.get('first_name',None)
    last_name=request.GET.get('last_name',None)
    email=request.GET.get('email', None)
    origin=request.GET.get('origin', None)
    addon = request.GET.get('addon', None)  
    if rtype == 'normal':
        if (addon != None):
            addon = json.loads(addon.replace("\'", "\""))
            print(addon)
        bagaddon = request.GET.get('bagaddon', None)
        if (bagaddon != None):
            bagaddon = json.loads(bagaddon.replace("\'", "\""))
            print(bagaddon)
        seataddon = request.GET.get('seataddon', None)  
        if (seataddon != None): 
            seataddon = json.loads(seataddon.replace("\'", "\""))   
            print(seataddon)
    mobile=request.GET.get('mobile', None)
    destination=request.GET.get('destination', None)
    meal=request.GET.get('meal', None)
    baggage=request.GET.get('baggage', None)
    seat_no=request.GET.get('seat_no', None)
    panno=request.GET.get('panno', None)
    passport_no=request.GET.get('passport_no', None)
    flightcode=request.GET.get('flightcode', None)
    flightno=request.GET.get('flightno', None)
    cabinClass=request.GET.get('cabinClass', None)
    pp=request.GET.get('pp', None)
    date_of_birth = request.GET.get('date_of_birth', "01-01-1950")
    passport_no = request.GET.get('date_of_birth', None)
    expiry_date = request.GET.get('expiry_date', None)
    issue_date = request.GET.get('issue_date', None)
    src = request.GET.get('src', None)
    dest = request.GET.get('dest', None)
    apiamount = request.GET.get('apiamount', None)
    token = request.GET.get('token', None)
    ticketid = request.GET.get('ticketid', None)
    adult = request.GET.get('adult', None)
    child = request.GET.get('child', None)
    infant = request.GET.get('infant', None)
    gstno = request.GET.get('gstno', None)
    company_name = request.GET.get('company_name', None)
    gst_mobile = request.GET.get('gst_mobile', None)
    gst_email = request.GET.get('gst_email', None)
    address = request.GET.get('address', None)
    gstno_our = '27AADCO8306K1Z7'
    company_name_our = 'ONLINE SAVAARI PRIVATE LIMITED'
    gst_mobile_our = '9073494362'
    gst_email_our = 'onlinesavaari@gmail.com'
    address_our = '3RD FLOOR, OFFICE NO. A302, RANGE HEIGHTS, LINK ROAD, BEHRAM BUG ROAD, Oshiwara, SARVODYA NAGAR, Mumbai, Mumbai Suburban, Maharashtra, 400102'
    print("ssr", bid, bagg_code,meal_code)
    insurance = None
    # return JsonResponse(seataddon['ADULT_1'], safe=False)
    # Person = int(Person)
    if rtype == "spicejet":
        spice_token = request.GET.get('spice_token', None)
        spice_request = """<?xml version="1.0" encoding="UTF-8"?> <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"> <s:Header> <h:ContractVersion xmlns:h="http://schemas.navitaire.com/WebServices">420</h:ContractVersion> <h:EnableExceptionStackTrace xmlns:h="http://schemas.navitaire.com/WebServices">false</h:EnableExceptionStackTrace> <h:MessageContractVersion xmlns:h="http://schemas.navitaire.com/WebServices" xmlns:i="http://www.w3.org/2001/XMLSchema-instance" i:nil="true"/> <h:Signature xmlns:h="http://schemas.navitaire.com/WebServices">"""+spice_token+"""</h:Signature> </s:Header> <s:Body> <BookingCommitRequest xmlns="http://schemas.navitaire.com/WebServices/ServiceContracts/BookingService"> <BookingCommitRequestData xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Booking"> <State>New</State> <RecordLocator i:nil="true"/> <CurrencyCode>INR</CurrencyCode> <PaxCount>1</PaxCount> <SystemCode i:nil="true"/> <BookingID>0</BookingID> <BookingParentID>0</BookingParentID> <ParentRecordLocator i:nil="true"/> <BookingChangeCode i:nil="true"/> <GroupName i:nil="true"/> <SourcePOS xmlns:a="http://schemas.navitaire.com/WebServices/DataContracts/Common"> <a:State>New</a:State> <a:AgentCode>AG</a:AgentCode> <a:OrganizationCode>APITESTID</a:OrganizationCode> <a:DomainCode>WWW</a:DomainCode> <a:LocationCode i:nil="true"/> </SourcePOS> <BookingHold i:nil="true"/> <ReceivedBy> <State xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Common">New</State> <ReceivedBy>APITESTID</ReceivedBy> <ReceivedReference i:nil="true"/> <ReferralCode i:nil="true"/> <LatestReceivedBy i:nil="true"/> <LatestReceivedReference i:nil="true"/> </ReceivedBy> <RecordLocators i:nil="true" xmlns:a="http://schemas.navitaire.com/WebServices/DataContracts/Common"/> <Passengers i:nil="true"/> <BookingComments i:nil="true"/> <BookingContacts> <BookingContact> <State xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Common">New</State> <TypeCode>P</TypeCode> <Names> <BookingName> <State xmlns="http://schemas.navitaire.com/WebServices/DataContracts/Common">New</State> <FirstName>THREE</FirstName> <MiddleName i:nil="true"/> <LastName>TEST</LastName> <Suffix i:nil="true"/> <Title>MR</Title> </BookingName> </Names> <EmailAddress>TEST@TEST.COM</EmailAddress> <HomePhone>+919090909090</HomePhone> <WorkPhone i:nil="true"/> <OtherPhone i:nil="true"/> <Fax i:nil="true"/> <CompanyName>Online Savaari Pvt Ltd</CompanyName> <AddressLine1>A</AddressLine1> <AddressLine2>B</AddressLine2> <AddressLine3 i:nil="true"/> <City>GGN</City> <ProvinceState i:nil="true"/> <PostalCode i:nil="true"/> <CountryCode>IN</CountryCode> <CultureCode>en-GB</CultureCode> <DistributionOption>Email</DistributionOption> <CustomerNumber i:nil="true"/> <NotificationPreference>None</NotificationPreference> <SourceOrganization>APITESTID</SourceOrganization> </BookingContact> </BookingContacts> <NumericRecordLocator i:nil="true"/> <RestrictionOverride>false</RestrictionOverride> <ChangeHoldDateTime>false</ChangeHoldDateTime> <WaiveNameChangeFee>false</WaiveNameChangeFee> <WaivePenaltyFee>false</WaivePenaltyFee> <WaiveSpoilageFee>false</WaiveSpoilageFee> <DistributeToContacts>true</DistributeToContacts> <SourceBookingPOS i:nil="true" xmlns:a="http://schemas.navitaire.com/WebServices/DataContracts/Common"/> </BookingCommitRequestData> </BookingCommitRequest> </s:Body> </s:Envelope>"""
        spice_booking = spice_data(spice_url,'/Bookingmanager.svc',spice_request,spice_header={"Content-Type":"text/xml; charset=utf-8", "SOAPAction":"http://schemas.navitaire.com/WebServices/IBookingManager/BookingCommit","Accept-Encoding":"gzip, deflate"})  
        with open("booking.txt", "w") as file:
            file.write(str(spice_booking))
            file.close()
        spice_booking = xmltodict.parse(spice_booking, attr_prefix='')
        spice_booking = json.dumps(spice_booking)
        spice_booking = json.loads(spice_booking)
        with open("inp_booking.txt", "w") as file:
            file.write(str(spice_request))
            file.close()
        spice_request= """<?xml version="1.0" encoding="UTF-8"?> <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"> <s:Header> <h:ContractVersion xmlns:h="http://schemas.navitaire.com/WebServices">420</h:ContractVersion> <h:EnableExceptionStackTrace xmlns:h="http://schemas.navitaire.com/WebServices">false</h:EnableExceptionStackTrace> <h:MessageContractVersion xmlns:h="http://schemas.navitaire.com/WebServices" xmlns:i="http://www.w3.org/2001/XMLSchema-instance" i:nil="true"/> <h:Signature xmlns:h="http://schemas.navitaire.com/WebServices">"""+spice_token+"""</h:Signature> </s:Header> <s:Body> <LogoutRequest xmlns="http://schemas.navitaire.com/WebServices/ServiceContracts/SessionService"/> </s:Body> </s:Envelope>"""
        spice_logout = spice_data(spice_url,'/Sessionmanager.svc',spice_request,spice_header={"Content-Type":"text/xml; charset=utf-8", "SOAPAction":"http://schemas.navitaire.com/WebServices/ISessionManager/Logout","Accept-Encoding":"gzip, deflate"})
        with open("logout.txt", "w") as file:
            file.write(str(spice_logout))
            file.close()
        data_dict = xmltodict.parse(spice_logout, attr_prefix='')
        data_dict = json.dumps(data_dict)
        data_dict = json.loads(data_dict)
        with open("inp_logout.txt", "w") as file:
            file.write(str(spice_request))
            file.close()          
        return JsonResponse(spice_booking, safe=False)
    if(rtype == "akasa"):
        # return JsonResponse({'status': 'done'})
        null= None
        false = False
        print(akasa_token, "test")
        akasa_request ={"receivedBy":null,"restrictionOverride":false,"hold":null,"notifyContacts":false,"comments":null,"contactTypesToNotify":null}
        akasaa_pay = akasa_data(akasa_url, '/api/nsk/v3/booking', akasa_request,akasa_header={"Authorization":akasa_token})
        return HttpResponse(akasaa_pay)
    if(token != "None") and rtype == "series":
        arrival_date = arrival_date.replace("/","-")
        departure_date = departure_date.replace("/","-")
    name= first_name +" "+ last_name
    insurance_amount = 135
    if(insurance_checked != "None"):
        cust1=Insurance.objects.create(name=name,mobileno=mobile,emailaddress=email,totalcharges=insurance_amount,arrival_date=arrival_date,departure_date=departure_date)
        
        insurance = Insurance.objects.latest('id')
        a_list = arrival_date.split("-")
        ayy = int(a_list[0])
        amm = int(a_list[1])
        add = int(a_list[2])
        a1 = date(ayy, amm, add)
        d_list = departure_date.split("-")
        dyy = int(d_list[0])
        dmm = int(d_list[1])
        ddd = int(d_list[2])
        d1 = date(dyy, dmm, ddd)
        delta = a1 - d1
        totaldays = str(delta.days+1)
        arrivaldate = str(insurance.arrival_date)
        departuredate = str(insurance.departure_date)
        departuredate = change_date_format(departuredate)
        arrivaldate = change_date_format(arrivaldate)
        tree = ET.parse('flight/insurance.xml')
        myroot = tree.getroot()


        for temp in myroot.iter('reference'):
            temp.text = insurance.reference
        for temp in myroot.iter('departuredate'):
            temp.text = departuredate
        for temp in myroot.iter('arrivaldate'):
            temp.text = arrivaldate
        for temp in myroot.iter('mobileno'):
            temp.text = insurance.mobileno
        for temp in myroot.iter('emailaddress'):
            temp.text = insurance.emailaddress
        for temp in myroot.iter('name'):
            temp.text = insurance.name
        for temp in myroot.iter('days'):
            temp.text = totaldays

        tree.write('flight/insurance.xml')

    # s = []
    # s.append({"key": bid,"code": seat_no})

    if(token != "None") and rtype == 'series':
        adult_info = []
        child_info = []
        infant_info = []
        for i in range(int(Person)):
            if i == 0:
                newperson = {
                "title": request.GET.get(f'title', None) + ".",
                "first_name": request.GET.get(f'first_name',None),
                "last_name": request.GET.get(f'last_name',None),
                }
                adult_info.append(newperson)
            else:
                newperson = {
                "title": request.GET.get(f'title{j}', None) + ".",
                "first_name": request.GET.get(f'first_name{j}',None),
                "last_name": request.GET.get(f'last_name{j}',None),
                }
                if(request.GET.get(f'pp{j}') == 'CHILD'):
                    child_info.append(newperson)
                elif (request.GET.get(f'pp{j}') == 'INFANT'):
                    infant_info.append(newperson)
                else:
                    adult_info.append(newperson)


        search_series = {
            "ticket_id": ticketid,
            "total_pax": Person,
            "adult":adult,
            "child":child,
            "infant":infant,
            "adult_info":adult_info,
            "child_info":child_info,
            "infant_info":infant_info,
        }
    else:
        meal = []   
        bag = []
        seat = []   
        for k, v in addon.items():  
            print(v)    
            meal.append({"key":v['bid'],"code":v['code']})  
        for k, v in bagaddon.items():   
            print(v)    
            bag.append({"key":v['bid'],"code":v['code']})
        seat_adult = []
        for k, v in seataddon['ADULT_1'].items():
            seat_adult.append({"key": v['bid'], "code": v['code']})

        t = [
             {
              "ti": title,
              "fN": first_name,
              "lN": last_name,
              "pt": pp,
              "dob": date_of_birth,
              "pNum" :passport_no,
              "eD" : expiry_date,
              "pid" : issue_date,
              "ssrMealInfos": meal, 
              "ssrBaggageInfos": bag,
              "ssrSeatInfos": seat_adult,
            }
        ]
        num_adult = 1
        num_child = 0
        child_title = {
            "Master": "Master",
            "Miss": "Ms",
            "Mr": "Mr",
            "Ms": "Ms",
            "Mrs": "Mrs",
        }
        for i in range(int(Person)):
            if i > 0:
                num = 0
                j = i + 1
                pt = request.GET.get(f'pp{j}')
                title = request.GET.get(f'title{j}', "Mr")
                if(pt == 'CHILD'):
                    num_child += 1
                    num = num_child
                    dob = '01-05-2012'
                    title = child_title[request.GET.get(f'title{j}', "Mr")]
                elif (pt == 'INFANT'):
                    dob = request.GET.get(f'dob{j}', None)
                else:
                    num_adult += 1
                    num = num_adult
                    dob = "01-01-1950"
                if (pt != "INFANT"):
                    seat = []
                    for k, v in seataddon[f'{pt}_{num}'].items():
                        seat.append({"key": v['bid'], "code": v['code']})
                t.append({
                    "ti": title,
                    "fN": request.GET.get(f'first_name{j}',None),
                    "lN": request.GET.get(f'last_name{j}',None),
                    "pt": request.GET.get(f'pp{j}', None),
                    "dob": dob,
                    "pNum" :passport_no,
                    "eD" : expiry_date,
                    "pid" : issue_date,
                    "ssrMealInfos": meal,
                    "ssrBaggageInfos": bag,
                    "ssrSeatInfos": seat,

                })

        
        if(gstno == ""):
            print("ssr", bid, bagg_code,meal_code)
            search_request ={
              "bookingId": bookingId,

              "paymentInfos": [
                {
                  "amount": apiamount
                  
                }
              ],
              "travellerInfo": t,

                  "gstInfo": {
                    "gstNumber": gstno_our,
                    "email": gst_email_our,
                    "registeredName": company_name_our,
                    "mobile": gst_mobile_our,
                    "address":address_our
                },

                "deliveryInfo": {
                    "emails": [
                      email
                    ],
                    "contacts": [
                      mobile
                    ]
                }
            } 
        else:
            print("ssr", bid, bagg_code,meal_code)
            search_request ={
          "bookingId": bookingId,

          "paymentInfos": [
            {
              "amount": apiamount
              
            }
          ],
          "travellerInfo": t,
              "gstInfo": {
                "gstNumber": gstno,
                "email": gst_email,
                "registeredName": company_name,
                "mobile": gst_mobile,
                "address":address
            },

            "deliveryInfo": {
                "emails": [
                  email
                ],
                "contacts": [
                  mobile
                ]
            }
        } 
        #   "bookingId": bookingId,
        #   "paymentInfos": [
        #     {
        #       "amount": apiamount
        #     }
        #   ],
        #   "travellerInfo": t,
        #   "deliveryInfo": {
        #     "emails": [
        #       email
        #     ],
        #     "contacts": [
        #       mobile
        #     ]
        #   }
        # } 

    if(token != "None") and rtype == 'series':
        seriess_data = series_data(series_url, '/book',search_series,header={"api-key":api_key,"Authorization":token, "Content-Type":"application/json"})
        search_sdata=seriess_data.json()
        # return Response(search_sdata)
        sbookindId = search_sdata['booking_id']
        context= {
            "search_sdata":search_sdata,
            "Person":Person,
            "bookingId":bookingId,
            "cabinClass":cabinClass,
            "apiamount" : apiamount,
            "amount" : amount,
            "src": src,
            "dest": dest,
            "sbookindId": sbookindId,
            "token": token,
            "insurance": insurance,
            "email": email,
            "mobile": mobile,
            "insurance_checked": insurance_checked,
            "gstno" : gstno,
            "company_name" : company_name,
            "gst_email" : gst_email,
            "gst_mobile" : gst_mobile,
            "address" : address,
        }
        return JsonResponse(search_sdata)
    else:
        # return JsonResponse(search_request)
        result = flight_data(api_url, apikey, '/oms/v1/air/book',search_request)
        data=result.json()
        print(data)        
        context= {
            "data":data,
            "key" : key,
            "Person":Person,
            "bookingId":bookingId,
            "cabinClass":cabinClass,
            "apiamount" : apiamount,
            "amount" : amount,
            "src": src,
            "dest": dest,
            "rtype": rtype,
            "arrival_date": arrival_date,
            "flight_num": flight_num,
            "insurance": insurance,
            "insurance_checked": insurance_checked,
            "gstno" : gstno,
            "company_name" : company_name,
            "gst_email" : gst_email,
            "gst_mobile" : gst_mobile,
            "address" : address,
        }
        return JsonResponse(data)
    # return render(request, "online_savaari/success.html", context)


def sendEmail(smtpHost, smtpPort, mailUname, mailPwd, fromEmail, mailSubject, mailContentHtml, recepientsMailList, attachmentFpaths):
     # create message object
    msg = MIMEMultipart()
    msg['From'] = fromEmail
    msg['To'] = ','.join(recepientsMailList)
    msg['Subject'] = mailSubject
    # msg.attach(MIMEText(mailContentText, 'plain'))
    msg.attach(MIMEText(mailContentHtml, 'html'))

    # create file attachments
    for aPath in attachmentFpaths:
     # check if file exists
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(aPath, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(aPath)))
        msg.attach(part)

    # Send message object as email using smptplib
    s = smtplib.SMTP(smtpHost, smtpPort)
    s.starttls()
    s.login(mailUname, mailPwd)
    msgText = msg.as_string()
    sendErrs = s.sendmail(fromEmail, recepientsMailList, msgText)
    s.quit()

    # check if errors occured and handle them accordingly
    if not len(sendErrs.keys()) == 0:
        raise Exception("Errors occurred while sending email", sendErrs)

# def readxmlins():
#     with open("flight/insurance.xml") as xml_file:
#         xml_policy = xml_file.read() 
#     data = encrypt(xml_policy)
#     result = insurance(url_inc,data,Ref)
#     result = result.text
#     result = xmltodict.parse(result)
#     return result


@api_view(["GET","POST"])
def get_details(request):
    # return JsonResponse(json.loads(request.GET.get('insurance_data').replace("\'", "\"")), safe=False)
    login_user = request.user

    if not login_user.is_authenticated:
        return JsonResponse({'status':False, 'msg':"User is not logged In!"})
    print(request.POST)
    insurance_data = request.GET.get('insurance_data', None)
    booking_id = request.GET.get('bookingId')
    book_status = request.GET.get('data[status][success]',None)
    err_code = request.GET.get('data[errors][0][errCode]',None)
    err_msg = request.GET.get('data[errors][0][message]',None)
    transaction_id = request.GET.get('transaction_id',None)
    key = request.GET.get('key')
    Person = request.GET.get('Person')
    date_of_birth = request.GET.get('date_of_birth', "1950-01-01")
    bid = request.GET.get('id')
    amount = request.GET.get('amount')
    cabinClass = request.GET.get('cabinClass')
    rtype = request.GET.get('rtype', None)
    arrival_date = request.GET.get('arrival_date', None)
    departure_date = request.GET.get('departure_date', None)
    if(arrival_date != 'None'):
        arrival_date = arrival_date.replace("/","-")
        departure_date = departure_date.replace("/","-")
    flight_num = request.GET.get('flight_num', None)
    token = request.GET.get('token', None)
    src = request.GET.get('src', None)
    dest = request.GET.get('dest', None)
    sbookindId = request.GET.get('sbookindId', None)
    email = request.GET.get('email', None)
    mobile = request.GET.get('mobile', None)
    gstno = request.GET.get('gstno', None)
    company_name = request.GET.get('company_name', None)
    gst_mobile = request.GET.get('gst_mobile', None)
    gst_email = request.GET.get('gst_email', None)
    address = request.GET.get('address', None)
    akasa_token = request.GET.get('akasa_token', None)
    booking_id = request.GET.get("bookingId")
    arrival_date = request.GET.get("arrival_date")
    departure_date = request.GET.get("departure_date")


    if(rtype == "akasa" ):
        akasa_request = akasa_token
        print(akasa_request)
        print(akasa_request)
        akasaa_pay = akasa_details(akasa_url, '/api/nsk/v1/booking', akasa_request,akasa_header={"Authorization":akasa_token})
        adata = akasaa_pay.json()
        # return Response(akasaa_pay.json())
        print(akasaa_pay, akasa_token)
        airline_name= "Akasa Air"
        src = adata['data']['journeys'][0]['designator']['origin']
        origin_airport = adata['data']['journeys'][0]['designator']['origin']
        dest = adata['data']['journeys'][0]['designator']['destination']
        destination_airport = adata['data']['journeys'][0]['designator']['destination']
        flight_code = adata['data']['journeys'][0]['segments'][0]['identifier']['carrierCode']
        flight_number = adata['data']['journeys'][0]['segments'][0]['identifier']['identifier']
        departure_datetime = adata['data']['journeys'][0]['designator']['departure']
        datetime =  departure_datetime.split("T")
        departure_time = datetime[1]
        departure_date= datetime[0]
        arrival_datetime = adata['data']['journeys'][0]['designator']['arrival']
        datetime =  arrival_datetime.split("T")
        arrival_time = datetime[1]
        arrival_date= datetime[0]
        duration= (dt.strptime(arrival_time, '%H:%M:%S') - dt.strptime(departure_time, '%H:%M:%S')).total_seconds() // 60
        stop = 0
        flight_class = cabinClass


        base_price = adata['data']['breakdown']['journeyTotals']['totalAmount']
        total_fare = adata['data']['breakdown']['totalAmount']
        taf = adata['data']['breakdown']['journeyTotals']['totalTax']
        paid_amount = amount
        # flight_status = data['order']['status']
        osn_id = randint(1000000000, 9999999999)
        osn_id = str(osn_id)
        os_id = 'OS'+osn_id
        booking_id = adata['data']['bookingKey']
        for i, v in adata['data']['passengers'].items():
            print(dict(adata['data']['passengers'][i]))
            pnr = adata['data']['recordLocator']
            baggage = None
            meal = None
            seat = None

            title = v['name']['title']
            first_name = v['name']['first']
            last_name = v['name']['last']
            date_of_birth = None
            passenger_type = v['passengerTypeCode']
            # os_id = Passenger.objects.latest('id')
            # os_id = os_id.os_bookingId
            # print(os_id,"os_id")
            # os_id=int(os_id[2:])
            # os_id+=1
            # os_id=str(os_id)
            # os_id="OS"+os_id
            # print(os_id)

            if(book_status == 'false'):
                flight_status = 'PENDING'
            else:
                flight_status = 'SUCCESSFUL'

            cust1=Passenger.objects.create(bookingId=booking_id,transaction_id=transaction_id,err_code=err_code,err_desc=err_msg,os_bookingId=os_id,user=login_user,flight_status=flight_status,gstno=gstno,company_name=company_name,gst_email=gst_email,gst_mobile=gst_mobile,address=address,title=title,first_name=first_name,last_name=last_name,email=email,mobile=mobile,passenger_type='Adult',date_of_birth=date_of_birth,src=src,dest=dest,airline_name=airline_name,origin_airport=origin_airport,destination_airport=destination_airport,flight_code=flight_code,flight_number=flight_number,departure_date=departure_date,departure_time=departure_time,arrival_date=arrival_date,arrival_time=arrival_time,duration=duration,stop=stop,pnr=pnr,flight_class=flight_class,base_price=base_price,total_fare=total_fare,taf=taf,paid_amount=paid_amount)
        cust_token = Akasa_token.objects.create(user=login_user, bookingId=booking_id,token=akasa_token)


        p_data = list(Passenger.objects.filter(user=login_user,bookingId=booking_id).values())
        print(p_data)
        for x in p_data:
            os_bookingId = x['os_bookingId']
            print(os_bookingId)

        if (flight_status == 'SUCCESSFUL'):
            company_name = 'tripjack'
            apibalance = list(APIbalance.objects.all().values())
            for x in apibalance:
                data_comany_name = x['company_name']
                data_balance = x['balance']
                if (company_name == data_comany_name):
                    r_balance = float(data_balance) - float(total_fare)
                    data_id = x['id']
                    apibalance_new = APIbalance.objects.get(id=data_id)
                    apibalance_new.balance = r_balance
                    apibalance_new.save()
        
        if (flight_status == 'PENDING') and (pnr == None):
            url1 = "https://www.fast2sms.com/dev/bulkV2"
            querystring = {
            "route" : "dlt",
            "sender_id" : "OSTOUR",
            "message" : "144727",
            "variables_values" : os_id+"|"+amount,
            "flash" : 0,
            "numbers" : "9315980690" ,
            }
          
            headers = {
            "authorization":"YnqF5CyIdT2ONH9rf6U0jlGWPswaJBhiS1KXgM3bR87ptxDZczkpnzN6yVDFaKI5hBQE9eq7tTOoJYb3",
            "Content-Type":"application/json"
            }
            try:
                response = requests.request("POST", url1,
                                            headers = headers,
                                            params = querystring)
                  
                print("SMS Successfully Sent")
            except:
                print("Oops! Something wrong")

        

            # mail server parameters
            smtpHost = "smtp.gmail.com"
            smtpPort = 587
            mailUname = 'no-reply@onlinesavaari.com'
            mailPwd = 'afbzoctjmpppkwvk'
            fromEmail = 'no-reply@onlinesavaari.com'

            # mail body, recepients, attachment files
            mailSubject = "Ticket Confirmation"
            mailContentHtml = "Your booking with Ref No."+ os_id +" Is Successful with Airline PNR " +pnr+".<br/> You have been charged RS " + amount +"for this booking.<br/>Thank you for booking With Online Savaari."
            recepientsMailList = [email,'booking@onlinesavaari.com']
            attachmentFpaths = ["flight/logo.png"]
            sendEmail(smtpHost, smtpPort, mailUname, mailPwd, fromEmail,
                      mailSubject, mailContentHtml, recepientsMailList, attachmentFpaths)

            print("execution complete...")
            # mail server parameters
            smtpHost = "smtp.gmail.com"
            smtpPort = 587
            mailUname = 'no-reply@onlinesavaari.com'
            mailPwd = 'afbzoctjmpppkwvk'
            fromEmail = 'no-reply@onlinesavaari.com'

            # mail body, recepients, attachment files
            mailSubject = "Ticket Confirmation"
            mailContentHtml = "Your booking with Ref No."+ os_id +" Is In Process with Online Savaari.<br/> You will get responce within 30 min.<br/>Thank you for booking With Online Savaari."
            recepientsMailList = [email,'booking@onlinesavaari.com']
            attachmentFpaths = ["flight/logo.png"]
            sendEmail(smtpHost, smtpPort, mailUname, mailPwd, fromEmail,
                      mailSubject, mailContentHtml, recepientsMailList, attachmentFpaths)

            print("execution complete...")
            

        if (flight_status == 'SUCCESSFUL'):
            url1 = "https://www.fast2sms.com/dev/bulkV2"
            grp = find_group(request.user)
            if (grp=="Customer"):
                querystring = {
                "route" : "dlt",
                "sender_id" : "OSTICK",
                "message" : "144678",
                "variables_values" : os_id+"|"+pnr+"|"+amount,
                "flash" : 0,
                "numbers" : "9315980690" ,
                }
          
                
            else:
                querystring = {
                "route" : "dlt",
                "sender_id" : "OSTICK",
                "message" : "144682",
                "variables_values" : first_name+"/"+last_name+"|"+src+"-"+dest+"|"+departure_date+"|"+flight_code+" "+flight_number+"|"+departure_time+"|"+pnr+"|"+"Online Savaari Private Limited",
                "flash" : 0,
                "numbers" : "9315980690" ,
                }
            
            headers = {
            "authorization":"YnqF5CyIdT2ONH9rf6U0jlGWPswaJBhiS1KXgM3bR87ptxDZczkpnzN6yVDFaKI5hBQE9eq7tTOoJYb3",
            "Content-Type":"application/json"
            }
            try:
                response = requests.request("POST", url1,
                                            headers = headers,
                                            params = querystring)
                  
                print("SMS Successfully Sent")
            except:
                print("Oops! Something wrong")

        

            # mail server parameters
            smtpHost = "smtp.gmail.com"
            smtpPort = 587
            mailUname = 'no-reply@onlinesavaari.com'
            mailPwd = 'afbzoctjmpppkwvk'
            fromEmail = 'no-reply@onlinesavaari.com'

            # mail body, recepients, attachment files
            mailSubject = "Ticket Confirmation"
            mailContentHtml = ""
            # mailContentHtml = """<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>Invoice</title> <style> .d-flex { display: flex; align-items: center; justify-content: start; gap: 1em; } /* .passengers--details__header { border-radius: 50%; } */ .invoice--main--container { font-family: sans-serif; color: #666666; } ul li{ margin-left: 0; } .invoice--main--container { width: 90%; max-width: 1180px; margin: 3.5em auto; } nav { display: flex; justify-content: space-between; align-items: center; background-color: #F0F0F0; padding: 1em; border-bottom: 1px solid rgba(0, 0, 0, 0.229); } .ban--logo { font-family: 'Mouse Memoirs', sans-serif; font-size: 2rem; font-weight: 900; color: #DF212E; } .icon--apps { display: flex; } .flight--details { display: flex; gap: 1.5em; padding: 0.8em 0; } .flight--details h4{ font-size: 0.8rem; font-weight: 600; } .fn--black { color: black !important; } .ref__num { padding-left: 1em; } /* passengers--details */ .passengers--details { border: 1px solid #CCCCCC; border-radius: 10px; margin-bottom: 1.2em; } .passengers--details__label { display: flex; justify-content: space-between; padding: 0.5em; padding-right: 1.5em; } .passengers--details__header { padding: 0.5em; border-bottom: 1px dotted #CCCCCC; } .passengers--details__header h3 { font-size: 0.8rem; font-weight: 600; } .passengers--details__label { font-size: 0.72rem; } .label { margin-bottom: 1em; } .label h4 { font-size: 0.72rem; font-weight: 500; } .passengers--details__label p { font-size: 0.72rem; } .flight--img { width: 100%; object-fit: contain; } .guidelines, .information { border: 2px solid #d1d1d1; margin-bottom: 1em; /* padding: 0.6em; */ } .guidelines--title { background-color: #EBEBEB; padding: 1em 0.8em; } .guidelines--content { padding: 0.5em; } .guidelines--content ul li + li { margin-top: 1em; } .air__img { border-radius: 50% } </style> </head> <body> <section class="main" id="tblCustomers"> <div class="invoice--main--container" > <header class="invoice--container" > <nav> <div class="ban--logo"> <img src="https://onlinesavaari.com/static/main/images/logo.png" alt=""> </div> <div class="icon--apps"> <div class="android"></div> <div class="apple"></div> </div> </nav> <div class="flight--details"> <h4 class="flight">FLIGHT</h4> <h4 class="e-ticket fn--black">E-TICKET</h4> <h4 class="ref--num"> REF NUMBER <span class="ref__num fn--black">"""+os_id+"""</span> </h4> </div> </header> <section class="main" id="tblCustomers1"> <div class="passengers--details"> <div class="passengers--details__header"> <h3>PASSENGERS DETAILS</h3> </div> <div class="passengers--details__label"> <div class="pass__name"> <div class="name__label label"> <h4>NAME</h4> </div> <div class="name__value"> <h4 class="name"> """+title+" "+first_name+" "+last_name+ """</h4> <p>("""+passenger_type+""")</p> <p>Insurance Policy:</p>  <p></p> </div> </div> <div class="pass__destination"> <div class="des__label label"> <h4>DESTINATION</h4> </div> <div class="des__value"> <p> <span class="from">"""+src+"""  </span> <span>-</span> <span class="to">"""+dest+""" </span> <span>-</span> <span class="to"> </span> </p> </div> </div> <div class="pass__meals"> <div class="meals__label label"> <h4>MEALS</h4> </div> <div class="meals__value"> <p>NA</p> </div> </div> <div class="pass__baggage"> <div class="baggage__label label"> <h4>BAGGAGE</h4> </div> <div class="baggage__value"> <p>15kg (Free)</p> </div> </div> <div class="pass__seat"> <div class="seat__label label"> <h4>SEAT NO.</h4> </div> <div class="seat__value"> <p>"""+src+"-"+dest+"""</p> </div> </div> <div class="pass__ticket"> <div class="ticket__label label"> <h4>TICKET NO.</h4> </div> <div class="ticket__value"> <p>"""+pnr+"""</p> </div> </div> </div> </div> <div class="passengers--details"> <div class="passengers--details__header d-flex"> <img src="https://onlinesavaari.com/static/main/images/arrow__air.png" alt=""> <h5>"""+src+"""</h5> <img src="https://onlinesavaari.com/static/main/images/air__logo.png" alt=""> <h5>"""+dest+"""</h5> <p class="date">"""+departure_date+""" </p> </div> <div class="passengers--details__label"> <div class="air__name"> <div class="name__label label"> <h4>AIRLINE</h4> </div> <div class="name__value"> <img class="air__img" src="https://onlinesavaari.com/static/main/images/airline/4.png" alt=""> <p>"""+origin_airport+"""</p> <p>"""+flight_code+"-"+flight_number+"""</p> </div> </div> <div class="air__departure"> <div class="des__label label"> <h4>DEPARTURE</h4> </div> <div class="des__value"> <h4>"""+src+"""</h4> <p>"""+departure_date+" "departure_time+""" </p> <p>"""+origin_airport+","+ """</p> </div> </div> <div class="air__arrival"> <div class="meals__label label"> <h4>ARRIVAL</h4> </div> <div class="air__value"> <h4>"""+dest+"""</h4> <p> """+arrival_date+" "+arrival_time+"""</p> <p>"""+destination_airport+","+"""</p> </div> </div> <div class="air__duration"> <div class="dur__label label"> <h4>DURATION</h4> </div> <div class="baggage__value"> <p>"""+str(duration)+"""</p> <p>"""+str(stop)+"""</p> </div> </div> <div class="pass__seat"> <div class="seat__label label"> <h4>SEAT NO.</h4> </div> <div class="seat__value"> <p>NA</p> </div> </div> <div class="pass__ticket"> <div class="ticket__label label"> <h4>TICKET NO.</h4> </div> <div class="ticket__value"> <p>"""+pnr+"""</p> </div> </div> </div> </div></section> <div class="useful-tip"> <p> Useful tip : You can go to Yatra Mybookings to check your refund status, if in future your flight is cancelled by the airline or you have cancelled the flight directly with the airline. Please bookmark this link for more details. </p> </div> <section class="guidelines" id="tblCustomers2"> <div class="guidelines--title"> <h3>Compulsory Guidelines for Domestic Travel</h3> </div> <div class="guidelines--content"> <p> The Government has decided for recommencement of domestic air travel of passengers with effect from 25th May 2020. In order to ensure safety of the passengers during prevailing circumstances due to COVID I9 pandemic, precautionary measures need to be taken by passengers </p> <ul> <li> All travellers above 14 years of age must have the Aarogya Setu app activated on their mobiles before arriving at the airport. </li> <li> Travellers will be required to certify the status of their health through the Aarogya Setu app or a self-declaration form. </li> <li> No physical check-in at airport counters would be done. Only those passengers with confirmed web check-in will be allowed to enter the airport. </li> <li> Travellers should report to the airport at least 2 hours prior to the departure time </li> <li> Only passengers who have flights departing in the next 4 hours will be allowed to enter the terminal building. </li> <li> Passengers are required to wear face masks at the airport and in the flight. </li> <li> Only 1 check-in baggage and 1 cabin baggage will be allowed per passenger. </li> <li> Travellers will be required to print and paste a pre-filled baggage tag and affix it on the bags. Alternatively, they should mention the PNR number and name on paper and affix it on the bags. </li> <li> Elderly, pregnant and ailing individuals are advised to avoid air travel. Additionally, individuals who have been tested COVID-19 positive or are staying in a containment zone should not travel. </li> <li> No meal service, newspapers or magazines will be available on-board. </li> <li> Travellers will be required to sign self-declaration forms. In case of a PNR having more than one passenger, the declaration would be deemed to be covering all the passengers mentioned in the PNR. </li> <li> View all mandatory travel guidelines issued by Govt. of India here </li> </ul> </div> </section> <section class="information"> <div class="guidelines--title"> <h3>Information</h3> </div> <div class="guidelines--content"> <ul> <li> All time indicated are the local times (in 24 hrs. format) at the relevant airport. </li> <li> Cancellation and date change fees are applicable before departure and per passenger basis. In case of amendment, along with the airline and Yatra fees, you will also have to pay fare difference, if any. </li> <li> Any change to a confirmed ticket including cancellation, postponement, and change of itinerary must be done at least 24 hours prior to flight departure. </li> <li> Please connect with the airline for refund or alternative to avoid no show before revised scheduled departure, in case you receive any email and SMS from airline about flight timings change. </li> <li> Please directly contact airline for any cancellation/reschedule within four hours of departure time </li> <li> Airline Contact Information: Go First : 18602-100-999,91-22-6273-2111 </li> <li> Please reference the Airline PNR Number when communicating with the airline regarding this booking. </li> <li> If a ticket is canceled directly from the airlines website, office or call center, the customer needs to Claim Refund from MyBookings portal at Yatra. Yatra will levy Rs. 400 per passenger per segment. </li> <li> Delhi and Mumbai airports have multiple terminals catering to domestic flights, please check the departure/arrival terminal of your flight with the airlines before reaching airport. </li> <li> Passengers traveling on flights originating from Jammu, Srinagar and Leh will not be allowed to carry any cabin baggage due to security restrictions. </li> <li> Indian citizens need to carry a printout of the e ticket along with a photo identity proof such as driver's license, voters ID or passport to the airline checkin counter. For infant passengers, it is mandatory to carry the Date of Birth certificate. Foreigners travelling on Indian domestic sectors needs to carry their passport along with e ticket. </li> <li> Use your Airline PNR for all your communication for this booking with the airline. </li> <li> We recommend you checkin at least 2 hours prior to departure of your domestic flight and 3 hours prior to your international flight. </li> <li> When an infant (not entitled to a seat or free baggage allowance) accompanies an adult, a carrycot, or a fully collapsible push chair/stroller is allowed. This may be carried in the cabin if space is available, or else as checked in baggage. </li> <li> Airlines allows free checked baggage of 15kgs per passenger for all domestic flights. </li> <li> It is mandatory to carry the Date of Birth certificate for infant passengers. </li> <li> Hand Baggage and Cabin Baggage of 5-7 kg (which would include Laptop and duty free shopping bags) having maximum overall dimensions of: 115 cms (L+W+H) on Boeing flights and 108 cms (L+W+H) on Bombardier flights, is allowed to be carried per passenger, free of cost. The baggage information provided here is just for reference. Kindly check with the airline before check-in Due to airport security regulations, no cabin baggage is allowed on flights originating from Jammu or Srinagar airports. </li> <li> For domestic airlines, baggage allowance of 1 piece is equivalent to one bag of 15 Kgs (max). However, this baggage information is just for reference. Please check with the airline before check-in. </li> <li> Please refer to the Passenger charter for any additional information. </li> </ul> </div> </section> </div> </section> </body> </html>"""                
            recepientsMailList = ['dishaarora1996@gmail.com']
            attachmentFpaths = ["flight/logo.png"]
            sendEmail(smtpHost, smtpPort, mailUname, mailPwd, fromEmail,
                      mailSubject, mailContentHtml, recepientsMailList, attachmentFpaths)

            print("execution complete...")



        context= { 
            "adata":adata,
            "os_bookingId" : os_id,
            "key" : key,
            "Person":Person,
            "id" : bid,
            "pnr" : pnr,
            "src":src,
            "dest":dest,
            "amount":amount,
            "baggage":baggage,
            "seat":seat,
            "meal":meal,
            # "ticketnumber":ticketnumber,
            "flight_status":flight_status,
            "insurance":insurance
        }

    if( rtype == "normal"):
        if(insurance_data != None):
            insurance_data = json.loads(insurance_data.replace("\'", "\""))
        search_request = {
            "bookingId" : booking_id,
        }
        result = flight_data(api_url, apikey, '/oms/v1/booking-details',search_request)
        data=result.json()
        # return JsonResponse(data)
        print(data)


        for i in data['itemInfos']['AIR']['tripInfos']:
            for a in i['sI']:
                airline_name= a['fD']['aI']['name']
                origin_airport = a['da']['name']
                destination_airport=a['aa']['name']
                flight_code = a['fD']['aI']['code']
                flight_number = a['fD']['fN']
                departure_datetime = a['dt']
                datetime =  departure_datetime.split("T")
                departure_time = datetime[1]
                departure_date= datetime[0]
                arrival_datetime = a['at']
                datetime =  arrival_datetime.split("T")
                arrival_time = datetime[1]
                arrival_date= datetime[0]
                duration= a['duration']
                stop =a['stops']
                flight_class = cabinClass


        base_price = data['itemInfos']['AIR']['totalPriceInfo']['totalFareDetail']['fC']['BF']
        total_fare = data['itemInfos']['AIR']['totalPriceInfo']['totalFareDetail']['fC']['TF']
        taf = total_fare - base_price
        taf = round(taf,2)
        paid_amount = amount
        email = data['order']['deliveryInfo']['emails'][0]
        mobile = data['order']['deliveryInfo']['contacts'][0]
        flight_status = data['order']['status']
        pnr = "None"
        baggage = None
        meal = None
        seat = None
        ticketnumber = None
        i = 0
        ins_amount = 0
        for a in data['itemInfos']['AIR']['travellerInfos']:
            insurancelist = []
            # return JsonResponse(insurance_data, safe=False)
            if(insurance_data):
                i += 1
                for v in insurance_data[f'person_{i}']:
                    # return JsonResponse(v, safe=False)

                    passengerreference = str(randint(1000000000, 9999999999))
                    name = v['first_name'] + " " + v["last_name"]

                    a_list = v['tripdate']['arrivaldate'].split("T")[0].split("-")
                    ayy = int(a_list[0])
                    amm = int(a_list[1])
                    add = int(a_list[2])
                    a1 = date(ayy, amm, add)
                    d_list = v['tripdate']['departuredate'].split("T")[0].split("-")
                    dyy = int(d_list[0])
                    dmm = int(d_list[1])
                    ddd = int(d_list[2])
                    d1 = date(dyy, dmm, ddd)
                    delta = a1 - d1
                    if delta.days == 0:
                        totaldays = str(delta.days+1)
                    else:
                        totaldays = str(delta.days)
                    dob_list = v['dob'].split("-")
                    dobyy = int(dob_list[0])
                    today = date.today()
                    today_year = today.year
                    age = today_year - dobyy
                    arrivaldate = str(v['tripdate']['arrivaldate'].split("T")[0])
                    departuredate = str(v['tripdate']['departuredate'].split("T")[0])
                    departuredate = change_date_format(departuredate)
                    arrivaldate = change_date_format(arrivaldate)

                    policy = {
                        'policy': {
                            'identity': {
                                'sign': 'e663ecc7-7e40-4eec-a2be-56d952729860',
                                'branchsign': 'acfeba18-073b-42c8-b813-fe170ceed3df',
                                'username': 'Online_Savri',
                                'reference': f'SavariInc{randint(10000, 99999)}',
                            },
                            'plan': {
                                'categorycode': v['category'],
                                'plancode': v['plancode'],
                                'basecharges': str(v['price']['basePrice']),
                                'totalbasecharges': str(v['price']['total_base']),
                                'servicetax': str(v['price']['service_tax']),
                                'totalcharges': str(v['price']['basePrice']),
                            },
                            'traveldetails': {
                                'departuredate':departuredate,
                                'days':totaldays,
                                'arrivaldate':arrivaldate,
                            },
                            'passengerreference': passengerreference,
                            'insured': {
                                'passport': v['passport'],
                                'contactdetails': {
                                    'address1':'NA',
                                    'address2':'NA',
                                    'city':'NA',
                                    'district':'NA',
                                    'state':'NA',
                                    'pincode':'NA',
                                    'country':'NA',
                                    'phoneno':'NA',
                                    'mobileno':mobile,
                                    'emailaddress':email,
                                },
                                'name': name,
                                'dateofbirth': v['dob'],
                                'age': str(age),
                                'trawelltagnumber': "",
                                'nominee': 'NA',
                                'relation': 'NA',
                                'pastillness': 'NA',
                            },
                            'otherdetails': {
                                'policycomment': '',
                                'niversityname':'',
                                'universityaddress': '',
                            }
                        }
                    }
                    # return HttpResponse(dicttoxml(json.loads(json.dumps(policy)), attr_type=False, root=False))

                    xml = dicttoxml(json.loads(json.dumps(policy)), attr_type=False, root=False)
                    xml = parseString(xml)
                    # return HttpResponse(xml.childNodes[0].toprettyxml())
                    data = encrypt(xml.childNodes[0].toprettyxml())
                    result = insurance(url_inc,data,Ref)
                    result = result.text
                    # return HttpResponse(result)
                    result = xmltodict.parse(result)
                    # with open("flight/insurance.xml") as xml_file:
                    #     xml_policy = xml_file.read() 
                    # data = encrypt(xml_policy)
                    # result = insurance(url_inc,data,Ref)
                    # result = result.text
                    # result = xmltodict.parse(result)
                    insurancelist.append(result)
                # return JsonResponse(insurancelist, safe=False)
            
            if('pnrDetails' in a): 
                res= a['pnrDetails']
                pnr = list(res.values())[0]
            if('ssrBaggageInfos' in a):
                res = a['ssrBaggageInfos']
                baggage_list = list(res.values())[0]
                baggage = baggage_list['desc']
            if('ssrMealInfos' in a): 
                res = a['ssrMealInfos']
                meal_list = list(res.values())[0]
                meal = meal_list['desc']
            if('ssrSeatInfos' in a): 
                res = a['ssrSeatInfos']
                seat_list = list(res.values())[0]
                seat = seat_list['code']
            if('ticketNumberDetails' in a): 
                res = a['ticketNumberDetails']
                ticketnumber = list(res.values())[0]

            title = a['ti']
            first_name = a['fN']
            last_name = a['lN']
            date_of_birth = a['dob']
            passenger_type = a['pt']
            # os_id = Passenger.objects.latest('id')
            # os_id = os_id.os_bookingId
            # print(os_id,"os_id")
            # os_id=int(os_id[2:])
            # os_id+=1
            # os_id=str(os_id)
            # os_id="OS"+os_id
            # print(os_id)
            osn_id = randint(1000000000, 9999999999)
            osn_id = str(osn_id)
            os_id = 'OS'+osn_id
            print(os_id)

            if(book_status == 'false'):
                flight_status = 'PENDING'
            else:
                flight_status = 'SUCCESSFUL'

            cust1=Passenger.objects.create(bookingId=booking_id,transaction_id=transaction_id,err_code=err_code,err_desc=err_msg,os_bookingId=os_id,user=login_user,flight_status=flight_status,gstno=gstno,company_name=company_name,gst_email=gst_email,gst_mobile=gst_mobile,address=address,title=title,first_name=first_name,last_name=last_name,email=email,mobile=mobile,passenger_type='Adult',date_of_birth=date_of_birth,src=src,dest=dest,airline_name=airline_name,origin_airport=origin_airport,destination_airport=destination_airport,flight_code=flight_code,flight_number=flight_number,departure_date=departure_date,departure_time=departure_time,arrival_date=arrival_date,arrival_time=arrival_time,duration=duration,stop=stop,pnr=pnr,flight_class=flight_class,base_price=base_price,total_fare=total_fare,taf=taf,paid_amount=paid_amount,insurance_pdf=json.dumps({'insr':insurancelist}),insurance_charges=ins_amount)


            p_data = list(Passenger.objects.filter(user=login_user,bookingId=booking_id).values())
            print(p_data)

            mark = (WalletDetails.objects.filter(email=request.user)).latest('id')
            mark.booking_id = os_id
            mark.save()
            for x in p_data:
                os_bookingId = x['os_bookingId']
                print(os_bookingId)

            if (flight_status == 'SUCCESSFUL'):
                company_name = 'tripjack'
                apibalance = list(APIbalance.objects.all().values())
                for x in apibalance:
                    data_comany_name = x['company_name']
                    data_balance = x['balance']
                    if (company_name == data_comany_name):
                        r_balance = float(data_balance) - float(total_fare)
                        data_id = x['id']
                        apibalance_new = APIbalance.objects.get(id=data_id)
                        apibalance_new.balance = r_balance
                        apibalance_new.save()
            airline_list = []
            with open("static/flight/airlines.json", "r") as f:
                airline = json.loads(f.read())
            for x in airline:
                airline_list.append(x['code'])


            with open("static/flight/airport_list.json", "r") as f:
                airport = json.loads(f.read())
                l = []
                k = []
                for i in airport:
                    if(i['country'] == 'India'):
                        air_domestic = i['code']
                        l.append(air_domestic)

            for j in airport:
                if(j['country'] != 'India'):
                    air_international = j['code']
                    k.append(air_international)


            if (flight_status == 'SUCCESSFUL') and (pnr != "None"):
                commission_data = list(Commission.objects.all().values()) 
                print(commission_data)
                for x in commission_data:
                    com_start_date = x['start_date']
                    com_end_date= x['end_date']
                    today = date.today()
                    if ((com_start_date <= today) and (com_end_date >= today)):
                        email_list = eval(x['email'])
                        login_user = str(request.user)
                        airline_list_db = eval(x['airline_type'])
                        for y in email_list:
                            if(y == login_user) or (y == "All"):
                                print("enter in all agents")
                                if(airline_list_db != []):
                                    for z in airline_list_db:
                                        print("enter in for")
                                        if(z in airline_list):
                                            print("passed first round")
                                            if(z == flight_code):
                                                print("enter in all airlines")
                                                if (x['commission_type'] == "Domestic"):
                                                    print("enter in all airline")
                                                    if((src in l) and (dest in l)):
                                                        if(x['amount_type'] == "fixed"):
                                                            discount = float(x['amount'])
                                                            tds = (discount * 5)/100
                                                            discount = discount - tds
                                                            wallet_detail = (WalletDetails.objects.filter(booking_id=os_id,username=request.user).values()).latest('id')
                                                            print(wallet_detail)
                                                            wallet_bal = wallet_detail['wallet_balance']
                                                            new_bal = float(wallet_bal)+ float(discount)
                                                            transaction_number = randint(1000000000, 9999999999)
                                                            osn_id = str(transaction_number)
                                                            transaction_number = 'DSCNT'+osn_id
                                                            curl = WalletDetails.objects.create(booking_id=os_id,username=request.user,tds=tds,email=request.user,wallet_balance=new_bal,amount=discount,trasc_type="Credit",transaction_mode="DISCOUNT",transaction_status="Success",transaction_id=transaction_number,note="ADDED AS DISCOUNT.")
                                                        elif(x['amount_type'] == "percent"):
                                                            discount = float(x['amount'])
                                                            discount = (base_price * discount)/100
                                                            tds = (discount * 5)/100
                                                            discount = discount - tds
                                                            wallet_detail = (WalletDetails.objects.filter(booking_id=os_id,username=request.user).values()).latest('id')
                                                            wallet_bal = wallet_detail['wallet_balance']
                                                            new_bal = float(wallet_bal)+ float(discount)
                                                            transaction_number = randint(1000000000, 9999999999)
                                                            osn_id = str(transaction_number)
                                                            transaction_number = 'DSCNT'+osn_id
                                                            curl = WalletDetails.objects.create(booking_id=os_id,username=request.user,tds=tds,email=request.user,wallet_balance=new_bal,amount=discount,trasc_type="Credit",transaction_mode="DISCOUNT",transaction_status="Success",transaction_id=transaction_number,note="ADDED AS DISCOUNT.")
                                                elif(x['commission_type'] == "International"):
                                                    if((src in k) and (dest in k)):
                                                        if(x['amount_type'] == "fixed"):
                                                            discount = float(x['amount'])
                                                            tds = (discount * 5)/100
                                                            discount = discount - tds
                                                            wallet_detail = (WalletDetails.objects.filter(booking_id=os_id,username=request.user).values()).latest('id')
                                                            print(wallet_detail)
                                                            wallet_bal = wallet_detail['wallet_balance']
                                                            new_bal = float(wallet_bal)+ float(discount)
                                                            transaction_number = randint(1000000000, 9999999999)
                                                            osn_id = str(transaction_number)
                                                            transaction_number = 'DSCNT'+osn_id
                                                            curl = WalletDetails.objects.create(booking_id=os_id,username=request.user,tds=tds,email=request.user,wallet_balance=new_bal,amount=discount,trasc_type="Credit",transaction_mode="DISCOUNT",transaction_status="Success",transaction_id=transaction_number,note="ADDED AS DISCOUNT.")
                                                        elif(x['amount_type'] == "percent"):
                                                            discount = float(x['amount'])
                                                            discount = (base_price * discount)/100
                                                            tds = (discount * 5)/100
                                                            discount = discount - tds
                                                            wallet_detail = (WalletDetails.objects.filter(booking_id=os_id,username=request.user).values()).latest('id')
                                                            wallet_bal = wallet_detail['wallet_balance']
                                                            new_bal = float(wallet_bal)+ float(discount)
                                                            transaction_number = randint(1000000000, 9999999999)
                                                            osn_id = str(transaction_number)
                                                            transaction_number = 'DSCNT'+osn_id
                                                            curl = WalletDetails.objects.create(booking_id=os_id,username=request.user,tds=tds,email=request.user,wallet_balance=new_bal,amount=discount,trasc_type="Credit",transaction_mode="DISCOUNT",transaction_status="Success",transaction_id=transaction_number,note="ADDED AS DISCOUNT.")
                                else:
                                    if (x['commission_type'] == "Domestic"):
                                        print("enter in all airline")
                                        if((src in l) and (dest in l)):
                                            if(x['amount_type'] == "fixed"):
                                                discount = float(x['amount'])
                                                tds = (discount * 5)/100
                                                discount = discount - tds
                                                wallet_detail = (WalletDetails.objects.filter(booking_id=os_id,username=request.user).values()).latest('id')
                                                print(wallet_detail)
                                                wallet_bal = wallet_detail['wallet_balance']
                                                new_bal = float(wallet_bal)+ float(discount)
                                                transaction_number = randint(1000000000, 9999999999)
                                                osn_id = str(transaction_number)
                                                transaction_number = 'DSCNT'+osn_id
                                                curl = WalletDetails.objects.create(booking_id=os_id,username=request.user,tds=tds,email=request.user,wallet_balance=new_bal,amount=discount,trasc_type="Credit",transaction_mode="DISCOUNT",transaction_status="Success",transaction_id=transaction_number,note="ADDED AS DISCOUNT.")
                                            elif(x['amount_type'] == "percent"):
                                                discount = float(x['amount'])
                                                discount = (base_price * discount)/100
                                                tds = (discount * 5)/100
                                                discount = discount - tds
                                                wallet_detail = (WalletDetails.objects.filter(booking_id=os_id,username=request.user).values()).latest('id')
                                                wallet_bal = wallet_detail['wallet_balance']
                                                new_bal = float(wallet_bal)+ float(discount)
                                                transaction_number = randint(1000000000, 9999999999)
                                                osn_id = str(transaction_number)
                                                transaction_number = 'DSCNT'+osn_id
                                                curl = WalletDetails.objects.create(booking_id=os_id,username=request.user,tds=tds,email=request.user,wallet_balance=new_bal,amount=discount,trasc_type="Credit",transaction_mode="DISCOUNT",transaction_status="Success",transaction_id=transaction_number,note="ADDED AS DISCOUNT.")
                                    elif(x['commission_type'] == "International"):
                                        if((src in k) and (dest in k)):
                                            if(x['amount_type'] == "fixed"):
                                                discount = float(x['amount'])
                                                tds = (discount * 5)/100
                                                discount = discount - tds
                                                wallet_detail = (WalletDetails.objects.filter(booking_id=os_id,username=request.user).values()).latest('id')
                                                print(wallet_detail)
                                                wallet_bal = wallet_detail['wallet_balance']
                                                new_bal = float(wallet_bal)+ float(discount)
                                                transaction_number = randint(1000000000, 9999999999)
                                                osn_id = str(transaction_number)
                                                transaction_number = 'DSCNT'+osn_id
                                                curl = WalletDetails.objects.create(booking_id=os_id,username=request.user,tds=tds,email=request.user,wallet_balance=new_bal,amount=discount,trasc_type="Credit",transaction_mode="DISCOUNT",transaction_status="Success",transaction_id=transaction_number,note="ADDED AS DISCOUNT.")
                                            elif(x['amount_type'] == "percent"):
                                                discount = float(x['amount'])
                                                discount = (base_price * discount)/100
                                                tds = (discount * 5)/100
                                                discount = discount - tds
                                                wallet_detail = (WalletDetails.objects.filter(booking_id=os_id,username=request.user).values()).latest('id')
                                                wallet_bal = wallet_detail['wallet_balance']
                                                new_bal = float(wallet_bal)+ float(discount)
                                                transaction_number = randint(1000000000, 9999999999)
                                                osn_id = str(transaction_number)
                                                transaction_number = 'DSCNT'+osn_id
                                                curl = WalletDetails.objects.create(booking_id=os_id,username=request.user,tds=tds,email=request.user,wallet_balance=new_bal,amount=discount,trasc_type="Credit",transaction_mode="DISCOUNT",transaction_status="Success",transaction_id=transaction_number,note="ADDED AS DISCOUNT.")
                                 

            if (flight_status == 'PENDING'):
                url1 = "https://www.fast2sms.com/dev/bulkV2"
                querystring = {
                "route" : "dlt",
                "sender_id" : "OSTOUR",
                "message" : "144727",
                "variables_values" : os_id+"|"+amount,
                "flash" : 0,
                "numbers" : "9315980690" ,
                }
              
                
                headers = {
                "authorization":"YnqF5CyIdT2ONH9rf6U0jlGWPswaJBhiS1KXgM3bR87ptxDZczkpnzN6yVDFaKI5hBQE9eq7tTOoJYb3",
                "Content-Type":"application/json"
                }
                try:
                    response = requests.request("POST", url1,
                                                headers = headers,
                                                params = querystring)
                      
                    print("SMS Successfully Sent")
                except:
                    print("Oops! Something wrong")
                # mail server parameters
                smtpHost = "smtp.gmail.com"
                smtpPort = 587
                mailUname = 'no-reply@onlinesavaari.com'
                mailPwd = 'afbzoctjmpppkwvk'
                fromEmail = 'no-reply@onlinesavaari.com'

                # mail body, recepients, attachment files
                mailSubject = "Ticket Confirmation"
                mailContentHtml = "Your booking with Ref No."+os_id +" Is In Process with Online Savaari.<br/> You will get responce within 30 min.<br/>Thank you for booking With Online Savaari."
                recepientsMailList = ['richapaliwaldhawan@gmail.com']
                attachmentFpaths = []
                sendEmail(smtpHost, smtpPort, mailUname, mailPwd, fromEmail,
                          mailSubject, mailContentHtml, recepientsMailList, attachmentFpaths)

                print("execution complete...")
            
                url1 = "https://www.fast2sms.com/dev/bulkV2"
                grp = find_group(request.user)
                if (grp=="Customer"):
                    querystring = {
                    "route" : "dlt",
                    "sender_id" : "OSTICK",
                    "message" : "144678",
                    "variables_values" : os_id+"|"+pnr+"|"+amount,
                    "flash" : 0,
                    "numbers" : "9315980690" ,
                    }
              
                    
                else:
                    querystring = {
                    "route" : "dlt",
                    "sender_id" : "OSTICK",
                    "message" : "144682",
                    "variables_values" : first_name+"/"+last_name+"|"+src+"-"+dest+"|"+departure_date+"|"+flight_code+" "+flight_number+"|"+departure_time+"|"+pnr+"|"+"Online Savaari Private Limited",
                    "flash" : 0,
                    "numbers" : "9315980690" ,
                    }
                
                headers = {
                "authorization":"YnqF5CyIdT2ONH9rf6U0jlGWPswaJBhiS1KXgM3bR87ptxDZczkpnzN6yVDFaKI5hBQE9eq7tTOoJYb3",
                "Content-Type":"application/json"
                }
                try:
                    response = requests.request("POST", url1,
                                                headers = headers,
                                                params = querystring)
                      
                    print("SMS Successfully Sent")
                except:
                    print("Oops! Something wrong")

            

                # mail server parameters
                smtpHost = "smtp.gmail.com"
                smtpPort = 587
                mailUname = 'no-reply@onlinesavaari.com'
                mailPwd = 'afbzoctjmpppkwvk'
                fromEmail = 'no-reply@onlinesavaari.com'

                # mail body, recepients, attachment files
                mailSubject = "Ticket Confirmation"
                mailContentHtml = """<!doctype html><html lang=en><head><meta charset=UTF-8><meta http-equiv=X-UA-Compatible content="IE=edge"><meta name=viewport content="width=device-width,initial-scale=1"><title>Invoice</title><style>.d-flex{display:flex;align-items:center;justify-content:start}.d-flex>*{margin-right:1em}.invoice--main--container{font-family:sans-serif;color:#666;width:90%;max-width:1180px;margin:3.5em auto}ul li{margin-left:0}.nav-bar{display:flex;justify-content:space-between;align-items:center;background-color:#ebebeb;padding:1em;border-bottom:1px solid rgba(0,0,0,.229)}.flight--details{display:flex;padding:.8em 0}.flight--details h4{font-size:.8rem;font-weight:600;margin-right:1.5em}.fn--black{color:#000!important}.ref__num{padding-left:1em}.passengers--details{border:1px solid #ccc;border-radius:10px;margin-bottom:1.2em}.passengers--details__label{display:flex;padding:.5em;padding-right:1.5em;font-size:.72rem}table{width:100%;border-collapse:collapse;margin:1em;color:#7d7e7b}tr{font-size:.72rem}th{text-align:start}.passengers--details__header{padding:.5em;border-bottom:1px dotted #ccc}.passengers--details__header h3{font-size:.8rem;font-weight:600}.passengers--details__label div{width:25%;margin-right:auto;font-size:clamp(.8rem,5vw,1rem)}.label{margin-bottom:1em}.label h4{font-size:.72rem;font-weight:500}.passengers--details__label p{font-size:.72rem}.flight--img{width:100%;object-fit:contain}.guidelines,.information{border:2px solid #d1d1d1;margin-bottom:1em}.guidelines--title{background-color:#ebebeb;padding:1em .8em}.guidelines--content{padding:.5em}.guidelines--content ul li+li{margin-top:1em}.air__img{border-radius:50%}</style></head><body><section class=main id=tblCustomers><div class=invoice--main--container><header class=invoice--container><div class=nav-bar><div class=ban--logo><img src=https://onlinesavaari.com/static/main/images/logo.png alt=""></div><div class=icon--apps><div class=android></div><div class=apple></div></div></div><div class=flight--details><h4 class=flight>FLIGHT</h4><h4 class="e-ticket fn--black">E-TICKET</h4><h4 class=ref--num> REF NUMBER <span class="ref__num fn--black">"""+os_id+"""</span></h4></div></header><section class=main id=tblCustomers1><div class=passengers--details><div class=passengers--details__header><h3>PASSENGERS DETAILS</h3></div><table><tr><th>NAME</th><th>DESTINATION</th><th>MEALS</th><th>BAGGAGE</th><th>SEAT NO.</th><th>TICKET NO.</th></tr><tr><td><h4 class=name> """ +title+" "+first_name+" "+last_name+"""</h4><p>("""+passenger_type+""")</p><p>Insurance Policy:</p><p></p></td><td><p><span class=from>"""+src+""" </span><span>-</span><span class=to>"""+dest+"""
</span><span>-</span><span class=to></span></p></td><td><p>"""+str(meal)+"""</p></td><td>
15kg (Free)
</td><td><p>"""+str(seat)+"""</p></td><td><p>"""+pnr+"""</p></td></tr></table></div><div class=passengers--details><div class="passengers--details__header d-flex"><img src=https://onlinesavaari.com/static/main/images/arrow__air.png alt=""><h5>"""+src+"""</h5><img src=https://onlinesavaari.com/static/main/images/air__logo.png alt=""><h5>"""+dest+"""</h5><p class=date>"""+departure_date+""" </p></div><table><th>AIRLINE</th><th>DEPARTURE</th><th>ARRIVAL</th><th>DURATION</th><th>SEAT NO.</th><th>TICKET NO.</th><tr><td><img class=air__img style=margin-top:1em src=https://onlinesavaari.com/static/main/images/airline/4.png alt=""><p>"""+str(airline_name)+"""</p><p>"""+flight_code+"-"+flight_number+"""</p></td><td><h4>"""+src+"""</h4><p>"""+departure_date+" "+departure_time+""" </p><p>"""+origin_airport+"""</p></td><td><h4>"""+dest+"""</h4><p> """+arrival_date+" "+arrival_time+"""</p><p>"""+destination_airport+","+"""</p></td><td><p>"""+str(duration)+"""</p></td><td><p>NA</p></td><td><p>"""+pnr+"""</p></td></tr></table></div></section><div class=useful-tip><p> Useful tip : You can go to Yatra Mybookings to check your refund status, if in future your flight is cancelled by the airline or you have cancelled the flight directly with the airline. Please bookmark this link for more details. </p></div><section class=guidelines id=tblCustomers2><div class=guidelines--title><h3>Compulsory Guidelines for Domestic Travel</h3></div><div class=guidelines--content><p> The Government has decided for recommencement of domestic air travel of passengers with effect from 25th May 2020. In order to ensure safety of the passengers during prevailing circumstances due to COVID I9 pandemic, precautionary measures need to be taken by passengers </p><ul><li> All travellers above 14 years of age must have the Aarogya Setu app activated on their mobiles before arriving at the airport. </li><li> Travellers will be required to certify the status of their health through the Aarogya Setu app or a self-declaration form. </li><li> No physical check-in at airport counters would be done. Only those passengers with confirmed web check-in will be allowed to enter the airport. </li><li> Travellers should report to the airport at least 2 hours prior to the departure time </li><li> Only passengers who have flights departing in the next 4 hours will be allowed to enter the terminal building. </li><li> Passengers are required to wear face masks at the airport and in the flight. </li><li> Only 1 check-in baggage and 1 cabin baggage will be allowed per passenger. </li><li> Travellers will be required to print and paste a pre-filled baggage tag and affix it on the bags. Alternatively, they should mention the PNR number and name on paper and affix it on the bags. </li><li> Elderly, pregnant and ailing individuals are advised to avoid air travel. Additionally, individuals who have been tested COVID-19 positive or are staying in a containment zone should not travel. </li><li> No meal service, newspapers or magazines will be available on-board. </li><li> Travellers will be required to sign self-declaration forms. In case of a PNR having more than one passenger, the declaration would be deemed to be covering all the passengers mentioned in the PNR. </li><li> View all mandatory travel guidelines issued by Govt. of India here </li></ul></div></section><section class=information><div class=guidelines--title><h3>Information</h3></div><div class=guidelines--content><ul><li> All time indicated are the local times (in 24 hrs. format) at the relevant airport. </li><li> Cancellation and date change fees are applicable before departure and per passenger basis. In case of amendment, along with the airline and Yatra fees, you will also have to pay fare difference, if any. </li><li> Any change to a confirmed ticket including cancellation, postponement, and change of itinerary must be done at least 24 hours prior to flight departure. </li><li> Please connect with the airline for refund or alternative to avoid no show before revised scheduled departure, in case you receive any email and SMS from airline about flight timings change. </li><li> Please directly contact airline for any cancellation/reschedule within four hours of departure time </li><li> Airline Contact Information: Go First : 18602-100-999,91-22-6273-2111 </li><li> Please reference the Airline PNR Number when communicating with the airline regarding this booking. </li><li> If a ticket is canceled directly from the airlines website, office or call center, the customer needs to Claim Refund from MyBookings portal at Yatra. Yatra will levy Rs. 400 per passenger per segment. </li><li> Delhi and Mumbai airports have multiple terminals catering to domestic flights, please check the departure/arrival terminal of your flight with the airlines before reaching airport. </li><li> Passengers traveling on flights originating from Jammu, Srinagar and Leh will not be allowed to carry any cabin baggage due to security restrictions. </li><li> Indian citizens need to carry a printout of the e ticket along with a photo identity proof such as driver's license, voters ID or passport to the airline checkin counter. For infant passengers, it is mandatory to carry the Date of Birth certificate. Foreigners travelling on Indian domestic sectors needs to carry their passport along with e ticket. </li><li> Use your Airline PNR for all your communication for this booking with the airline. </li><li> We recommend you checkin at least 2 hours prior to departure of your domestic flight and 3 hours prior to your international flight. </li><li> When an infant (not entitled to a seat or free baggage allowance) accompanies an adult, a carrycot, or a fully collapsible push chair/stroller is allowed. This may be carried in the cabin if space is available, or else as checked in baggage. </li><li> Airlines allows free checked baggage of 15kgs per passenger for all domestic flights. </li><li> It is mandatory to carry the Date of Birth certificate for infant passengers. </li><li> Hand Baggage and Cabin Baggage of 5-7 kg (which would include Laptop and duty free shopping bags) having maximum overall dimensions of: 115 cms (L+W+H) on Boeing flights and 108 cms (L+W+H) on Bombardier flights, is allowed to be carried per passenger, free of cost. The baggage information provided here is just for reference. Kindly check with the airline before check-in Due to airport security regulations, no cabin baggage is allowed on flights originating from Jammu or Srinagar airports. </li><li> For domestic airlines, baggage allowance of 1 piece is equivalent to one bag of 15 Kgs (max). However, this baggage information is just for reference. Please check with the airline before check-in. </li><li> Please refer to the Passenger charter for any additional information. </li></ul></div></section></div></section></body></html>"""                
                recepientsMailList = ['dishaarora1996@gmail.com']
                attachmentFpaths = ["flight/logo.png"]
                sendEmail(smtpHost, smtpPort, mailUname, mailPwd, fromEmail,
                          mailSubject, mailContentHtml, recepientsMailList, attachmentFpaths)

                print("execution complete...")


            context= {
                "data":data,
                "os_bookingId" : os_bookingId,
                "key" : key,
                "Person":Person,
                "id" : bid,
                "pnr" : pnr,
                "src":src,
                "dest":dest,
                "amount":amount,
                "baggage":baggage,
                "seat":seat,
                "meal":meal,
                "ticketnumber":ticketnumber,
                "flight_status":flight_status,
                "insurance":insurance
            }

    if(rtype == "series" ):
        header =  {"api-key":api_key,"Authorization":token, "Content-Type":"application/json"}
        seriesurl= "https://omairiq.azurewebsites.net/ticket?booking_id="+sbookindId
        details = requests.get(seriesurl, headers=header)
        sdata = details.json()
        print(sdata)
        flight_status = sdata['status']
        print(flight_status,"flight_status")
        route = sdata['data']['sector']
        route = route.split(" // ")
        paxdetail = sdata['data']['passenger_details']['Adult'][0]['Name']
        paxdetail = paxdetail.split(" ")
        title= paxdetail[0]
        title = title.replace(".","")
        first_name = paxdetail[1]
        last_name = paxdetail[2]
        pnr = sdata['data']['pnr']
        base_price = sdata['data']['total_amount']
        airline_name = sdata['data']['airline']
        departure_time = sdata['data']['departure_time']
        arrival_time = sdata['data']['arrival_time']
        src = route[0]
        dest = route[1]
        total_fare = sdata['data']['total_amount']
        taf = 0
        paid_amount = amount
        time_cal = arrival_time.split(":")
        hr = int(time_cal[0])
        mins = int(time_cal[1])
        flight = flight_num.split(" ")
        flight_code = flight[0]
        flight_number =flight[1]
        # arrival_time = time(hr,mins)
        # print(arrival_time)
        # time_cal = departure_time.split(":")
        # hr = int(time_cal[0],)
        # mins = int(time_cal[1])
        # departure_time = datetime.datetime.strptime(hr,mins,'%M')
        # print(departure_time)
        # duration = arrival_time - departure_time
        # print(duration)
        # print(title,first_name,amount,last_name,email,mobile,pnr,cabinClass,base_price,total_fare,taf,paid_amount,date_of_birth,airline_name,duration,src,dest)
        osn_id = randint(1000000000, 9999999999)
        osn_id = str(osn_id)
        os_bookingId = 'OS'+osn_id
        print(os_bookingId)

        cust1=Passenger.objects.create(bookingId=sbookindId,transaction_id=transaction_id,err_code=err_code,err_desc=err_msg,os_bookingId=os_bookingId,user=login_user,flight_status=flight_status,title=title,first_name=first_name,last_name=last_name,email=email,mobile=mobile,passenger_type=cabinClass,date_of_birth=date_of_birth,src=src,dest=dest,airline_name=airline_name,origin_airport=src,destination_airport=dest,flight_code=flight_code,flight_number=flight_number,departure_date=departure_date.replace('/', '-'),departure_time=departure_time,arrival_date=arrival_date.replace('/', '-'),arrival_time=arrival_time,duration="1h 30min",stop= False,pnr=pnr,flight_class=cabinClass,base_price=base_price,total_fare=total_fare,taf=taf,paid_amount=paid_amount)
            
        context= {
            "flight_code" : flight_code,
            "os_bookingId" : os_bookingId,
            "arrival_date" : arrival_date,
            "email" : email,
            "mobile" : mobile,
            "airline_name" : airline_name,
            "departure_date" : departure_date,
            "key" : key,
            "sdata" : sdata,
            "Person":Person,
            "id" : bid,
            "src":src,
            "dest":dest,
            "amount":amount,
            "insurance":insurance
        }   

    return render(request, "online_savaari/newinvoice.html", context)


@api_view(["GET","POST"])
def cancel_booking(request):
    login_user = request.user

    if not login_user.is_authenticated:
        return JsonResponse({'status':False, 'msg':"User is not logged In!"})
        
    bookingId = request.POST.get('bookingId')
    bookingId1 = request.POST.get('bookingId1')
    remark = request.POST.get('remark')
    radio1 = request.POST.get('radio1')
    person_name = request.POST.getlist('person_name')
    rtype = "akasa"
    print(bookingId,rtype)

    if(rtype=="normal"):
        t=[]
        if (radio1== "complete"):
            search_request = {
            "bookingId": bookingId,
            "remarks":"remark",
            "type": "CANCELLATION"
            }

        if(radio1 == "traveller"):
            if(len(person_name) > 0):
                for i in person_name:
                    cust1=list(Passenger.objects.filter(bookingId=bookingId).filter(first_name=i).values())
                    t.append({
                        'fn':cust1[0]["first_name"],
                        'ln':cust1[0]["last_name"]
                    })
                    if(i == person_name[-1]):
                        src=cust1[0]['src']
                        dest=cust1[0]['dest']
                        departureDate=cust1[0]['departure_date'].isoformat()

                search_request=  {
                        "bookingId": bookingId,
                        "type": "CANCELLATION",
                        "remarks":"test CANCELLATION",
                        "trips":[
                            {
                                "src":src,
                                "dest":dest,
                                "departureDate":departureDate,
                                "travellers":t,
                            }
                        ]
                    }

        if(radio1 == "route"):
                search_request= {
                    "bookingId": bookingId,
                    "type": "CANCELLATION",
                    "remarks":"test CANCELLATION",
                    "trips":[
                        {
                            "src":src,
                            "dest":dest,
                            "departureDate":departureDate
                        }
                    ]
                    }

        result = flight_data(api_url, apikey, '/oms/v1/air/amendment/submit-amendment',search_request)
        data=result.json()

        context= {
            "data":data,
        }
    if(rtype=="akasa"):
        Passengers = Passenger.objects.get(os_bookingId=bookingId)
        pnr = Passengers.pnr
        akasa_request = {
                "credentials": {
                    "username": "QPBOM6061B_01",
                    "password":"New@1234",
                    "domain":"EXT"}
                }
        token_akasa = akasa_data(akasa_url, '/api/nsk/v2/token',akasa_request,akasa_header={"Content-Type":"application/json"})
        akasa_token=token_akasa.json()
        akasa_token = akasa_token['data']['token']
        akasa_url_new= "https://tbnk-reyalrb.qp.akasaair.com/api/nsk/v1/booking/retrieve/byRecordLocator/"+pnr
        retrieve_res = requests.get(akasa_url_new, data="NULL", headers={"Authorization":akasa_token})
        retrieve = retrieve_res.json()
        akasa_url_new ="https://tbnk-reyalrb.qp.akasaair.com/api/nsk/v1/booking/journeys"
        delete_jour = requests.delete(akasa_url_new, data="NULL", headers={"Authorization":akasa_token})
        delete_journey = delete_jour.json()
        akasa_url_new="https://tbnk-reyalrb.qp.akasaair.com/api/nsk/v1/booking"
        get_pan = requests.get(akasa_url_new, data="NULL", headers={"Authorization":akasa_token})
        get_panalty = get_pan.json()
        print(get_panalty)
        due_amount= get_panalty['data']['breakdown']['balanceDue']
        payment_key = get_panalty['data']['payments'][0]['paymentKey']
        print(due_amount,payment_key)
        akasa_request = {
            "parentPaymentKey": payment_key,
            "amount": due_amount,
                "paymentFields": {  
                    "ACCTNO": "QPBOM6061B",
                    "AMOUNT": due_amount
                },
                "currencyCode": "INR",
                "paymentMethodCode": "AG",
                "accountTransactionCode": "CXL"
        }
        akasa_url_new="https://tbnk-reyalrb.qp.akasaair.com/api/nsk/v4/booking/payments/refunds"
        refund = requests.post(akasa_url_new, data=json.dumps(akasa_request), headers={"Authorization":akasa_token})
        get_refund = refund.json()
        print(get_refund)
        akasa_url_new="https://tbnk-reyalrb.qp.akasaair.com/api/nsk/v3/booking"
        commit = requests.put(akasa_url_new, data="NULL", headers={"Authorization":akasa_token})
        commit_booking = commit.json()
        print(commit_booking)
        akasa_url_new="https://tbnk-reyalrb.qp.akasaair.com/api/nsk/v1/booking"
        state = requests.get(akasa_url_new, data="NULL", headers={"Authorization":akasa_token})
        get_state = state.json()
        print(get_state)
        context= {
            "data":get_state,
        }

    return render(request, "main.html", context)



def get_data(request):
    login_user = request.user

    if not login_user.is_authenticated:
        return JsonResponse({'status':False, 'msg':"User is not logged In!"})

    login_user = request.user
    passengers = list(Passenger.objects.filter(user=login_user)).values()
    # return render(request, "online_savaari/booking-history.html", {'passenger':passengers,
                                                                #    'passengerflight':passengerflights,
                                   
                                                                #    'passangerare':passangerares,})
    return JsonResponse({'passengers': passengers}, safe=False) 



def GeneratePDF(request):
    booking_id = request.GET.get('bookingId')
    print(booking_id)

    search_request = {
        "bookingId" : booking_id
    }
    result = flight_data(api_url, apikey, '/oms/v1/booking-details',search_request)
    data=result.json()


    context = {
        'data': data,
    }
    template = get_template('invoice.html')
    html = template.render(context)
    return HttpResponse(html)

def string_to_ordereddict(txt):

    from collections import OrderedDict
    import re

    tempDict = OrderedDict()

    od_start = "OrderedDict([";
    od_end = '])';

    first_index = txt.find(od_start)
    last_index = txt.rfind(od_end)

    new_txt = txt[first_index+len(od_start):last_index]

    pattern = r"(\(\'\S+\'\,\ \'\S+\'\))"
    all_variables = re.findall(pattern, new_txt)

    for str_variable in all_variables:
        data = str_variable.split("', '")
        key = data[0].replace("('", "")
        value = data[1].replace("')", "")
        #print "key : %s" % (key)
        #print "value : %s" % (value)
        tempDict[key] = value

    #print tempDict
    #print tempDict['title']

    return tempDict
import signal
class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

from collections import OrderedDict
@api_view(["GET","POST"])
def newinvoice(request):
    sdata = None
    src = None
    dest = None
    airline_name = None
    flight_status = None
    login_user = request.user
    booking_id = request.GET.get('bookingId')
    adata = None
    data = None
    p_data = None
    os_bookingId = None
    pnr = None
    baggage = False
    meal= None
    amount = None
    seat= None
    ticketnumber = None
    flight_status = None
    db_data =False
    # Change the behavior of SIGALRM
    # signal.signal(signal.SIGALRM, timeout_handler)
      
    search_request = {
        "bookingId" : booking_id
    }
     # Start the timer. Once 5 seconds are over, a SIGALRM signal is sent.
    # signal.alarm(5)
    try:
        result = flight_data(api_url, apikey, '/oms/v1/booking-details',search_request)
        print(result)
    except:
        print("hello")
    # else:
    #     # Reset the alarm
    #     signal.alarm(0) 
    p_data = list(Passenger.objects.filter(user=login_user,bookingId=booking_id).values())
    for x in p_data:
        pnr =  x['pnr']
    
    akasa_list = list(Akasa_token.objects.filter(user=login_user,bookingId=booking_id).values())
    # return JsonResponse(akasa_list, safe=False)

    if len(akasa_list) > 0:
        akasa_request = {
                "credentials": {
                    "username": "QPBOM6061B_01",
                    "password":"Jan@2023",
                    "domain":"EXT"}
                }
        token_akasa = akasa_data(akasa_url, '/api/nsk/v2/token',akasa_request,akasa_header={"Content-Type":"application/json"})
        akasa_token=token_akasa.json()
        return Response(akasa_token)
        akasa_token = akasa_token['data']['token']
        pnr = Passenger.objects.filter(user=login_user,bookingId=booking_id).values().latest('id')['pnr']
        akasa_endpoint = '/api/nsk/v1/booking/retrieve/byRecordLocator/' + pnr
        akasaa_pay = akasa_details(akasa_url, akasa_endpoint, akasa_request,akasa_header={"Authorization":akasa_token})
        adata = akasaa_pay.json()
        p_data = list(Passenger.objects.filter(user=login_user,bookingId=booking_id).values())
        # print(p_data)
        i_ins = 0
        baggage = None
        meal = None
        seat = None
        ticketnumber = None
        if len(p_data) > i_ins:
            if p_data[i_ins]['insurance_pdf']:
                data['itemInfos']['AIR']['travellerInfos'][i_ins]['insurance_pdf'] = json.loads(json.loads(json.dumps(p_data[i_ins]['insurance_pdf'])))
                # print(json.loads(json.loads(p_data[i_ins]['insurance_pdf'])))
        p_data = list(Passenger.objects.filter(user=login_user,bookingId=booking_id).values())
        for x in p_data:
            os_bookingId = x['os_bookingId']
            amount = x['total_fare']
        i_ins += 1 

        context= {
            "data":data,
            "db_data":db_data,
            'jsondata': json.dumps(data),
            'pdata': p_data,
            "sdata":sdata,
            "adata": adata,
            "jsonsdata": json.dumps(sdata),
            "src":src,
            "dest":dest,
            "flight_status":flight_status,
            "airline_name":airline_name,
            "os_bookingId" : os_bookingId,
            "pnr" : pnr,
            "baggage":baggage,
            "seat":seat,
            "meal":meal,
            'amount':amount,
            "ticketnumber":ticketnumber,
            "flight_status":flight_status,
        }
        # return Response(context)
        return render(request, "online_savaari/booking-invoice.html", context)
    
    data=result.json()
    print(data)   
    with open("data.txt", "w") as file:
        file.write(str(data))
        file.close()
    flight_number_second = None 
    if (data['status']['success'] == True):
        for a in data['itemInfos']['AIR']['travellerInfos']:
            first_name = a['fN']
            last_name = a['lN']
        for i in data['itemInfos']['AIR']['tripInfos']:
            origin_airport_code = i['sI'][0]['da']['code']
            departure_datetime = i['sI'][0]['dt']
            datetime =  departure_datetime.split("T")
            departure_date_first= datetime[0]
            try:
                arrival_datetime = i['sI'][1]['dt']
                destination_airport_code=i['sI'][1]['aa']['code']
                datetime =  arrival_datetime.split("T")
                departure_date_second= datetime[0]
                flight_number_first = i['sI'][0]['fD']['fN']
                flight_number_second = i['sI'][1]['fD']['fN']
                flight_code = i['sI'][0]['fD']['aI']['code']
                date_time_str = departure_date_first.split("-")
                yy = int(date_time_str[0])
                mm = int(date_time_str[1])
                dd = int(date_time_str[2])
                travelDateseries = date(yy,mm,dd)
                departure_date_first= travelDateseries.strftime("%d %b %Y")
                date_time_str = departure_date_second.split("-")
                yy = int(date_time_str[0])
                mm = int(date_time_str[1])
                dd = int(date_time_str[2])
                travelDateseries = date(yy,mm,dd)
                departure_date_second= travelDateseries.strftime("%d %b %Y")
                qr_content = last_name+"/"+first_name+" "+pnr+" "+departure_date_first+" "+departure_date_second+" "+flight_code+" "+flight_number_first+" "+flight_number_second+" "+origin_airport_code+" "+destination_airport_code
                print(qr_content)
                url = pyqrcode.create(qr_content)
                # url.svg("myqr.svg", scale = 8)
                url.png('static/main/images/ticket_qr/'+str(request.user)+'.png', scale = 6)
                print("hi")
            except:
                print("hello")
            for a in i['sI']:
                airline_name= a['fD']['aI']['name']
                origin_airport = a['da']['name']
                destination_airport = a['aa']['name']
                destination_airport_code=a['aa']['code']
                flight_code = a['fD']['aI']['code']
                flight_number = a['fD']['fN']
                departure_datetime = a['dt']
                datetime =  departure_datetime.split("T")
                departure_time = datetime[1]
                departure_date= datetime[0]
                arrival_datetime = a['at']
                datetime =  arrival_datetime.split("T")
                arrival_time = datetime[1]
                arrival_date= datetime[0]
                duration= a['duration']
                stop =a['stops']
            if (flight_number_second == None):
                print("yes")
                date_time_str = departure_date.split("-")
                yy = int(date_time_str[0])
                mm = int(date_time_str[1])
                dd = int(date_time_str[2])
                travelDateseries = date(yy,mm,dd)
                departure_date= travelDateseries.strftime("%d %b %Y")
                qr_content = last_name+"/"+first_name+" "+pnr+" "+departure_date+" "+flight_code+" "+flight_number+" "+origin_airport_code+" "+destination_airport_code
                print(qr_content)
                url = pyqrcode.create(qr_content)
                # url.svg("myqr.svg", scale = 8)
                url.png('static/main/images/ticket_qr/'+str(request.user)+'.png', scale = 6)


        base_price = data['itemInfos']['AIR']['totalPriceInfo']['totalFareDetail']['fC']['BF']
        total_fare = data['itemInfos']['AIR']['totalPriceInfo']['totalFareDetail']['fC']['TF']
        taf = total_fare - base_price
        taf = round(taf,2)
        email = data['order']['deliveryInfo']['emails'][0]
        mobile = data['order']['deliveryInfo']['contacts'][0]
        flight_status = data['order']['status']
        pnr = None
        baggage = None
        meal = None
        seat = None
        ticketnumber = None
        p_data = list(Passenger.objects.filter(user=login_user,bookingId=booking_id).values())
        # print(p_data)
        i_ins = 0
        for a in data['itemInfos']['AIR']['travellerInfos']:
            if len(p_data) > i_ins:
                if p_data[i_ins]['insurance_pdf']:
                    data['itemInfos']['AIR']['travellerInfos'][i_ins]['insurance_pdf'] = json.loads(json.loads(json.dumps(p_data[i_ins]['insurance_pdf'])))
                    # print(json.loads(json.loads(p_data[i_ins]['insurance_pdf'])))

            if('pnrDetails' in a): 
                res= a['pnrDetails']
                pnr = list(res.values())[0]
            if('ssrBaggageInfos' in a): 
                res = a['ssrBaggageInfos']
                baggage_list = list(res.values())[0]
                baggage = baggage_list['desc']
            if('ssrMealInfos' in a): 
                res = a['ssrMealInfos']
                meal_list = list(res.values())[0]
                meal = meal_list['desc']
            if('ssrSeatInfos' in a): 
                res = a['ssrSeatInfos']
                seat_list = list(res.values())[0]
                seat = seat_list['code']
            if('ticketNumberDetails' in a): 
                res = a['ticketNumberDetails']
                ticketnumber = list(res.values())[0]

            title = a['ti']
            first_name = a['fN']
            last_name = a['lN']
            # date_of_birth = a['dob']
            passenger_type = a['pt']

            
            p_data = list(Passenger.objects.filter(user=login_user,bookingId=booking_id).values())
            # print(p_data)
            for x in p_data:
                os_bookingId = x['os_bookingId']
                amount = x['total_fare']
                # print(os_bookingId)
            i_ins += 1
    else:
        grp = find_group(request.user)
        if(grp == 'Agent'):
            search_series = {
                        "Username":"9555202202",
                        "Password":"9800830000@api"
                    }
        token_series = series_data(series_url, '/login',search_series,header={"api-key":api_key, "Content-Type":"application/json"})
        series_token=token_series.json()
        token = series_token['token']
        print("token",token)

        header =  {"api-key":api_key,"Authorization":token, "Content-Type":"application/json"}
        seriesurl= "https://omairiq.azurewebsites.net/ticket?booking_id="+booking_id
        details = requests.get(seriesurl, headers=header)
        sdata = details.json()
        print(sdata)
        flight_status = sdata['status']
        print(flight_status,"flight_status")
        route = sdata['data']['sector']
        route = route.split(" // ")
        paxdetail = sdata['data']['passenger_details']['Adult'][0]['Name']
        paxdetail = paxdetail.split(" ")
        title= paxdetail[0]
        title = title.replace(".","")
        first_name = paxdetail[1]
        last_name = paxdetail[2]
        pnr = sdata['data']['pnr']
        base_price = sdata['data']['total_amount']
        airline_name = sdata['data']['airline']
        departure_time = sdata['data']['departure_time']
        arrival_time = sdata['data']['arrival_time']
        src = route[0]
        dest = route[1]
        total_fare = sdata['data']['total_amount']
        taf = 0
        time_cal = arrival_time.split(":")
        hr = int(time_cal[0])
        mins = int(time_cal[1])
        baggage =None
        seat = None
        seat = None
        meal = None
        ticketnumber = None
        insurance = None
        amount = base_price
        osn_id = randint(1000000000, 9999999999)
        osn_id = str(osn_id)
        os_bookingId = 'OS'+osn_id
        print(os_bookingId)
        p_data = list(Passenger.objects.filter(user=login_user,bookingId=booking_id).values())
            # print(p_data)
        with open("static/flight/airport_list.json", "r") as f:
            airport = json.loads(f.read())
        l = []
        k = []
        for i in airport:
            if (i['city'] == src):
                origin_airport_code = i['code']
            if (i['city'] == dest):
                destination_airport_code = i['code']

        for x in p_data:
            last_name = x['last_name']
            first_name = x['first_name']
            pnr = x['pnr']
            departure_date = x['departure_date']
            flight_code = x['flight_code']
            flight_number = x['flight_number']
            origin_airport = x['origin_airport']
            destination_airport = x['destination_airport']
        qr_content = last_name+"/"+first_name+" "+pnr+" "+str(departure_date)+" "+flight_code+" "+flight_number+" "+origin_airport_code+" "+destination_airport_code
        print(qr_content)
        url = pyqrcode.create(qr_content)
        # url.svg("myqr.svg", scale = 8)
        url.png('static/main/images/ticket_qr/'+str(request.user)+'.png', scale = 6)
        print("hi")
    # except:
    #     db_data = (Passenger.objects.filter(user=login_user,bookingId=booking_id).values()).latest("id")
    #     print(db_data)
    #     sdata = False
    #     data = False

    akasa_list = list(Akasa_token.objects.filter(user=login_user,bookingId=booking_id).values())
    # return JsonResponse(akasa_list, safe=False)

    if len(akasa_list) > 0:
        akasa_request = {
                "credentials": {
                    "username": "QPBOM6061B_01",
                    "password":"New@1234",
                    "domain":"EXT"}
                }
        token_akasa = akasa_data(akasa_url, '/api/nsk/v2/token',akasa_request,akasa_header={"Content-Type":"application/json"})
        akasa_token=token_akasa.json()
        akasa_token = akasa_token['data']['token']
        pnr = Passenger.objects.filter(user=login_user,bookingId=booking_id).values().latest('id')['pnr']
        akasa_endpoint = '/api/nsk/v1/booking/retrieve/byRecordLocator/' + pnr
        akasaa_pay = akasa_details(akasa_url, akasa_endpoint, akasa_request,akasa_header={"Authorization":akasa_token})
        adata = akasaa_pay.json()     
        p_data = list(Passenger.objects.filter(user=login_user,bookingId=booking_id).values())
        # print(p_data)
        i_ins = 0
        baggage = None
        meal = None
        seat = None
        ticketnumber = None
        if len(p_data) > i_ins:
            if p_data[i_ins]['insurance_pdf']:
                data['itemInfos']['AIR']['travellerInfos'][i_ins]['insurance_pdf'] = json.loads(json.loads(json.dumps(p_data[i_ins]['insurance_pdf'])))
                # print(json.loads(json.loads(p_data[i_ins]['insurance_pdf'])))
        p_data = list(Passenger.objects.filter(user=login_user,bookingId=booking_id).values())
        for x in p_data:
            os_bookingId = x['os_bookingId']
            amount = x['total_fare']
        i_ins += 1 

    context= {
        "data":data,
        "db_data":db_data,
        'jsondata': json.dumps(data),
        'pdata': p_data,
        "sdata":sdata,
        "adata": adata,
        "jsonsdata": json.dumps(sdata),
        "src":src,
        "dest":dest,
        "flight_status":flight_status,
        "airline_name":airline_name,
        "os_bookingId" : os_bookingId,
        "pnr" : pnr,
        "baggage":baggage,
        "seat":seat,
        "meal":meal,
        'amount':amount,
        "ticketnumber":ticketnumber,
        "flight_status":flight_status,
    }
    # return Response(context)
    return render(request, "online_savaari/booking-invoice.html", context)

def newbooking(request):
    login_user = request.user

    if not login_user.is_authenticated:
        return JsonResponse({'status':False, 'msg':"User is not logged In!"})
    

    bookingId = request.GET.get('bookingid', None)
    cust1 = Product.objects.filter(bookingId=bookingId)
    cust1.isBooked = True
    product=Product.objects.filter(bookingId=bookingId)
    lastproduct = product.latest('id')
    traveller=Product_traveller.objects.filter(product=lastproduct).all()
    search_request ={
        "bookingId": bookingId,

        "paymentInfos": [
            {
            "amount": product.values()[0]['api_amount']
            
            }
        ],
        "gstInfo": {
            "gstNumber": None,
            "email": None,
            "registeredName": None,
            "mobile": None,
            "address":None,
        },

        "deliveryInfo": {
            "emails": [
            product.values()[0]['delivery_email']
            ],
            "contacts": [
            product.values()[0]['phone']
            ]
        }
    }
    t = []
    for trav in traveller.values():
        tr = {
        "ti": trav['title'],
        "fN": trav['first_name'],
        "lN": trav['last_name'],
        "pt": trav['passenger_type'],
        "dob": trav['date_of_birth'],
        "pNum" :trav['passport_no'],
        "eD" : trav['passport_ed'],
        "pid" : trav['passport_issue_date'],
        }

        seat = Ssrseat.objects.filter(traveller=Product_traveller.objects.get(id=trav['id'])).values()
        bag = Ssrbagg.objects.filter(traveller=Product_traveller.objects.get(id=trav['id'])).values()
        meal = Ssrmeal.objects.filter(traveller=Product_traveller.objects.get(id=trav['id'])).values()
        if bag:
            tr["ssrBaggageInfos"] = [
                {
                    "key": bag[0].bag_id,
                    "code": bag[0].bag_code
                    }
                ]
        if meal:
            tr["ssrMealInfos"] = [
                    {
                    "key": meal[0].meal_id,
                    "code": meal[0].meal_cod
                    }
                ],
        if seat:
            tr["ssrSeatInfos"] = [
            {
                "key": seat[0].seat_id,
                "code": seat[0].seat_code
                }
            ]
        t.append(tr)
    search_request["travellerInfo"] = t

    # result = flight_data(api_url, apikey, '/oms/v1/air/book',search_request)
    # data=result.json()
    # print(data)        
    return JsonResponse({"status": "test"})



def send_ticket_email(request):
    
    
    
    subject = 'Cravings & balloons pedido confirmado'

    html_message = render_to_string('ticket_template.html', {'Sender_Address': '*********@gmail.com'})
    plain_message = strip_tags(html_message)

    email = EmailMultiAlternatives(
        subject,
        plain_message,
        '*********@gmail.com',
        ['dishaarora1996@gmail.com'],
    )
    email.attach_alternative(html_message, 'text/html')
    email.send()
        
    return HttpResponse('Email Sent successfully')