import datetime
from datetime import date
import json
from urllib import response
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Customer , Agent ,CorporateCust
from django.contrib.auth.hashers import check_password ,make_password
from flight.models import Passenger, Search_History
from adminpanel.models import *
from api.serializers import UserSerializer,AgentSerializer,CustomerSerializer,CorporateCustSerializer
from rest_framework.decorators import api_view
from wallet.models import *
import razorpay
import string, random
from random import randint
from django.http import JsonResponse
from easebuzz_lib.easebuzz_payment_gateway import Easebuzz
import string, random
from hashlib import sha512
from django.views.decorators.csrf import csrf_exempt
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import os
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages #import messages
from django.db.models import Count
from django.http import JsonResponse

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

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					smtpHost = "smtp.gmail.com"
					smtpPort = 587
					mailUname = 'no-reply@onlinesavaari.com'
					mailPwd = 'afbzoctjmpppkwvk'
					fromEmail = 'no-reply@onlinesavaari.com'
					attachmentFpaths = ["flight/logo.png"]
					recepientsMailList = [user.email]
					mailSubject = "Password Reset Requested"
					email_template_name = "online_savaari/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					mailContentHtml = render_to_string(email_template_name, c)
					print(mailContentHtml)
					try:
						sendEmail(smtpHost, smtpPort, mailUname, mailPwd, fromEmail,
							  mailSubject, mailContentHtml, recepientsMailList, attachmentFpaths)
						
					except BadHeaderError:

						return HttpResponse('Invalid header found.')
						
					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect ("index")
			messages.error(request, 'An invalid email has been entered.')
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="online_savaari/password_reset.html", context={"password_reset_form":password_reset_form})

def find_group(user):
	if user.groups.filter(name='Agent').exists():
		return 'Agent'
	elif user.groups.filter(name='Corporate').exists():
		return 'Corporate'
	else:
		return 'Customer'

def index(request):
	banner = Banner.objects.latest('id')
	banner1 = SmallBanner1.objects.latest('id')
	banner2 = SmallBanner2.objects.latest('id')
	print(banner,banner1,banner2)
	big_banner = banner.big_banner 
	small_banner1 = banner1.small_banner1 
	small_banner2 = banner2.small_banner2
	print(big_banner,small_banner1,small_banner2)
	commission_data = list(Commission.objects.all().values())
	print(commission_data)
	for x in commission_data:
		print(x['start_date'])
		print(x['end_date'])
	# Insert users data in customer table for google login
	if request.user.is_authenticated:
		login_user = request.user
		print(login_user)
		if Customer.objects.filter(user = login_user.id).exists() or login_user.is_staff:
			pass
		else:
			my_user = User.objects.get(username = login_user.username)
			my_user.username = login_user.email
			my_user.save()
			Customer.objects.create(user=login_user,first_name=login_user.first_name, last_name=login_user.last_name, email= login_user.email)

	d = date.today()
 
	# return JsonResponse({"promocode": d})
	# get promocode
	promocode = Promocode.objects.filter(end_date__gt=d)
 
	# get domestic $ international flights list
	domestic = []
	international, international_code = [], []
	with open("static/flight/airport_list.json", "r") as f:
		airport = json.loads(f.read())
		
		for x in airport:
			if x['country'] == 'India':
				domestic.append({'code': x['code'], 'city': x['city']})
			else:
				international.append({'code': x['code'], 'city': x['city']})
				international_code.append(x['code'])
		all_flight = domestic + international
	
	flight_search_list = list(Search_History.objects.values('origin', 'destination').annotate(total=Count('id')))
	
	international_flight_list=[]
	domestic_flight_list=[]
	
	max_domestic_search = []
	price_list = [2499, 3499, 2999]
	count = 0
	
	for x in flight_search_list:
		if x['origin'] in international_code or x['destination'] in international_code:
			international_flight_list.append(x)
		else:
			domestic_flight_list.append(x)
	
	# search 3 popular domestic flights
	length = 3 if len(domestic_flight_list) > 3 else len(domestic_flight_list)
	
	while count < length:
		max_search_item = findHighestSearchFlight(domestic_flight_list)
		for x in domestic:
			if max_search_item['origin'] == x['code']:
				max_search_item['origin_city'] = x['city']
				for x in domestic:
					if max_search_item['destination'] == x['code']:
						max_search_item['dest_city'] = x['city']
						max_search_item['price'] = price_list[count]
						max_domestic_search.append(max_search_item)
						domestic_flight_list.remove(max_search_item)
						count+=1
			else:
				continue
	
	# search 3 popular international flights
	max_international_search = []
	price_list = [14499, 15999, 16499]
	count = 0
	
	length = 3 if len(international_flight_list) > 3 else len(international_flight_list)
	
	while count < length:
		max_search_item2 = findHighestSearchFlight(international_flight_list)

	
		for x in all_flight:
			if max_search_item2['origin'] == x['code']:
				max_search_item2['origin_city'] = x['city']
				for x in international:
					if max_search_item2['destination'] == x['code']:
						max_search_item2['dest_city'] = x['city']
						max_search_item2['price'] = price_list[count]
						max_international_search.append(max_search_item2)
						international_flight_list.remove(max_search_item2)
						count+=1
			else:
				continue
 

	return render(request, "online_savaari/index.html", context={'big_banner':big_banner,'small_banner':small_banner1,'small_banner1':small_banner2,'max_domestic_search': max_domestic_search, 'max_international_search': max_international_search, 'promocode': promocode})


def findHighestSearchFlight(flight_search_list):
		maxSearchItem = max(flight_search_list, key=lambda x:x['total'])
		return maxSearchItem



def agencysignup(request):
	return render(request, "online_savaari/agency-signup.html", context={})

def deposit_request_user(request):
	if (request.method == "POST"):
		deposit_type = request.POST.get('deposit_type')
		amount = request.POST.get('Amount')
		bank_name = request.POST.get('bank_name')
		deposite_branch = request.POST.get('deposite_branch')
		deposit_slip = request.FILES.get('deposit_slip')
		trasaction_num = request.POST.get('trasaction_num')
		if(trasaction_num == ""):
			transaction_number = randint(1000000000, 9999999999)
			osn_id = str(transaction_number)
			trasaction_num = 'USER'+osn_id
		cust1=Deposit.objects.create(user=request.user,dep_status="Not Approve",email_or_phone=request.user.email,amount=amount,deposit_type=deposit_type,bank_name=bank_name,deposite_branch=deposite_branch,trasaction_num=trasaction_num,deposit_slip=deposit_slip)
			
	return render(request, "online_savaari/ecash.html", context={})

def about(request):
	return render(request, "online_savaari/about.html", context={})

def details(request):
	return render(request, "online_savaari/details.html", context={})

def listing(request):
	return render(request, "online_savaari/listing.html", context={})

def invoice(request):
	return render(request, "online_savaari/invoice.html", context={})

def payments(request):
	return render(request, "online_savaari/wallet-payments.html", context={})

@csrf_exempt
def Pay_success(request, id):
	t = id.split(":")[0]
	if t == "hotel":
		return render(request, "savaari_hotel/Hotel_Pay_success.html", {})
	context = {
		'bookingId': id,
	}
	return render(request, "online_savaari/Pay_success.html", context)

@csrf_exempt
def wallet_success(request, id):
	context = {
		'paymentid': id,
	}
	return render(request, "online_savaari/Pay_success.html", context)

@csrf_exempt
def Pay_failed(request, id):
	return render(request, "online_savaari/Pay_failed.html", context={'bookingId':id})

def privacy(request):
	return render(request, "online_savaari/privacy.html", context={})
@api_view(["GET", "POST"])
def cancel(request):
	if request.method == "GET":
		BookingId = request.GET.get('bookingId', "")

	context = {
		'bookingId': BookingId,
	}
	return render(request, "online_savaari/cancel.html", context=context)

def faq(request):
	return render(request, "online_savaari/faq.html", context={})

def response(request):
	return render(request, "online_savaari/response.html", context={})

import random
def encrypt_pay(pay_hash):
	size = 32
	res = bytes(pay_hash, 'utf-8')
	hashed = sha512(res).hexdigest()
	return hashed

def savaari_cash(request):
	if AgentCredit.objects.filter(agent__user=request.user).exists():
		credit_amount = AgentCredit.objects.filter(agent__user=request.user).last().credit_balance
		credit_history = AgentCredit.objects.filter(agent__user=request.user)

	else:
		credit_amount = 0
		credit_history = None
	amount = 0
	grp = find_group(request.user)

	# if grp ==  'Agent' or grp == 'Corporate':
	# 	MERCHANT_KEY = "DZU9JYGI3O";
	# 	SALT = "OXODUCPA08";
	# 	ENV = "prod"
	# else:
	# 	MERCHANT_KEY = "M3YR2SW37O";
	# 	SALT = "HHWBRBCYTT";
	# 	ENV = "prod"

	MERCHANT_KEY = "2PBP7IABZ2";
	SALT = "DAH88E3UWQ";
	ENV = "test"

	if request.method == "POST":
		if request.POST.get('ajax') == 'ajax-payment-done':
			payment_id = request.POST.get('payment_id')
			amount = request.POST.get('amount')
			# return JsonResponse(request.POST)
			print("main")
			if(payment_id):
				transaction_status = 'Success'
			else:
				transaction_status = 'Fail'

			last_balance_added = date.today() 
			transaction_date = date.today()
			if(transaction_status == 'Success'):
				print(amount)
				wallet_data = (WalletDetails.objects.filter(username=request.user).values()).latest('id')
				balance = float(wallet_data['wallet_balance']) + float(amount)
				print(wallet_data)
				if wallet_data['canadd']:
					cust1=WalletDetails.objects.create(wallet_balance=balance,transaction_id=payment_id,username=request.user,email=request.user,amount=amount,last_balance_added=last_balance_added,trasc_type='Credit',transaction_status=transaction_status)
					return JsonResponse({'status': 'false'})
			
			return JsonResponse({'status': 'true'})
		if request.POST.get('payment_type') == 'debit':
			amount = request.POST.get('amount', 0)
			with open("data1.txt", "w") as file:
				file.write(str(amount))
				file.close()
			payment_id = request.POST.get('payment_id', None)
			last_balance_added = date.today()
			wallet_data = (WalletDetails.objects.filter(username=request.user).values()).latest('id')
			balance = float(wallet_data['wallet_balance']) - float(amount)
			if(balance > 0 and amount != 0):
				cust1=WalletDetails.objects.create(wallet_balance=balance,transaction_id=payment_id,username=request.user,email=request.user,amount=amount,last_balance_added=last_balance_added,trasc_type='Debit',transaction_status='Success')
				return JsonResponse({'status': 'true'})
			elif(balance <= 0):
				return JsonResponse({'status': 'false'})

			return JsonResponse(wallet_data)
		return redirect(request.path)
		if request.POST.get('payment_type') == 'agentcredit':
			amount = request.POST.get('amount', 0)
			with open("spice_logon.txt", "w") as file:
				file.write(str(amount))
				file.close()
			payment_id = request.POST.get('payment_id', None)
			last_balance_added = date.today()
			credit_data = (AgentCredit.objects.filter(agent__user=request.user).values()).latest('id')
			balance = float(credit_data['amount']) - float(amount)
			if(balance > 0 and amount != 0):
				cust1=a = AgentCredit(agent__user=request.user,duduct_date=date.today,trasaction_num='CREDIT'+str(randint(1000000000, 9999999999)),status="Debit",amount=balance,credit_balance=amount)
				return JsonResponse({'status': 'true'})
			elif(balance <= 0):
				return JsonResponse({'status': 'false'})

			return JsonResponse(credit_data)
		return redirect(request.path)
		
	if request.method == 'GET':
		if request.GET.get('ajax') == 'ajax':
			print(MERCHANT_KEY, SALT)
			amt = request.GET.get('amount', 50000)
			amt = float(amt)
			txnid = ''.join(random.choices(string.ascii_uppercase +
							 string.digits, k = 15))
			first_name = 'krishna'
			email = str(request.user)
			#pay_hash = '2PBP7IABZ2'+'|'+ txnid+'|'+str(amt)+'|'+'Online Savaari'+'|'+first_name+'|'+email+'|||||||||||'+'DAH88E3UWQ'
			pay_hash = MERCHANT_KEY +'|'+ txnid+'|'+str(amt)+'|'+'Online Savaari'+'|'+'krishna'+'|'+'krishnamahato223@gmail.com'+'|||||||||||'+SALT
			hashed_form = encrypt_pay(pay_hash)
			print(hashed_form)
			amt = str(amt)
				  
			ENV = "test"; 
			easebuzzObj = Easebuzz(MERCHANT_KEY, SALT, ENV)
			postDict = {
				'txnid': txnid,
				'firstname': 'krishna',
				'phone': '9873344868',
				'email': 'krishnamahato223@gmail.com',
				'amount': amt,
				'productinfo': 'Online Savaari',
				'surl': f'http://onlinesavaari.website/wallet_success/{txnid}:{amt}/',
				'furl': f'http://onlinesavaari.website/Pay_failed/',
				'hash': hashed_form
			}

			final_response = easebuzzObj.initiatePaymentAPI(postDict)
			result = json.loads(final_response)
			print(result)
			if result['status'] == 1:
				wallet_data = (WalletDetails.objects.filter(username=request.user)).latest('id')
				wallet_data.canadd = True
				wallet_data.save()
				print(wallet_data)
				print("Success")
				print(result)
				# note: result['data'] - contain payment link. 
				return JsonResponse(result)
			else:
				return JsonResponse(result)
			
		if request.GET.get('ajax') == 'payment':
			MERCHANT_KEY = MERCHANT_KEY
			SALT = SALT
			ENV = "test" 
			easebuzzObj = Easebuzz(MERCHANT_KEY, SALT, ENV)
			txnid = request.GET.get('txnid')
			amt = request.GET.get('amount')
			amt = float(amt)
			amt = str(amt)
			email = request.GET.get('email')
			postDict = {
			  'txnid':txnid,
			  'amount':amt,
			  'phone':'9873344868',
			  'email':email
			}

			final_response = easebuzzObj.transactionAPI(postDict)
			final_response = json.loads(final_response)
			amount = final_response['msg']['net_amount_debit']
			transaction_status = final_response['msg']['status']
			transaction_mode = final_response['msg']['mode']
			transaction_id = final_response['msg']['easepayid']
			note = final_response['msg']['error_Message']
			email = final_response['msg']['email']

		data = list(WalletDetails.objects.filter(username=request.user).values())
		if len(data) == 0:
			wallet_activated_on = date.today()
			curl = WalletDetails.objects.create(username=request.user,email=request.user,wallet_activated_on=wallet_activated_on,wallet_balance=0)
			data = list(WalletDetails.objects.filter(username=request.user).values())
		wallet_data = (WalletDetails.objects.filter(username=request.user).values()).latest('id')
		balance = float(wallet_data['wallet_balance'])
		print(balance)
		if amount != 0:
			wallet_balance = float(balance) + float(amount)
			cust1=WalletDetails.objects.create(username=request.user,email=request.user.email,amount=amount,wallet_balance=wallet_balance,trasc_type='Credit',transaction_mode=transaction_mode,transaction_status=transaction_status,transaction_id=transaction_id,note=note)
		
		# if data == []:
		#     data = None
		context = {
			'data' : data,
			'balance' : balance,
			'credit_amount' : credit_amount,
			'credit_history' : credit_history,
		}
		return render(request, "online_savaari/ecash.html", context)

def seatmap(request):
	return render(request, "online_savaari/seatmap.html", context={})
def contact(request):
	return render(request, "online_savaari/contact.html", context={})
	
def term(request):
	return render(request, "online_savaari/terms.html", context={})


def profile(request):
	
	error_mgs = None
	success_mgs = None
	print(request.method)
	# response=requests.get('http://127.0.0.1:8000/api/register_customer/').json()
	if request.method == 'POST':
		id = request.user.id
		edit_first_name = request.POST.get('edit_first_name')
		edit_last_name = request.POST.get('edit_last_name')
		edit_email = request.POST.get('edit_email')
		edit_phone = request.POST.get('edit_phone')
		edit_old_password = request.POST.get('edit_old_password')
		edit_new_password = request.POST.get('edit_new_password')
		edit_confirm_password = request.POST.get('edit_confirm_password')
		edit_address = request.POST.get('edit_address')
		edit_State = request.POST.get('edit_State')
		edit_pin = request.POST.get('edit_pin')
		edit_gstin = request.POST.get('edit_gstin')
		edit_company_name = request.POST.get('edit_company_name')
		print(edit_first_name, edit_last_name, edit_email, edit_address,
			  edit_State, edit_pin, edit_phone,edit_old_password,
			  edit_confirm_password,edit_new_password,)
		adult = request.POST.get('radio')
		passenger_first_name = request.POST.get('passenger_first_name')
		passenger_last_name = request.POST.get('passenger_last_name')
		passenger_dob = request.POST.get('passenger_dob')
		print(passenger_dob)
		try:
			birthday = datetime.strptime(passenger_dob, '%d-%m-%Y').date()
		except TypeError:
			pass

		try:
			file = request.FILES['myfile']
		except:
			file = None

		user = get_object_or_404(User, id=id)
		
		if file is not None:
			agent =  Agent.objects.get(user_id =request.user.id)
			agency_logos = request.FILES['myfile']
			agent.agency_logo=agency_logos
			agent.save()
			error_mgs = 'Details Updated !!'
			return render(request, "online_savaari/profile.html", context={'error_mgs': error_mgs,'agent':agent})
		
		
		
		user = get_object_or_404(User, id=id)
		
		try:
			print("1")
			print(edit_old_password !=None and (edit_new_password!=None and edit_confirm_password!=None))
			corporat =  CorporateCust.objects.get(user_id =request.user.id)
			if (edit_old_password != "" and (edit_new_password!="" and edit_confirm_password!="")):
				print("1-2")
				if user.check_password(edit_old_password):
					print("1-3")
					if edit_new_password == edit_confirm_password:
						print("1-4")
						user.password = make_password(edit_new_password)
						user.save()
						success_mgs = 'Your password is changed successfully!!'
						return render(request, "online_savaari/profile.html", context={'corporat':corporat,'success_mgs': success_mgs})
					else:
						print("1-5")
						error_mgs = 'Enter valid Confirm Password invalid !!'
						return render(request, "online_savaari/profile.html", context={'error_mgs': error_mgs,'corporat':corporat})
				error_mgs = 'Enter valid Old Password invalid !!'
			elif adult:
				passenger = Passenger(first_name=passenger_first_name, 
											last_name=passenger_last_name,
											passenger_type = adult,
											mobile=corporat.mobile, 
											email=corporat.email,
											date_of_birth=birthday)
				passenger.save()
				
			  
			else:
				print("1-6")
				user.first_name = edit_first_name
				user.last_name = edit_last_name
				user.username = edit_email
				user.email = edit_email
				user.save()
				corporat.email = edit_email
				corporat.mobile = edit_phone
				corporat.address = edit_address
				corporat.pincode = edit_pin
				corporat.gst_state = edit_State
				corporat.gstin = edit_gstin
				corporat.save()
				error_mgs = 'Details Updated Successfully !!'
				return render(request, "online_savaari/profile.html", context={'error_mgs': error_mgs,'corporat':corporat})
			print("1-7")
			return render(request, "online_savaari/profile.html", context={'error_mgs': error_mgs,'corporat':corporat})
		except CorporateCust.DoesNotExist:
			try:
				print("1")
				if (edit_old_password != "" and (edit_new_password!="" and edit_confirm_password!="")):
					print("1-2")
					if user.check_password(edit_old_password):
						print("1-3")
						if edit_new_password == edit_confirm_password:
							print("1-4")
							user.password = make_password(edit_new_password)
							user.save()
							success_mgs = 'Your password is changed successfully!!'
							return render(request, "online_savaari/profile.html", context={'agent':agent,'success_mgs': success_mgs})
						else:
							print("1-5")
							error_mgs = 'Enter valid Confirm Password invalid !!'
							return render(request, "online_savaari/profile.html", context={'error_mgs': error_mgs,'agent':agent})
					error_mgs = 'Enter valid Old Password invalid !!'
					
				elif adult:
					passenger = Passenger(first_name=passenger_first_name, 
											last_name=passenger_last_name,
											passenger_type = adult,
											mobile=agent.mobile, 
											email=agent.email,
											date_of_birth=birthday)
					passenger.save()
				
				else:
					print("1-6")
					user.first_name = edit_first_name
					user.last_name = edit_last_name
					user.username = edit_email
					user.email = edit_email
					user.save()
					agent.name = edit_first_name + ' ' + edit_last_name
					agent.email = edit_email
					agent.mobile = edit_phone
					agent.agency_address = edit_address
					agent.agency_name = edit_company_name
					agent.pincode = edit_pin
					agent.gst_state = edit_State
					agent.gstin = edit_gstin
					agent.save()
					error_mgs = 'Details Updated !!'
					return render(request, "online_savaari/profile.html", context={'error_mgs': error_mgs,'agent':agent})
				print("1-7")
				return render(request, "online_savaari/profile.html", context={'error_mgs': error_mgs,'agent':agent})
			except Agent.DoesNotExist:
				print("1")
				customer =  Customer.objects.get(user_id =request.user.id)
				if (edit_old_password != "" and (edit_new_password!="" and edit_confirm_password!="")):
					print("1-2")
					if user.check_password(edit_old_password):
						print("1-3")
						if edit_new_password == edit_confirm_password:
							print("1-4")
							user.password = make_password(edit_new_password)
							user.save()
							success_mgs = 'Your password is changed successfully!!'
							return render(request, "online_savaari/profile.html", context={'customer':customer,'success_mgs': success_mgs})
						else:
							print("1-5")
							error_mgs = 'Enter valid Confirm Password invalid !!'
							return render(request, "online_savaari/profile.html", context={'error_mgs': error_mgs,'customer':customer})
					error_mgs = 'Enter valid Old Password invalid !!'
					
				elif adult:
					passenger = Passenger(first_name=passenger_first_name, 
											last_name=passenger_last_name,
											passenger_type = adult,
											mobile=customer.customer,
											email=customer.email,
											date_of_birth=birthday)
					passenger.save()
				
				else:
					print("1-6")
					user.first_name = edit_first_name
					user.last_name = edit_last_name
					user.username = edit_email
					user.email = edit_email
					user.save()
					customer.email = edit_email
					customer.mobile = edit_phone
					customer.address = edit_address
					customer.pincode = edit_pin
					customer.gst_state = edit_State
					customer.gstin = edit_gstin
					customer.save()
					error_mgs = 'Details Updated !!'
					return render(request, "online_savaari/profile.html", context={'error_mgs': error_mgs,'customer':customer})
				print("1-7")
				return render(request, "online_savaari/profile.html", context={'error_mgs': error_mgs,'customer':customer})

	else:
		
		if CorporateCust.objects.filter(user_id =request.user.id).exists():
			corporat = CorporateCust.objects.get(user_id =request.user.id)
			try :
				passenger = Passenger.objects.filter(email =request.user.email).last()
			except Passenger.DoesNotExist:
				pass
			print("pass corporat")
			return render(request,'online_savaari/profile.html',context={'corporat':corporat,'passenger':passenger})
		elif Agent.objects.filter(user_id = request.user.id).exists():
			agent = Agent.objects.get(user_id = request.user.id)
			try :
				passenger = Passenger.objects.filter(email =request.user.email).last()
			except Passenger.DoesNotExist:
				pass
			print("pass agent")
			return render(request,'online_savaari/profile.html',context={'agent':agent,'passenger':passenger})
		elif User.objects.filter(id = request.user.id).exists():
			user = User.objects.get(id = request.user.id)
			try :
				passenger = Passenger.objects.filter(email =request.user.email).last()
			except Passenger.DoesNotExist:
				pass
			print("pass agent")
			return render(request,'online_savaari/profile.html',context={'user':user,'passenger':passenger})
		else:
			customer = Customer.objects.get(user_id = request.user.id)
			try :
				passenger = Passenger.objects.filter(email =request.user.email).last()
			except Passenger.DoesNotExist:
				pass
			print("pass customer")
			return render(request,'online_savaari/profile.html',context={'customer':customer,'passenger':passenger})
		
		
def dashboard(request):
	return render(request, "online_savaari/dashboard.html", context={}) 

def custlogin(request):
	error_mgs = None
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate( username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('index')
		error_mgs = 'Email or Password invalid !!'
	
	return render(request, "online_savaari/login.html", context={'error_mgs': error_mgs})

def custlogout(request):
	logout(request)
	return redirect('index')

@api_view(["GET", "POST"])
def refundclaim(request):
	login_user = request.user
	if request.method == 'POST':
		bookingId=request.POST.get('bookingId', None)
		if(bookingId != None):
			refundquery=request.POST.get('refundquery', None)
			cust1=RefundFlight.objects.create(user=login_user,Refund_bookingid=bookingId,Refund_query=refundquery)
			return redirect(request.path)

	if request.method == 'GET':
		data = list(RefundFlight.objects.filter(user=login_user).values())
		print(data)
		return render(request, "online_savaari/refundclaim.html", context={'data': data})


@api_view(["GET", "POST"])
def rescheduleclaim(request):
	login_user = request.user
	if request.method == 'POST':
		bookingId=request.POST.get('bookingId', None)
		if(bookingId != None):
			Reschedule_flight_date=request.POST.get('Reschedule_flight_date', None)
			Reschedule_query=request.POST.get('Reschedule_query', None)
			print(bookingId,Reschedule_flight_date,Reschedule_query)
			cust1=RescheduleFlight.objects.create(user=login_user,Reschedule_bookingid=bookingId,Reschedule_flight_date=Reschedule_flight_date,Reschedule_query=Reschedule_query)
			return redirect(request.path)

	if request.method == 'GET':
		bookingId=request.GET.get('bookingId', None)
		if (bookingId != None):
			status=True
		else:
			status=False
		data = list(RescheduleFlight.objects.filter(user=login_user).values())
		return render(request, "online_savaari/rescheduleclaim.html", context={'data': data, 'status':status,'bookingId': bookingId})

# corporat.email = edit_email
# corporat.mobile = edit_phone
# corporat.address = edit_address
# corporat.pincode = edit_pin
# corporat.gst_state = edit_State
# corporat.gstin = edit_gstin
# corporat.save()

# customer.email = edit_email
# customer.mobile = edit_phone
# customer.address = edit_address
# customer.pincode = edit_pin
# customer.gst_state = edit_State
# customer.gstin = edit_gstin
# customer.save()
def covid(request):
	return render(request, "online_savaari/covid.html", context={})
	

def Mobilelogin(request):
	username = list(request.POST.get('phone'))
	print(username)
	res = ''.join(random.choices(string.digits, k = 4))
	url1 = "https://www.fast2sms.com/dev/bulkV2"
	querystring = {
	"route" : "dlt",
	"sender_id" : "OSAVAR",
	"message" : "144192",
	"variables_values" : res,
	"flash" : 0,
	"numbers" : username,
	}
	
	headers = {
	"authorization":"YnqF5CyIdT2ONH9rf6U0jlGWPswaJBhiS1KXgM3bR87ptxDZczkpnzN6yVDFaKI5hBQE9eq7tTOoJYb3",
	"Content-Type":"application/json"
	}
	try:
		print(querystring)
		print(url1)
		print(headers)
		response = requests.request("POST", url1,
									headers = headers,
									params = querystring)
		print(response)
		  
		print("SMS Successfully Sent")
	except:
		print("Oops! Something wrong")
	return render(request, "online_savaari/login.html", context={})
	
def Mobilelogin(request):
	if request.method == 'POST':
		username = request.POST.get('phone')
		password = request.POST.get('password')
		print(username, password)
		# users = User.objects.get(username=username)
		# user = users.password
		
		# if check_password(password, user):
		#     login(request, users)
		# user = authenticate( username=username, password=password)
		if username is not None:
			login(request, username)
			return redirect('index')
		error_mgs = 'Email or Password invalid !!'