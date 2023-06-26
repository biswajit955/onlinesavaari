from django.shortcuts import render, redirect
from csv import DictReader
import csv
from datetime import datetime
import numpy as np
from array import array
import pandas
from .utils import *
import json
import ast
import requests
from django.http import JsonResponse
import random
from .models import *


# Create your views here.


def insurance_claim(request):
    
    with open("static/insurance/Category.csv", 'r', encoding='utf-8-sig') as f:
        dict_reader = DictReader(f)
        category_list = list(dict_reader)

    context={'category_list': category_list}
    

    return render(request, "insurance/insurance.html", context)



def insurance_policy(request):
   
    with open("static/insurance/Category.csv", 'r', encoding='utf-8-sig') as f:
        dict_reader = DictReader(f)
        category_list = list(dict_reader)

    context={'category_list': category_list}
    
    if request.method =='POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birth_date = request.POST.get('birth_date')
        passport_no = request.POST.get('passport_no', 'NA')
        pnr_no = request.POST.get('pnr_no')
        country = request.POST.get('country')
        address = request.POST.get('address', 'NA')
        pin = request.POST.get('pin', 'NA')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        total_days = request.POST.get('total_days')
        depart_from = request.POST.get('depart_from')
        going_to = request.POST.get('going_to')
        category_code = request.POST.get('category_code')
        
        
        plan_details_list = get_insurance_plan_code_name(total_days, birth_date, category_code)
        age = calculateAge(birth_date)
        # plan_code = plan_name = ''
        # day_limit =  age_limit = 0

        # selected_plan_list=[]
        # premium_plan_list = []
        # updated_plan_list=[]
        # updated_rider_list =[]
        # plan_details_list=[]
    
        
        # with open("static/insurance/Plan.csv", 'r', encoding='utf-8-sig') as f:
        #     dict_reader = DictReader(f)
        #     plan_list = list(dict_reader)
            
        #     for plan in plan_list:
        #         if plan['category_code'] == category_code:
        #             plan_code= plan['plan_code']
        #             plan_name=plan['name']
        #             dict={'plan_code': plan_code, 'plan_name': plan_name}
        #             selected_plan_list.append(dict)
        #             # print(f'selected: {selected_plan_list}')
                    
                    
        # with open("static/insurance/PremiumChart.csv", 'r', encoding='utf-8-sig') as f:
        #     dict_reader = DictReader(f)
        #     premium_chart_list = list(dict_reader)
        
        
        # data = pandas.read_csv('static/insurance/PremiumChart.csv')
        
        # age_list = data.age_limit.tolist()
        
        # age_array_list=np.array(age_list)
        # unique_age_list= np.unique(age_array_list)
        
        # age_limit = findClosestNumber(unique_age_list, age)
        
        # day_list = data.day_limit.tolist()
        
        # day_array_list=np.array(day_list)
        # unique_day_list= np.unique(day_array_list)
        # day_limit = findClosestNumber(unique_day_list, int(total_days))
        
    
        # premium_plan_list = []
        
        # for premium in premium_chart_list:
        #     if int(premium['day_limit']) == day_limit and int(premium['age_limit']) == age_limit:
        #         premium_plan_list.append(premium)
            
        # for plan in selected_plan_list:
        #     for premium_list in premium_plan_list:
        #         if premium_list['plan_code'] == plan['plan_code']:
        #             plan.update({'premium': premium_list['premium']})
        #             updated_plan_list.append(plan)  
        #             break
        
        

        # with open("static/insurance/PlanRiders.csv", 'r', encoding='utf-8-sig') as f:
        #     dict_reader = DictReader(f)
        #     rider_code_list = list(dict_reader)
        
        # for plan in updated_plan_list:
        #     for rider in rider_code_list:
        #         if rider['plan_code'] == plan['plan_code']:
        #             plan.update({'rider_code': rider['rider_code']})
        #             updated_rider_list.append(plan)
        #             break
                            
        # with open("static/insurance/RiderMaster.csv", 'r', encoding='utf-8-sig') as f:
        #     dict_reader = DictReader(f)
        #     rider_name_list = list(dict_reader)
            
        #     for plan in updated_rider_list:
        #         for rider in rider_name_list:
        #             if rider['rider_code'] == plan['rider_code']:
        #                 plan.update({'plan_description': rider['name']})
        #                 plan_details_list.append(plan)
                        
        
        
        insurance_dict={"first_name": first_name, "last_name": last_name, "email": email, "phone": phone, "address": address, "country": country, "pin": pin, "dept_date": start_date, "arr_date": end_date,"total_days": total_days,"depart_from": depart_from, "going_to": going_to, "dob": birth_date, "passport": passport_no,"pnr_no": pnr_no, "age": age, "category_code": category_code}
        
       
        
        context={'plan_list': plan_details_list,'insurance_detail': insurance_dict}                   
            
        
        return render(request, "insurance/insurance_policy.html", context)

def insurance_policy_history(request):
    insurance_policy = Insurance_Policy.objects.filter(user=request.user)
    context = {'insurance_policy': insurance_policy}
    
    return render(request, "insurance/insurance_policy_history.html", context)


def insurance_payment(request):
    if request.method == 'POST':
        ins_count= Insurance_Policy.objects.all().count() + 1
        ins_booking_id = f"SavariInc{random.randint(10000, 99999)}{ins_count}" 
        plan_detail = ast.literal_eval(request.POST.get('plan_detail'))
        insurance_detail = ast.literal_eval(request.POST.get('insurance_detail'))
        insurance_detail['booking_ref'] = ins_booking_id
        context ={
                "plan_detail": plan_detail,
                "insurance_detail": insurance_detail,
        }
        return render(request, "insurance/insurance_payment.html", context)
        


def insurance_booking(request):
    
    if request.method == 'POST':
        plan_detail = ast.literal_eval(request.POST.get('plan_detail'))
        insurance_detail = ast.literal_eval(request.POST.get('insurance_detail'))
        
        
        createXMLFile(plan_detail, insurance_detail)

        
        with open("insurance/insurance_policy.xml") as xml_file:
            xml_policy = xml_file.read() 
            data = encrypt(xml_policy)
            result = insurance(data)
            result = result.text
            result = xmltodict.parse(result)
            response = result["data"]
            if response['status'] == 'Success':
                insurance_policy = Insurance_Policy(user= request.user,
                                                    first_name=insurance_detail['first_name'],
                                                    last_name=insurance_detail['last_name'],
                                                    date_of_birth=insurance_detail['dob'],
                                                    passport_no=insurance_detail['passport'],
                                                    pnr_no=insurance_detail['pnr_no'],
                                                    country=insurance_detail['country'],
                                                    address=insurance_detail['address'],
                                                    pin_no=insurance_detail['pin'],
                                                    phone=insurance_detail['phone'],
                                                    email=insurance_detail['email'],
                                                    amount=plan_detail['premium'],
                                                    start_date=insurance_detail['dept_date'],
                                                    end_date=insurance_detail['arr_date'],
                                                    total_days=insurance_detail['total_days'],
                                                    depart_from= insurance_detail['depart_from'],
                                                    going_to=insurance_detail['going_to'],
                                                    category=insurance_detail['category_code'],
                                                    plan_code=plan_detail['plan_code'],
                                                    pdf_url=response['pdf_url'],
                                                    reference_id=insurance_detail['booking_ref'],
                                                    policy_no=response['policy_no'],
                                                    insurance_status="Success",
                                                    )
            else:
                insurance_policy = Insurance_Policy(user= request.user,
                                                    first_name=insurance_detail['first_name'],
                                                    last_name=insurance_detail['last_name'],
                                                    date_of_birth=insurance_detail['dob'],
                                                    passport_no=insurance_detail['passport'],
                                                    pnr_no=insurance_detail['pnr_no'],
                                                    country=insurance_detail['country'],
                                                    address=insurance_detail['address'],
                                                    pin_no=insurance_detail['pin'],
                                                    phone=insurance_detail['phone'],
                                                    email=insurance_detail['email'],
                                                    amount=plan_detail['premium'],
                                                    start_date=insurance_detail['dept_date'],
                                                    end_date=insurance_detail['arr_date'],
                                                    total_days=insurance_detail['total_days'],
                                                    depart_from= insurance_detail['depart_from'],
                                                    going_to=insurance_detail['going_to'],
                                                    category=insurance_detail['category_code'],
                                                    plan_code=plan_detail['plan_code'],
                                                    reference_id=insurance_detail['booking_ref'],
                                                    err_code=response['errorcode'],
                                                    err_desc=response['message'],
                                                    insurance_status="Pending",
                                                    )
                
            insurance_policy.save()
                
            
        # return JsonResponse(result, safe=True)

        return redirect('insurance_policy_history')
        
        
        # return render(request, "insurance/insurance_policy_history.html")
        
        
        


