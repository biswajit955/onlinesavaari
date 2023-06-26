from datetime import datetime
import xml.etree.ElementTree as ET
import json
import ast
import xmltodict
from Crypto.Cipher import AES
import base64
import requests

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

def calculateAge(birthDate):
    b_date = datetime.strptime(birthDate, '%Y-%m-%d')
    today = datetime.today()
    
    try:
        birthday = b_date.replace(year = today.year)
 
    # raised when birth date is February 29
    # and the current year is not a leap year
    except ValueError:
        birthday = b_date.replace(year = today.year,
                  month = b_date.month + 1, day = 1)
 
    if birthday > today:
        return today.year - b_date.year - 1
    else:
        return today.year - b_date.year


def findClosestNumber(myArr, myNumber):
    
    return min([ i for i in myArr.tolist() if i >= myNumber], key=lambda x:abs(x-myNumber))

def createXMLFile(plan_detail, insurance_detail):
    tree = ET.parse('insurance/insurance_policy.xml')
    root = tree.getroot()
    
    base_charges= float(plan_detail['premium'])

#     print(insurance_detail['firs'])
    
    for temp in root.iter('reference'):
         temp.text = insurance_detail['booking_ref']
         
    for temp in root.iter('categorycode'):
         temp.text = insurance_detail['category_code']
    for temp in root.iter('plancode'):
         temp.text = plan_detail['plan_code']
    for temp in root.iter('basecharges'):
         temp.text = str(plan_detail['premium'])
    # for temp in root.iter('ridercode'):
    #      temp.text = plan_detail['rider_code']
    for temp in root.iter('totalbasecharges'):
         temp.text = str(base_charges - (0.18 * base_charges))
    for temp in root.iter('servicetax'):
         temp.text = str(0.18 * base_charges)
    for temp in root.iter('totalcharges'):
         temp.text = str(plan_detail['premium'])
    for temp in root.iter('departuredate'):
         dep_date = datetime.strptime(insurance_detail['dept_date'], '%Y-%m-%d')
         formatted_dep_date = datetime.strftime(dep_date, "%d-%m-%Y")
         print(f'departure_dt: {formatted_dep_date}')
         temp.text = formatted_dep_date
    for temp in root.iter('days'):
         temp.text = insurance_detail['total_days']
         
    for temp in root.iter('arrivaldate'):
         arr_date = datetime.strptime(insurance_detail['arr_date'], '%Y-%m-%d')
         formatted_date = datetime.strftime(arr_date, "%d-%m-%Y")
         print(f'arrival_date: {formatted_date}')
         temp.text = formatted_date
    for temp in root.iter('passport'):
         temp.text = insurance_detail['passport']
    for temp in root.iter('address1'):
         temp.text = insurance_detail['address']
    for temp in root.iter('pincode'):
         temp.text = insurance_detail['pin']
    for temp in root.iter('country'):
         temp.text = insurance_detail['country']
    for temp in root.iter('mobileno'):
         temp.text = insurance_detail['phone']
    for temp in root.iter('emailaddress'):
         temp.text = insurance_detail['email']
    for temp in root.iter('name'):
         temp.text = insurance_detail['first_name'] + " " + insurance_detail['last_name']
    for temp in root.iter('dateofbirth'):
         temp.text = insurance_detail['dob']
    for temp in root.iter('age'):
         temp.text = str(insurance_detail['age'])
    
    
    tree.write('insurance/insurance_policy.xml')
    

url_inc = "https://asegotravel.in/trawelltag/v2/CreatePolicy.aspx"
Ref = '5e74074a-91d4-45ee-bfdc-1299585584f3'

def insurance(data):
    res = 'data='+data+'&ref='+Ref
    response = requests.post(url_inc,data={'data':data,'ref':Ref})
    return response


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

def get_insurance_plan_code_name(total_days, birth_date,category_code):
     selected_plan_list=[]
     plan_code = plan_name = ''
     with open("static/insurance/Plan.csv", 'r', encoding='utf-8-sig') as f:
          dict_reader = DictReader(f)
          plan_list = list(dict_reader)
          
          for plan in plan_list:
               if plan['category_code'] == category_code:
                    plan_code= plan['plan_code']
                    plan_name=plan['name']
                    dict={'plan_code': plan_code, 'plan_name': plan_name}
                    selected_plan_list.append(dict)
                    # print(f'selected: {selected_plan_list}')
     
     plan_details_list = get_insurance_plan_details(total_days, birth_date, selected_plan_list)
     return plan_details_list

def get_insurance_plan_name(total_days, birth_date, plan_code):
     selected_plan_list=[]
     plan_name = ''
     with open("static/insurance/Plan.csv", 'r', encoding='utf-8-sig') as f:
          dict_reader = DictReader(f)
          plan_list = list(dict_reader)
          
          for plan in plan_list:
               if plan['plan_code'] == plan_code:
                    plan_name=plan['name']
                    dict={'plan_code': plan_code, 'plan_name': plan_name}
                    selected_plan_list.append(dict)
                    # print(f'selected: {selected_plan_list}')
     
     plan_details_list = get_insurance_plan_details(total_days, birth_date, selected_plan_list)
     return plan_details_list

def get_insurance_plan_details(total_days, birth_date, selected_plan_list):
     
     age = calculateAge(birth_date)
     # plan_code = plan_name = ''
     day_limit =  age_limit = 0

     # selected_plan_list=[]
     premium_plan_list = []
     updated_plan_list=[]
     updated_rider_list =[]
     plan_details_list=[]

     
     # with open("static/insurance/Plan.csv", 'r', encoding='utf-8-sig') as f:
     #      dict_reader = DictReader(f)
     #      plan_list = list(dict_reader)
          
     #      for plan in plan_list:
     #           if plan['category_code'] == category_code:
     #                plan_code= plan['plan_code']
     #                plan_name=plan['name']
     #                dict={'plan_code': plan_code, 'plan_name': plan_name}
     #                selected_plan_list.append(dict)
     #                # print(f'selected: {selected_plan_list}')
               
               
     with open("static/insurance/PremiumChart.csv", 'r', encoding='utf-8-sig') as f:
          dict_reader = DictReader(f)
          premium_chart_list = list(dict_reader)
     
     
     data = pandas.read_csv('static/insurance/PremiumChart.csv')
     
     age_list = data.age_limit.tolist()
     
     age_array_list=np.array(age_list)
     unique_age_list= np.unique(age_array_list)
     
     age_limit = findClosestNumber(unique_age_list, age)
     
     day_list = data.day_limit.tolist()
     
     day_array_list=np.array(day_list)
     unique_day_list= np.unique(day_array_list)
     day_limit = findClosestNumber(unique_day_list, int(total_days))
     

     premium_plan_list = []
     
     for premium in premium_chart_list:
          if int(premium['day_limit']) == day_limit and int(premium['age_limit']) == age_limit:
               premium_plan_list.append(premium)
          
     for plan in selected_plan_list:
          for premium_list in premium_plan_list:
               if premium_list['plan_code'] == plan['plan_code']:
                    plan.update({'premium': premium_list['premium']})
                    updated_plan_list.append(plan)  
                    break
     
     

     with open("static/insurance/PlanRiders.csv", 'r', encoding='utf-8-sig') as f:
          dict_reader = DictReader(f)
          rider_code_list = list(dict_reader)
     
     for plan in updated_plan_list:
          for rider in rider_code_list:
               if rider['plan_code'] == plan['plan_code']:
                    plan.update({'rider_code': rider['rider_code']})
                    updated_rider_list.append(plan)
                    break
                         
     with open("static/insurance/RiderMaster.csv", 'r', encoding='utf-8-sig') as f:
          dict_reader = DictReader(f)
          rider_name_list = list(dict_reader)
          
          for plan in updated_rider_list:
               for rider in rider_name_list:
                    if rider['rider_code'] == plan['rider_code']:
                         plan.update({'plan_description': rider['name']})
                         plan_details_list.append(plan)
                         
     return plan_details_list

