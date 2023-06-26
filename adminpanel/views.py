from operator import methodcaller
from urllib import response
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.views import View
from onlinesavaari.models import Agent,Customer,CorporateCust
from flight.models import *
from .models import *
from Hotel.models import *
from wallet.models import *
import json
from django.db.models import Q
import string, random
from random import randint
from django.http import JsonResponse
import requests
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import os
from datetime import datetime
import calendar
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from onlinesavaari.decorators import check_user_able_to_see_onlinesavaari_app_page
from django.contrib.admin.views.decorators import staff_member_required
from .decorators import check_user_able_to_see_adminpanel_app_page , check_user_able_to_see_auth_app_page
from flight.decorators import check_user_able_to_see_flight_app_page
from django.utils.decorators import method_decorator
from django_celery_beat.models import ClockedSchedule,PeriodicTask
from .utils import createExcelSheet
from insurance.models import *
from insurance.utils import *
from django.db.models import Max, Subquery


# ......................
apikey= "2120183a3d1670-91ac-4f08-8026-db803a04fbdc"
api_url='https://apitest.tripjack.com/'
headers={"apikey":apikey, "Content-Type":"application/json"}

def flight_data(baseurl, apikey, endpoint, search_request): 
    url= api_url + endpoint
    response = requests.post(url, data=json.dumps(search_request), headers=headers)
    return response


def find_ticket(request):
    context ={}
    if(request.method == "POST"):
        id_type = request.POST.get('id_type')
        booking_id = request.POST.get('booking_id')
        if (id_type == 'OS_ID'):
            tj_id = Passenger.objects.values_list('bookingId', flat=True).filter(os_bookingId=booking_id)[0]
            # return JsonResponse({'tj_id': tj_id})
        else:
            tj_id=booking_id

        search_request = {"bookingId" : tj_id}
        result = flight_data(api_url, apikey, '/oms/v1/booking-details',search_request)
        json_data = result.json()
        json_pretty = json.dumps(json_data, sort_keys=True, indent=4)

        return HttpResponse(json_pretty,content_type="application/json")
    
    
    return render(request, "savaari-admin/find_ticket.html", context)



# def find_ticket(request):
#     context ={}
#     if(request.method == "POST"):
#         os_id = request.POST.get('os_id')
#         tj_id = request.POST.get('tj_id')
#         if (os_id != None):
#             print("hello")
#             data =  list((Passenger.objects.filter(os_bookingId=os_id)).values())
#             print(data[0]['bookingId'])
#             tj_id = data[0]['bookingId']
#         search_request = {
#         "bookingId" : tj_id
#         }

#         result = flight_data(api_url, apikey, '/oms/v1/booking-details',search_request)
        
#         return HttpResponse(result)
    
#     return render(request, "savaari-admin/find_ticket.html", context)




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

def find_group(user):
    if user.groups.filter(name='Agent').exists():
        return 'Agent'
    elif user.groups.filter(name='Corporate').exists():
        return 'Corporate'
    else:
        return 'Customer'


@login_required(login_url="admin_login")
# @permission_required('is_staff',login_url="admin_login", raise_exception=True)
@staff_member_required
def base(request):
    income = []
    list_income = 0
    user_no = User.objects.all().count()
    agent_no = Agent.objects.all().count()
    customer_no = Customer.objects.all().count()
    corporate_no = CorporateCust.objects.all().count()
    passanger = Passenger.objects.all().order_by('-id')[:10]
    booking_no = Passenger.objects.all().count()
    income_list =  list(Passenger.objects.all().values())
    for x in income_list:
        list_income = x['paid_amount']+list_income
    income.append(list_income)
    round(income[0], 2)
    agents = Agent.objects.all().order_by('-id')[:10]
    apibalance = list(APIbalance.objects.all().order_by('-id').values())
    total=0
    for x in apibalance:
        total = float(x['balance'])+float(total)
    get_agent = list(Agent.objects.all().values())
    for x in get_agent:
        monthly_income = 0
        agent = get_object_or_404(Agent,id=x['id'])
        passengers = list(Passenger.objects.filter(user=agent.user).values())
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        year, month = currentYear, currentMonth
        last = calendar.monthrange(year, month)[1]
        first_date = date.today().replace(day=1)
        last_date = date.today().replace(day=last)
        prev = ""
        for y in passengers:
            cur = y['bookingId']
            if cur != prev:
                today_date= (y['created_at']).date()
                if(first_date<=today_date<=last_date):
                    monthly_income += y['paid_amount']
            prev = y['bookingId']

        x['monthly_inc'] = monthly_income
            #     monthly_inc.append(monthly_income)

    now = datetime.now()
    datas = calendar.monthrange(now.year, now.month)[1]
    revenue_list = []
    amount = 0
    for i in range(1,datas+1):
        if Passenger.objects.filter(created_at__startswith=date(now.year,now.month,i)).exists():
            objs = Passenger.objects.filter(created_at__startswith=date(now.year,now.month,i))
            for obj in objs:
                paid = obj.paid_amount
                amount += int(paid)
            revenue_list.append(amount)
            amount = 0
        else:
            revenue_list.append(0)
    d = []
    e =[]
    p = Passenger.objects.all()
    
    for i in p:
        d.append(i.paid_amount)
        e.append(i.created_at.strftime("%Y-%m-%d %H:%M:%S"))

        
    return render(request, "savaari-admin/base.html", context={"passangers":passanger,"income":income,
                                                               'labels': ['Agent','Customer', 'corporate' ],
                                                                'data': [ agent_no,customer_no,corporate_no],
                                                                'colors': [ "#8b2fc9", "#e9c46a", "#ff0a54"],
                                                                'booking_no':booking_no,'total':total,
                                                                'all_agent':agents,'apibalance':apibalance,
                                                                'revenue_limit':revenue_list,
                                                                'passanger':d,'e':e
                                                               })

@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_onlinesavaari_app_page('view_agent','add_agent')
def agent_list(request):
    agent = Agent.objects.all().order_by('-id')

    return render(request, "savaari-admin/agent_list.html", context={'agent_list':agent})


@login_required(login_url="admin_login")
@staff_member_required
def delete_user(request, id):
    mark =  User.objects.get(id=id)

    # delete the todo
    mark.delete()
    return render(request, "savaari-admin/base.html", context={})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_onlinesavaari_app_page('view_directcancelair')
def direct_cancel(request):
    direct_cancel = list(DirectCancelAir.objects.all().values())
    for i in direct_cancel:
        i["route_deatil"] = json.loads(i["route_deatil"].replace("\'", "\""))
        i['passenger_detail'] = json.loads(i['passenger_detail'].replace("\'", "\""))
        i['user'] = User.objects.filter(id=i['user_id']).values().latest('id')['email']
    return render(request, "savaari-admin/direct_cancel_refund.html", context={'refund': direct_cancel})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_onlinesavaari_app_page('change_agent')
def update_agent(request, id):
  if request.method == 'POST':
    agent_status = request.POST.get('agent_status')
    mark = Agent.objects.get(id=id)
    Agent_email = mark.user.email
    Agent_firstname = mark.first_name
    mark.user.is_active = agent_status
    mark.user.save()
    if (agent_status == "True"):
        smtpHost = "smtp.gmail.com"
        smtpPort = 587
        mailUname = 'no-reply@onlinesavaari.com'
        mailPwd = 'afbzoctjmpppkwvk'
        fromEmail = 'no-reply@onlinesavaari.com'

        # mail body, recepients, attachment files
        mailSubject = "Congratulations! Your Account has been verified by Online Savaari"
        mailContentHtml = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"> <head> <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <meta name="x-apple-disable-message-reformatting"> <title></title> <style type="text/css"> @media only screen and (min-width: 660px) { .u-row { width: 640px !important; } .u-row .u-col { vertical-align: top; } .u-row .u-col-100 { width: 640px !important; } } @media (max-width: 660px) { .u-row-container { max-width: 100% !important; padding-left: 0px !important; padding-right: 0px !important; } .u-row .u-col { min-width: 320px !important; max-width: 100% !important; display: block !important; } .u-row { width: calc(100% - 40px) !important; } .u-col { width: 100% !important; } .u-col > div { margin: 0 auto; } } body { margin: 0; padding: 0; } table, tr, td { vertical-align: top; border-collapse: collapse; } p { margin: 0; } .ie-container table, .mso-container table { table-layout: fixed; } * { line-height: inherit; } a[x-apple-data-detectors='true'] { color: inherit !important; text-decoration: none !important; } table, td { color: #000000; } #u_body a { color: #0000ee; text-decoration: underline; } </style> </head> <body class="clean-body u_body" style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #e7e7e7;color: #000000"> <table id="u_body" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #e7e7e7;width:100%" cellpadding="0" cellspacing="0"> <tbody> <tr style="vertical-align: top"> <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top"> <div class="u-row-container" style="padding: 0px;background-color: transparent"> <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 640px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #f7dbbe;"> <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;"> <div class="u-col u-col-100" style="max-width: 320px;min-width: 640px;display: table-cell;vertical-align: top;"> <div style="background-color: #ffffff;height: 100%;width: 100% !important;"> <div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"> <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:30px 10px 20px;font-family:arial,helvetica,sans-serif;" align="left"> <table width="100%" cellpadding="0" cellspacing="0" border="0"> <tr> <td style="padding-right: 0px;padding-left: 0px;" align="center"> <img align="center" border="0" src="https://onlinesavaari.com/static/main/images/logo.png" alt="Image" title="Image" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 100%;max-width: 135px;" width="135"/> </td> </tr> </table> </td> </tr> </tbody> </table> </div> </div> </div> </div> </div> <div class="u-row-container" style="padding: 0px;background-color: transparent"> <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 640px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #f7dbbe;"> <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;"> <div class="u-col u-col-100" style="max-width: 320px;min-width: 640px;display: table-cell;vertical-align: top;"> <div style="background-color: #ffffff;height: 100%;width: 100% !important;"> <div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"> <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left"> <div style="line-height: 150%; text-align: left; word-wrap: break-word;"> <p style="font-size: 14px; line-height: 150%; text-align: center;"><span style="color: #444444; font-size: 14px; line-height: 21px;"><strong><span style="font-size: 38px; line-height: 57px;">Congratulations</span></strong></span></p> <p style="font-size: 14px; line-height: 150%; text-align: center;"><strong><span style="font-size: 38px; line-height: 57px;"><span style="color: #ec8c30; font-size: 38px; line-height: 57px;">"""+Agent_firstname+"""</span></span></strong></p> </div> </td> </tr> </tbody> </table> <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:10px 10px 15px;font-family:arial,helvetica,sans-serif;" align="left"> <div style="line-height: 150%; text-align: left; word-wrap: break-word;"> <p style="font-size: 14px; line-height: 150%;">Your account has been successfully verified. You can start booking now. Thank you for joining Online Savaari team.</p> </div> </td> </tr> </tbody> </table> <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:10px 10px 30px;font-family:arial,helvetica,sans-serif;" align="left"> <div align="center"> <a href="https://onlinesavaari.com" target="_blank" class="v-button" style="box-sizing: border-box;display: inline-block;font-family:arial,helvetica,sans-serif;text-decoration: none;-webkit-text-size-adjust: none;text-align: center;color: #FFFFFF; background-color: #e03e2d; border-radius: 4px;-webkit-border-radius: 4px; -moz-border-radius: 4px; width:auto; max-width:100%; overflow-wrap: break-word; word-break: break-word; word-wrap:break-word; mso-border-alt: none;"> <span style="display:block;padding:10px 20px;line-height:120%;"><strong><span style="font-size: 16px; line-height: 19.2px;">START BOOKING</span></strong></span> </a> </div> </td> </tr> </tbody> </table> </div> </div> </div> </div> </div> <div class="u-row-container" style="padding: 0px;background-color: transparent"> <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 640px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #ffffff;"> <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;"> <div class="u-col u-col-100" style="max-width: 320px;min-width: 640px;display: table-cell;vertical-align: top;"> <div style="height: 100%;width: 100% !important;"> <div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"> <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px 30px;font-family:arial,helvetica,sans-serif;" align="left"> <div align="center"> <div style="display: table; max-width:83px;"> <table align="left" border="0" cellspacing="0" cellpadding="0" width="32" height="32" style="width: 32px !important;height: 32px !important;display: inline-block;border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;margin-right: 10px"> <tbody><tr style="vertical-align: top"><td align="left" valign="middle" style="word-break: break-word;border-collapse: collapse !important;vertical-align: top"> <a href="https://facebook.com/OnlineSavaari" title="Facebook" target="_blank"> <img src="https://cdn.tools.unlayer.com/social/icons/circle/facebook.png" alt="Facebook" title="Facebook" width="32" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: block !important;border: none;height: auto;float: none;max-width: 32px !important"> </a> </td></tr> </tbody></table> <table align="left" border="0" cellspacing="0" cellpadding="0" width="32" height="32" style="width: 32px !important;height: 32px !important;display: inline-block;border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;margin-right: 0px"> <tbody><tr style="vertical-align: top"><td align="left" valign="middle" style="word-break: break-word;border-collapse: collapse !important;vertical-align: top"> <a href="https://twitter.com/OnlineSavaari" title="Twitter" target="_blank"> <img src="https://cdn.tools.unlayer.com/social/icons/circle/twitter.png" alt="Twitter" title="Twitter" width="32" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: block !important;border: none;height: auto;float: none;max-width: 32px !important"> </a> </td></tr> </tbody></table> </div> </div> </td> </tr> </tbody> </table> </div> </div> </div> </div> </div> <div class="u-row-container" style="padding: 0px;background-color: transparent"> <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 640px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;"> <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;"> <div class="u-col u-col-100" style="max-width: 320px;min-width: 640px;display: table-cell;vertical-align: top;"> <div style="height: 100%;width: 100% !important;"> <div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"> <table class="addressContent" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:6px 10px 8px;font-family:arial,helvetica,sans-serif;" align="left"> <div style="line-height: 160%; text-align: left; word-wrap: break-word;"> <p style="text-align: center; font-size: 14px; line-height: 160%;"><span style="font-size: 12px; line-height: 19.200000000000003px;"><strong><span style="line-height: 19.200000000000003px; font-size: 12px;">Our mailing address is:</span></strong></span></p> <p style="text-align: center; font-size: 14px; line-height: 160%;"><span style="font-size: 12px; line-height: 19.200000000000003px;">support@onlinesavaari.com</span></p> </div> </td> </tr> </tbody> </table> </div> </div> </div> </div> </div> </td> </tr> </tbody> </table> </body> </html>"""

        recepientsMailList = [Agent_email]
        attachmentFpaths = ["flight/logo.png"]
        sendEmail(smtpHost, smtpPort, mailUname, mailPwd, fromEmail,
                mailSubject, mailContentHtml, recepientsMailList, attachmentFpaths)

    print("execution complete...")
    return redirect('agent_list')

  return render(request, "savaari-admin/base.html", context={})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_onlinesavaari_app_page('change_corporatecust')
def update_corp(request, id):
  agent_status = request.POST.get('agent_status')
  Corp_email = request.POST.get('Corp_email')
  Corp_firstname = (request.POST.get('Corp_firstname')).upper()
  mark = CorporateCust.objects.get(id=id)
  mark.user.is_active = agent_status
  mark.user.save()
  if (agent_status == "True"):
    smtpHost = "smtp.gmail.com"
    smtpPort = 587
    mailUname = 'no-reply@onlinesavaari.com'
    mailPwd = 'afbzoctjmpppkwvk'
    fromEmail = 'no-reply@onlinesavaari.com'

    # mail body, recepients, attachment files
    mailSubject = "Congratulations! Your Account has been verified by Online Savaari"
    mailContentHtml = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"> <head> <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <meta name="x-apple-disable-message-reformatting"> <title></title> <style type="text/css"> @media only screen and (min-width: 660px) { .u-row { width: 640px !important; } .u-row .u-col { vertical-align: top; } .u-row .u-col-100 { width: 640px !important; } } @media (max-width: 660px) { .u-row-container { max-width: 100% !important; padding-left: 0px !important; padding-right: 0px !important; } .u-row .u-col { min-width: 320px !important; max-width: 100% !important; display: block !important; } .u-row { width: calc(100% - 40px) !important; } .u-col { width: 100% !important; } .u-col > div { margin: 0 auto; } } body { margin: 0; padding: 0; } table, tr, td { vertical-align: top; border-collapse: collapse; } p { margin: 0; } .ie-container table, .mso-container table { table-layout: fixed; } * { line-height: inherit; } a[x-apple-data-detectors='true'] { color: inherit !important; text-decoration: none !important; } table, td { color: #000000; } #u_body a { color: #0000ee; text-decoration: underline; } </style> </head> <body class="clean-body u_body" style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #e7e7e7;color: #000000"> <table id="u_body" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #e7e7e7;width:100%" cellpadding="0" cellspacing="0"> <tbody> <tr style="vertical-align: top"> <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top"> <div class="u-row-container" style="padding: 0px;background-color: transparent"> <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 640px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #f7dbbe;"> <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;"> <div class="u-col u-col-100" style="max-width: 320px;min-width: 640px;display: table-cell;vertical-align: top;"> <div style="background-color: #ffffff;height: 100%;width: 100% !important;"> <div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"> <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:30px 10px 20px;font-family:arial,helvetica,sans-serif;" align="left"> <table width="100%" cellpadding="0" cellspacing="0" border="0"> <tr> <td style="padding-right: 0px;padding-left: 0px;" align="center"> <img align="center" border="0" src="https://onlinesavaari.com/static/main/images/logo.png" alt="Image" title="Image" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 100%;max-width: 135px;" width="135"/> </td> </tr> </table> </td> </tr> </tbody> </table> </div> </div> </div> </div> </div> <div class="u-row-container" style="padding: 0px;background-color: transparent"> <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 640px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #f7dbbe;"> <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;"> <div class="u-col u-col-100" style="max-width: 320px;min-width: 640px;display: table-cell;vertical-align: top;"> <div style="background-color: #ffffff;height: 100%;width: 100% !important;"> <div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"> <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left"> <div style="line-height: 150%; text-align: left; word-wrap: break-word;"> <p style="font-size: 14px; line-height: 150%; text-align: center;"><span style="color: #444444; font-size: 14px; line-height: 21px;"><strong><span style="font-size: 38px; line-height: 57px;">Congratulations</span></strong></span></p> <p style="font-size: 14px; line-height: 150%; text-align: center;"><strong><span style="font-size: 38px; line-height: 57px;"><span style="color: #ec8c30; font-size: 38px; line-height: 57px;">"""+Corp_firstname+"""</span></span></strong></p> </div> </td> </tr> </tbody> </table> <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:10px 10px 15px;font-family:arial,helvetica,sans-serif;" align="left"> <div style="line-height: 150%; text-align: left; word-wrap: break-word;"> <p style="font-size: 14px; line-height: 150%;">Your account has been successfully verified. You can start booking now. Thank you for joining Online Savaari team.</p> </div> </td> </tr> </tbody> </table> <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:10px 10px 30px;font-family:arial,helvetica,sans-serif;" align="left"> <div align="center"> <a href="https://onlinesavaari.com" target="_blank" class="v-button" style="box-sizing: border-box;display: inline-block;font-family:arial,helvetica,sans-serif;text-decoration: none;-webkit-text-size-adjust: none;text-align: center;color: #FFFFFF; background-color: #e03e2d; border-radius: 4px;-webkit-border-radius: 4px; -moz-border-radius: 4px; width:auto; max-width:100%; overflow-wrap: break-word; word-break: break-word; word-wrap:break-word; mso-border-alt: none;"> <span style="display:block;padding:10px 20px;line-height:120%;"><strong><span style="font-size: 16px; line-height: 19.2px;">START BOOKING</span></strong></span> </a> </div> </td> </tr> </tbody> </table> </div> </div> </div> </div> </div> <div class="u-row-container" style="padding: 0px;background-color: transparent"> <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 640px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #ffffff;"> <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;"> <div class="u-col u-col-100" style="max-width: 320px;min-width: 640px;display: table-cell;vertical-align: top;"> <div style="height: 100%;width: 100% !important;"> <div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"> <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px 30px;font-family:arial,helvetica,sans-serif;" align="left"> <div align="center"> <div style="display: table; max-width:83px;"> <table align="left" border="0" cellspacing="0" cellpadding="0" width="32" height="32" style="width: 32px !important;height: 32px !important;display: inline-block;border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;margin-right: 10px"> <tbody><tr style="vertical-align: top"><td align="left" valign="middle" style="word-break: break-word;border-collapse: collapse !important;vertical-align: top"> <a href="https://facebook.com/OnlineSavaari" title="Facebook" target="_blank"> <img src="https://cdn.tools.unlayer.com/social/icons/circle/facebook.png" alt="Facebook" title="Facebook" width="32" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: block !important;border: none;height: auto;float: none;max-width: 32px !important"> </a> </td></tr> </tbody></table> <table align="left" border="0" cellspacing="0" cellpadding="0" width="32" height="32" style="width: 32px !important;height: 32px !important;display: inline-block;border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;margin-right: 0px"> <tbody><tr style="vertical-align: top"><td align="left" valign="middle" style="word-break: break-word;border-collapse: collapse !important;vertical-align: top"> <a href="https://twitter.com/OnlineSavaari" title="Twitter" target="_blank"> <img src="https://cdn.tools.unlayer.com/social/icons/circle/twitter.png" alt="Twitter" title="Twitter" width="32" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: block !important;border: none;height: auto;float: none;max-width: 32px !important"> </a> </td></tr> </tbody></table> </div> </div> </td> </tr> </tbody> </table> </div> </div> </div> </div> </div> <div class="u-row-container" style="padding: 0px;background-color: transparent"> <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 640px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;"> <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;"> <div class="u-col u-col-100" style="max-width: 320px;min-width: 640px;display: table-cell;vertical-align: top;"> <div style="height: 100%;width: 100% !important;"> <div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"> <table class="addressContent" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:6px 10px 8px;font-family:arial,helvetica,sans-serif;" align="left"> <div style="line-height: 160%; text-align: left; word-wrap: break-word;"> <p style="text-align: center; font-size: 14px; line-height: 160%;"><span style="font-size: 12px; line-height: 19.200000000000003px;"><strong><span style="line-height: 19.200000000000003px; font-size: 12px;">Our mailing address is:</span></strong></span></p> <p style="text-align: center; font-size: 14px; line-height: 160%;"><span style="font-size: 12px; line-height: 19.200000000000003px;">support@onlinesavaari.com</span></p> </div> </td> </tr> </tbody> </table> </div> </div> </div> </div> </div> </td> </tr> </tbody> </table> </body> </html>"""

    recepientsMailList = [Corp_email]
    attachmentFpaths = ["flight/logo.png"]
    sendEmail(smtpHost, smtpPort, mailUname, mailPwd, fromEmail,
              mailSubject, mailContentHtml, recepientsMailList, attachmentFpaths)

    print("execution complete...")

  return render(request, "savaari-admin/base.html", context={})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_markup','add_markup')
def markup(request):
    login_user = request.user
    with open("static/flight/airlines.json", "r") as f:
        air_list = json.loads(f.read())
        
    user_type = request.POST.get('user_type')
    markup_type = request.POST.get('markup_type')
    amount_type = request.POST.get('amount_type')
    amount = request.POST.get('amount')
    airline = request.POST.get('airline')
    markup = Markup.objects.all().order_by('-id')

    if amount_type != None :
        cust1=Markup.objects.create(user=login_user,markup_type=markup_type,user_type=user_type,amount_type=amount_type,amount=amount,airline_type=airline)
    return render(request, "savaari-admin/markup.html", context={'markup':markup,'air_list':air_list})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_markup', 'delete_markup')
def delete_markup(request, id):
    mark =  Markup.objects.get(id=id)

    # delete the todo
    mark.delete()
    return render(request, "savaari-admin/base.html", context={})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_seriesmarkup','add_seriesmarkup')
def serialmarkup(request):
    login_user = request.user
    with open("static/flight/airport_list.json", "r") as f:
        result = json.loads(f.read())
        airport_code = [d for d in result if d['country'] == 'India']
    amount_type = request.POST.get('amount_type')
    amount = request.POST.get('amount')
    airport = request.POST.get('airport')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    seriesmarkup = SeriesMarkup.objects.all().order_by('-id')
    print(seriesmarkup.values())

    if amount_type != None :
        cust1=SeriesMarkup.objects.create(user=login_user,amount_type=amount_type,amount=amount,airport_name=airport,start_date=start_date,end_date=end_date)
    
    return render(request, "savaari-admin/serialmarkup.html", context={'seriesmarkup':seriesmarkup,'airport_code':airport_code})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_seriesmarkup', 'delete_seriesmarkup')
def delete_serialmarkup(request, id):
    mark =  SeriesMarkup.objects.get(id=id)

    # delete the todo
    mark.delete()
    return render(request, "savaari-admin/base.html", context={})

@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_markup', 'change_markup')
def updaterecord(request, id):
  amount = request.POST.get('amount')
  print(amount)
  mark = Markup.objects.get(id=id)
  mark.amount = amount
  mark.save()
  return render(request, "savaari-admin/base.html", context={})

@login_required(login_url="admin_login")
@staff_member_required
def updatedoc(request, id):
  doc = request.FILES.get('doc')
  print(doc)
  mark = Agent.objects.get(id=id)
  cust1=Documents.objects.create(username=mark,doc=doc)
  return render(request, "savaari-admin/base.html", context={})

@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_seriesmarkup', 'change_seriesmarkup')
def updateseriesrecord(request, id):
  amount = request.POST.get('amount')
  start_date = request.POST.get('start_date')
  end_date = request.POST.get('end_date')
  print(amount,end_date,start_date)
  mark = SeriesMarkup.objects.get(id=id)
  mark.amount = amount
  mark.start_date = start_date
  mark.end_date = end_date
  mark.save()
  return render(request, "savaari-admin/base.html", context={})

@login_required(login_url="admin_login")
@staff_member_required
def distribution_list(request):
    return render(request, "savaari-admin/distribution_list.html", context={})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_refundflight')
def refund(request):
    Refund = RefundFlight.objects.all().order_by('-id')
    return render(request, "savaari-admin/refund.html", context={"Refund":Refund})

@login_required(login_url="admin_login")
@staff_member_required
def tds_detail(request):
    tds_data = list(WalletDetails.objects.filter(~Q(tds=0)).order_by('-id').values())
    print(tds_data)
    return render(request=request, template_name="savaari-admin/tds_table.html", context={'tds_data':tds_data})

@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_rescheduleflight')
def reschedule(request):
    reschedule = RescheduleFlight.objects.all().order_by('-id')
    return render(request, "savaari-admin/reschedule.html", context={"reschedule":reschedule})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_onlinesavaari_app_page('view_customer')
def customer_list(request):
    customer = Customer.objects.all().order_by('-id')
    return render(request, "savaari-admin/customer_list.html", context={'customers':customer})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_onlinesavaari_app_page('view_corporatecust','add_corporatecust')
def corporation_list(request):
    corporate = CorporateCust.objects.all().order_by('-id')
    return render(request, "savaari-admin/corporation_list.html", context={'corporates':corporate})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_onlinesavaari_app_page('change_agent')
def view_agent_profile(request,id):
    try:
        agent = get_object_or_404(Agent,id=id)
    except:
        pass
    # passengers = Passenger.objects.filter(user=agent.user)
    grouping_query = Passenger.objects.filter(user=agent.user).values('os_bookingId').annotate(Max('id'))
    print("query: ", grouping_query)
    passengers = Passenger.objects.filter(id__in=Subquery(grouping_query.values('id__max'))).values_list('id', 'bookingId','paid_amount','pnr','flight_status',named=True)
    print("passenger: ", passengers)
    if not WalletDetails.objects.filter(username=agent.user):
            wallet_activated_on = date.today()
            curl = WalletDetails.objects.create(username=agent.user,email=agent.user,wallet_activated_on=wallet_activated_on,wallet_balance=0)
    wallet_data = (WalletDetails.objects.filter(username=agent.user).values()).latest('id')
    try:
        doc_detail = Documents.objects.filter(username=agent).doc
    except:
        doc_detail = None
    spent = 0
    total_spent = list(Passenger.objects.filter(user=agent.user).values())
    for x in total_spent:

        spent = spent + x['paid_amount']
    documents = request.FILES.get('doc')
    if (request.method == 'POST') and (documents != None) :
        documents = request.FILES.get('doc')
        doc = Documents.objects.create(username = agent.user, doc=documents)

    transactions = WalletDetails.objects.filter(username=agent.user)
    
    if AgentCredit.objects.filter(agent = agent).exists():
        credit_amount = AgentCredit.objects.filter(agent=agent).last().credit_balance
    else:
        credit_amount = 0
    
    

    context = {
        'agents': agent,
        'credit_amount': credit_amount,
        'passanger': passengers,
        'wallet': wallet_data,
        'doc_detail': doc_detail,
        'spent': spent,
        'transactions': transactions
    }
    return render(request, "savaari-admin/user_profile.html", context=context)


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_onlinesavaari_app_page('change_corporatecust')
def view_corp_profile(request,id):
    try:
        agent = get_object_or_404(CorporateCust,id=id)
    except:
        pass
    print(agent)
    passengers = Passenger.objects.filter(user=agent.user)
    print(passengers)
    if not WalletDetails.objects.filter(username=agent.user):
            wallet_activated_on = date.today()
            curl = WalletDetails.objects.create(username=agent.user,email=agent.user,wallet_activated_on=wallet_activated_on,wallet_balance=0)
    wallet_data = (WalletDetails.objects.filter(username=agent.user).values()).latest('id')
    try:
        doc_detail = Documents.objects.get(username=agent).doc
        print(doc_detail)
    except:
        doc_detail = None
    spent = 0
    total_spent = list(Passenger.objects.filter(user=agent.user).values())
    for x in total_spent:

        spent = spent + x['paid_amount']
    documents = request.FILES.get('doc')
    if (request.method == 'POST') and (documents != None) :
        documents = request.FILES.get('doc')
        doc = Documents.objects.create(username = agent.user, doc=documents)


    context = {
        'agents': agent,
        'passanger': passengers,
        'wallet': wallet_data,
        'doc_detail': doc_detail,
        'spent': spent,
    }
    return render(request, "savaari-admin/user_profile.html", context=context) 


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_onlinesavaari_app_page('change_customer')
def view_cust_profile(request,id):
    try:
        agent = get_object_or_404(Customer,id=id)
    except:
        pass
    print(agent)
    passengers = Passenger.objects.filter(user=agent.user)
    print(passengers)
    if not WalletDetails.objects.filter(username=agent.user):
            wallet_activated_on = date.today()
            curl = WalletDetails.objects.create(username=agent.user,email=agent.user,wallet_activated_on=wallet_activated_on,wallet_balance=0)
    wallet_data = (WalletDetails.objects.filter(username=agent.user).values()).latest('id')
    spent = 0
    total_spent = list(Passenger.objects.filter(user=agent.user).values())
    for x in total_spent:

        spent = spent + x['paid_amount']
    documents = request.FILES.get('doc')
    if (request.method == 'POST') and (documents != None) :
        documents = request.FILES.get('doc')
        doc = Documents.objects.create(username = agent.user, doc=documents)
    context = {
        'agents': agent,
        'passanger': passengers,
        'wallet': wallet_data,
        'spent': spent,

    }
    return render(request, "savaari-admin/user_profile.html", context=context)

def admin_login(request):
    error_mgs = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate( username=username, password=password)
        try:
            if user.is_superuser or user.is_staff:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect('base')
            error_mgs = 'You are are not a superuser !!'
        except:
            error_mgs = 'Email or Password invalid !!'
    return render(request, "savaari-admin/auth_login.html", context={'error_mgs': error_mgs})

def admin_logout(request):
    logout(request)
    messages.info(request, f"You are now logged out.")
    return render(request=request, template_name="savaari-admin/auth_login.html")

# def update_view(request, id):
#     context ={}
 
#     obj = get_object_or_404(Markup, id = id)
 
#     form = GeeksForm(request.POST or None, instance = obj)
 
#     # save the data from the form and
#     # redirect to detail_view
#     if form.is_valid():
#         form.save()
#         return HttpResponseRedirect("/"+id)
 
#     # add form dictionary to context
#     context["form"] = form 
 
#     return render(request, "savaari-admin/markup.html", context)



@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_promocode','add_promocode')
def promocode(request):
    login_user = request.user
    promocode = request.POST.get('promocode')
    amount = request.POST.get('amount')
    promo_description = request.POST.get('promo_description')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    Promo = list(Promocode.objects.all().order_by('-id').values())
    print(Promo)
    print(promocode,amount,promo_description,start_date,end_date)
    if promocode != None :
        cust1=Promocode.objects.create(user=login_user,promo_code=promocode,amount=amount,description=promo_description,start_date=start_date,end_date=end_date)
    return render(request=request, template_name="savaari-admin/code.html", context={'Promo':Promo})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_promocode', 'change_promocode')
def updatepromocode(request, id):
  description = request.POST.get('description')
  start_date = request.POST.get('start_date')
  end_date = request.POST.get('end_date')
  mark = Promocode.objects.get(id=id)
  mark.description = description
  mark.start_date = start_date
  mark.end_date = end_date
  mark.save()
  return render(request, "savaari-admin/base.html", context={})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_flight_app_page('view_passenger','add_passenger' )
def flightbooking(request):
    if request.method == "POST":
        bookingid = request.POST.get("bookingid")
        flight_detail = list(Passenger.objects.filter(bookingId=bookingid).values())
        # print(flight_detail)
        return render(request=request, template_name="savaari-admin/view_flight_admin.html", context={'flight_detail': flight_detail})
    passanger = Passenger.objects.all().order_by('-id')
    user_data = User.objects.all().order_by('-id')
    return render(request=request, template_name="savaari-admin/flight_booking.html", context={'data': passanger,'user_data':user_data})

@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_flight_app_page('view_passenger','add_passenger' )
def hold_booking(request):
    # if request.method == "POST":
    #     bookingid = request.POST.get("bookingid")
    #     flight_detail = list(Passenger.objects.filter(bookingId=bookingid).values())
    #     # print(flight_detail)
    #     return render(request=request, template_name="savaari-admin/view_hold_admin.html", context={'flight_detail': flight_detail})
    passanger = Hold.objects.all().order_by('-id')
    user_data = User.objects.all().order_by('-id')
    return render(request=request, template_name="savaari-admin/hold_booking.html", context={'data': passanger,'user_data':user_data})
@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_promocode', 'change_promocode')
def update_hold(request, id):
    if request.method == "POST":
        os_bookingId = request.POST.get('os_bookingId', None)
        bookingId = (Hold.objects.filter(os_bookingId=os_bookingId)[0]).bookingId
        
        search_request = {
                    "bookingId" : bookingId
                }           
        result = flight_data(api_url, apikey, '/oms/v1/booking-details',search_request)
        data=result.json()
        if data['order']['status']=="ON_HOLD":
            for a in data['itemInfos']['AIR']['travellerInfos']:
                if('pnrDetails' in a): 
                    res= a['pnrDetails']
                    pnr = list(res.values())[0]
            search_request ={
                        "bookingId":bookingId,
                        "pnrs":[pnr]
                    }           
            result = flight_data(api_url, apikey, '/oms/v1/air/unhold',search_request)
            unhold=result.json()
            if unhold['status']['success']:
                mark = Hold.objects.get(id=id)
                mark.booking_status = "Unhold"
                mark.unhold_by = str(request.user)
                mark.save()
        
    return render(request, "savaari-admin/base.html", context={})

@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_hotelbookinghistory', 'add_hotelbookinghistory')
def hotelbooking(request):
    if request.method == "POST":
        osh_bookingId = request.POST.get("osh_bookingId")
        print(osh_bookingId,"..........")
        flight_detail = list(HotelBookingHistory.objects.filter(
            osh_bookingId=osh_bookingId).values())
        print(flight_detail)
        return render(request=request, template_name="savaari-admin/view_hotel_admin.html", context={'flight_detail': flight_detail})
    passanger = HotelBookingHistory.objects.all().order_by('-id').values()
    return render(request=request, template_name="savaari-admin/hotel_booking.html", context={'data': passanger})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_hotelbookinghistory', 'change_hotelbookinghistory')
def updatehotelboking(request, id):
    print(id)
    pnr = request.POST.get('pnr')
    flight_status = request.POST.get('status')
    print(flight_status, pnr)
    if flight_status is not None:
        flight_detail = HotelBookingHistory.objects.get(id=id)
        flight_detail.booking_status = flight_status
        flight_detail.save()
    passanger = HotelBookingHistory.objects.all().order_by('-id').values()
    return render(request=request, template_name="savaari-admin/hotel_booking.html", context={'data': passanger})

@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_flight_app_page('view_passenger','change_passenger' )
def updateflightboking(request, id):
  pnr = request.POST.get('pnr')
  flight_status = request.POST.get('status')
  username = request.POST.get('username')
  wall_user = User.objects.get(email=username)
  print(wall_user)
  print(flight_status,pnr)
  flight_detail = Passenger.objects.get(id=id)
  flight_detail.pnr = pnr
  flight_detail.flight_status = flight_status
  flight_detail.user = wall_user
  flight_detail.save()
  return render(request, "savaari-admin/base.html", context={})



def agent_login(request):
    return render(request=request, template_name="savaari-admin/agent_login_admin.html", context={})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('add_banner', 'view_banner')
def banner(request):
    print(request.FILES)
    login_user = request.user
    big_banner = request.FILES.get('big_banner')
    small_banner1 = request.FILES.get('small_banner1')
    small_banner2 = request.FILES.get('small_banner2')
    if (big_banner != None) :
        cust1=Banner.objects.create(user=login_user,big_banner=big_banner)
    if (small_banner1 != None) :
        cust1=SmallBanner1.objects.create(user=login_user,small_banner1=small_banner1)
    if (small_banner2 != None) :
        cust1=SmallBanner2.objects.create(user=login_user,small_banner2=small_banner2)

    return render(request=request, template_name="savaari-admin/banner.html", context={})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('add_rescheduleflight', 'view_rescheduleflight')
def reschedule_pay_request(request):
    BookingId = request.POST.get('BookingId')
    pass_name = list(Passenger.objects.filter(os_bookingId=BookingId).values())
    pass_email = pass_name[0]['email']
    username = request.POST.get('username')
    amount = request.POST.get('amount')
    
    print(username,amount)

    smtpHost = "smtp.gmail.com"
    smtpPort = 587
    mailUname = 'no-reply@onlinesavaari.com'
    mailPwd = 'afbzoctjmpppkwvk'
    fromEmail = 'no-reply@onlinesavaari.com'

    # mail body, recepients, attachment files
    mailSubject = "Payment Request for Reschedule Flight"
    mailContentHtml = "Dear "+ username + ", Please Pay amount of rs. " + amount + " to Reschedule your flight. Thank You."

    recepientsMailList = [username,pass_email]
    attachmentFpaths = ["flight/logo.png"]
    sendEmail(smtpHost, smtpPort, mailUname, mailPwd, fromEmail,
              mailSubject, mailContentHtml, recepientsMailList, attachmentFpaths)

    print("execution complete...")
    return render(request, "savaari-admin/reschedule.html", context={"reschedule":reschedule})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('change_rescheduleflight', 'view_rescheduleflight')
def update_reschedule(request, id):
    BookingId = request.POST.get('BookingId')
    print(BookingId)
    pass_name = list(Passenger.objects.filter(os_bookingId=BookingId).values())
    print(pass_name)
    pass_email = pass_name[0]['email']
    username = request.POST.get('username')
    reschedule_status = request.POST.get('reschedule_status')
    flight_detail = Passenger.objects.get(os_bookingId=BookingId)
    flight_detail.flight_status = reschedule_status
    flight_detail.save()
    reschedule = RescheduleFlight.objects.get(id=id)
    reschedule.Reschedule_status = reschedule_status
    reschedule.save()


    smtpHost = "smtp.gmail.com"
    smtpPort = 587
    mailUname = 'no-reply@onlinesavaari.com'
    mailPwd = 'afbzoctjmpppkwvk'
    fromEmail = 'no-reply@onlinesavaari.com'

    # mail body, recepients, attachment files
    mailSubject = "Reschedule Request Status Changed"
    mailContentHtml = "Dear "+ username + ", Your Reschedule request status has been changed to "+ reschedule_status+ ". Thank You."

    recepientsMailList = [username,pass_email]
    attachmentFpaths = ["flight/logo.png"]
    sendEmail(smtpHost, smtpPort, mailUname, mailPwd, fromEmail,
              mailSubject, mailContentHtml, recepientsMailList, attachmentFpaths)

    print("execution complete...")

    return render(request, "savaari-admin/base.html", context={})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_deposit')
def deposit_request(request):  
    deposite = list(Deposit.objects.all().values())
    login_user = request.user
    email_or_phone = request.POST.get('email_or_phone')
    amount = request.POST.get('amount')
    bank_name = request.POST.get('bank_name')
    deposite_branch = request.POST.get('deposite_branch')
    transaction_number = request.POST.get('transaction_number')
    if(transaction_number == ""):
        transaction_number = randint(1000000000, 9999999999)
        osn_id = str(transaction_number)
        transaction_number = 'ADMN'+osn_id
    dep_status = request.POST.get('status')
    deposit_slip = request.FILES.get('deposit_slip')
    print(deposit_slip)

    if not WalletDetails.objects.filter(email=email_or_phone):
            wallet_activated_on = date.today()
            if(email_or_phone != None):
                wall_user = User.objects.get(email=email_or_phone)
                print(wall_user)
                curl = WalletDetails.objects.create(username=wall_user,email=email_or_phone,wallet_activated_on=wallet_activated_on,wallet_balance=0)
    if(email_or_phone != None):
        wallet_detail = (WalletDetails.objects.filter(email=email_or_phone).values()).latest('id')
        print(wallet_detail)
    if (request.method == "POST") and (dep_status != "Approve"):
        cust1=Deposit.objects.create(user=login_user,dep_status="Approve",deposit_slip=deposit_slip,email_or_phone=email_or_phone,amount=amount,bank_name=bank_name,deposite_branch=deposite_branch,trasaction_num=transaction_number)
        print(wallet_detail['username_id']) 
        wall_user = User.objects.get(id=wallet_detail['username_id'])
        print(wall_user)
        wallet_bal = wallet_detail['wallet_balance']
        new_bal = float(wallet_bal)+ float(amount)
        curl = WalletDetails.objects.create(username=wall_user,email=email_or_phone,wallet_balance=new_bal,amount=amount,trasc_type="Credit",transaction_mode="DEPOSIT",transaction_status="Success",transaction_id=transaction_number,note="added from admin panel for deposit request")
  
    
        smtpHost = "smtp.gmail.com"
        smtpPort = 587
        mailUname = 'no-reply@onlinesavaari.com'
        mailPwd = 'afbzoctjmpppkwvk'
        fromEmail = 'no-reply@onlinesavaari.com'

        # mail body, recepients, attachment files
        mailSubject = "Wallet Balance Updated"
        mailContentHtml = "Dear "+ email_or_phone + ", Your Amount of Rs. " + amount + " Has been Added to your Wallet. Thank You"

        recepientsMailList = [email_or_phone]
        attachmentFpaths = ["flight/logo.png"]
        sendEmail(smtpHost, smtpPort, mailUname, mailPwd, fromEmail,
                  mailSubject, mailContentHtml, recepientsMailList, attachmentFpaths)

        print("execution complete...")
    
    return render(request=request, template_name="savaari-admin/deposit.html", context={'deposite':deposite})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_deposit','change_deposit')
def update_deposit(request, id):
    dep_status = request.POST.get('dep_status')
    email_or_phone = request.POST.get('email_or_phone')
    amount = request.POST.get('amount')
    transaction_number = request.POST.get('transaction_number')
    print(dep_status,email_or_phone,amount,transaction_number)
    if not WalletDetails.objects.filter(email=email_or_phone):
            wallet_activated_on = date.today()
            if(email_or_phone != None):
                wall_user = User.objects.get(email=email_or_phone)
                print(wall_user)
                curl = WalletDetails.objects.create(username=wall_user,email=email_or_phone,wallet_activated_on=wallet_activated_on,wallet_balance=0)
    if(email_or_phone != None):
        wallet_detail = (WalletDetails.objects.filter(email=email_or_phone).values()).latest('id')
        print(wallet_detail)
    if (request.method == "POST") and (dep_status == "Approve"):
        print(wallet_detail['username_id']) 
        wall_user = User.objects.get(id=wallet_detail['username_id'])
        print(wall_user)
        wallet_bal = wallet_detail['wallet_balance']
        new_bal = float(wallet_bal)+ float(amount)
        curl = WalletDetails.objects.create(username=wall_user,email=email_or_phone,wallet_balance=new_bal,amount=amount,trasc_type="Credit",transaction_mode="DEPOSIT",transaction_status="Success",transaction_id=transaction_number,note="added from admin panel for deposit request")
  
    
        smtpHost = "smtp.gmail.com"
        smtpPort = 587
        mailUname = 'no-reply@onlinesavaari.com'
        mailPwd = 'afbzoctjmpppkwvk'
        fromEmail = 'no-reply@onlinesavaari.com'

        # mail body, recepients, attachment files
        mailSubject = "Wallet Balance Updated"
        mailContentHtml = "Dear "+ email_or_phone + ", Your Amount of Rs. " + amount + " Has been Added to your Wallet. Thank You"

        recepientsMailList = [email_or_phone]
        attachmentFpaths = ["flight/logo.png"]
        sendEmail(smtpHost, smtpPort, mailUname, mailPwd, fromEmail,
                  mailSubject, mailContentHtml, recepientsMailList, attachmentFpaths)

        print("execution complete...")
    
    mark = Deposit.objects.get(id=id)
    mark.dep_status = dep_status
    mark.save()

    return render(request, "savaari-admin/base.html", context={})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_userdata')
def staff(request):
    staff_id = request.POST.get('staff_id')
    group_name = request.POST.get('group')
    user = User.objects.all()
    user_group_names = [] 
    for users in user:
        groups = users.groups.all()
        group = [group.name for group in groups]
        user_group_names.append(group)
    print(user_group_names)
        
    if request.method == 'POST':
        g = Group.objects.get(name=group_name)
        users = User.objects.get(id = staff_id)
        g.user_set.add(users)
         
    group =Group.objects.all()
    staff = User.objects.filter(is_staff=True)
		
    return render(request=request, template_name="savaari-admin/staff.html", context={  'group':group,
                                                                                        'staff':user,
                                                                                        'user':zip(user,user_group_names)})

@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_walletdetails','change_walletdetails')
def update_credit(request, id):
    emailId = request.POST.get('emailId')
    creditamount = request.POST.get('creditamount')
    transaction_number = randint(1000000000, 9999999999)
    osn_id = str(transaction_number)
    transaction_number = 'DEBIT'+osn_id
    print(emailId,creditamount)
    if not WalletDetails.objects.filter(email=emailId):
        wallet_activated_on = date.today()
        if(emailId != None):
            wall_user = User.objects.get(email=emailId)
            print(wall_user)
            curl = WalletDetails.objects.create(username=wall_user,email=emailId,wallet_activated_on=wallet_activated_on,wallet_balance=0)
    if(emailId != None):
        wallet_detail = (WalletDetails.objects.filter(email=emailId).values()).latest('id')
        print(wallet_detail)
    if (request.method == "POST"):
        print(wallet_detail['username_id']) 
        wall_user = User.objects.get(id=wallet_detail['username_id'])
        print(wall_user)
        wallet_bal = wallet_detail['wallet_balance']
        new_bal = float(wallet_bal)- float(creditamount)
        curl = WalletDetails.objects.create(username=wall_user,email=emailId,wallet_balance=new_bal,amount=creditamount,trasc_type="Debit",transaction_mode="CREDITMODEL",transaction_status="Success",transaction_id=transaction_number,note="debited against  CREDIT given by admin")
    mark = AgentCredit.objects.get(id=id)
    mark.creditamount = creditamount
    mark.status = "Debited"
    mark.save()
    return render(request, "savaari-admin/base.html", context={})

@login_required(login_url="admin_login")
@staff_member_required
def notification(request):
    return render(request=request, template_name="savaari-admin/notifivation.html", context={})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_directcancelair')
def direct_cancel_air(request):
    return render(request=request, template_name="savaari-admin/index.html", context={})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_apibalance')
def apibalance(request):
    login_user = request.user
    balance = request.POST.get('balance')
    company_name = request.POST.get('company_name')
    #mobile = request.POST.get('mobile')
    mobile = "1800419906"
    email = "admin@onlinesavaari.com"
    add_company_name = request.POST.get('add_company_name')
    add_balance = request.POST.get('add_balance')
    print(add_company_name,add_balance)
    apibalance = list(APIbalance.objects.all().order_by('-id').values())


    # if add_balance != None:
    #     for x in apibalance:
    #         company_name = x['company_name']
    #         print(company_name)
    #         if(company_name == add_company_name):
    #             r_balance = x['balance']
    #             print(r_balance)
    #             total_balance = float(r_balance)+ float(add_balance)
    #             print(total_balance)



    if company_name != None :
        cust1=APIbalance.objects.create(user=login_user,balance=balance,company_name=company_name,mobile=mobile,email=email)
    return render(request=request, template_name="savaari-admin/apibalance.html", context={'apibalance':apibalance})


@method_decorator(login_required(login_url='admin_login'), name='dispatch')
@method_decorator(staff_member_required(), name='dispatch')
@method_decorator(check_user_able_to_see_adminpanel_app_page('add_userdata'), name='dispatch')
class RegisterAdmin(APIView):
    authentication_classes = []
    permission_classes = []
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "savaari-admin/base.html"


    def get(self, request, pk=None):
        if pk and User.objects.filter(id=pk).exists():
            qs = User.objects.filter(id=pk)
        else:
            qs = User.objects.all()
        serializer = UserSerializer(qs, many=True)
        return Response(serializer.data)



    def post(self, request):
        post_group = request.POST['group']
        group = Group.objects.get(name=post_group)
        user_serializer = UserSerializer(data={
            'username':request.data.get('email'),
            'first_name':request.data.get('fname'),
            'last_name':request.data.get('lname'),
            'email':request.data.get('email'), 
            'password':request.data.get('password'),
            'is_superuser':True,
            'is_staff':True,
            'is_active':True,
        })

        userdata_serializer = UserdataSerializer(data={
            'mobile':request.data.get('mobile'),
            'email':request.data.get('email'),
            'designation':post_group,
            'user_status':'True',
            'first_name':request.data.get('fname'),
            'last_name':request.data.get('lname'),
        })

        user_errors = user_serializer.is_valid()
        userdata_errors = userdata_serializer.is_valid()

        if user_errors and userdata_errors:
            user_serializer.save()
            user = User.objects.get(id=user_serializer.data.get('id'))
            user.set_password(request.data.get('password'))
            user.is_superuser =False
            user.is_staff =True
            user.groups.add(group)
            user.save()
            userdata_serializer.save(user=user)
            return Response({'status':'Success','msg':'Registration successful', 'user': user_serializer.data, 'customer':userdata_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error: Please Provide Valid Data", "errors":dict(user_serializer.errors, **userdata_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

# by biswajit paloi

def permission_string_method(self):
    return '%s' % (self.name)
Permission.__str__ = permission_string_method



@method_decorator(login_required(login_url='admin_login'), name='dispatch')
@method_decorator(staff_member_required(), name='dispatch')
@method_decorator(check_user_able_to_see_auth_app_page('view_group', 'add_group'), name='dispatch')
class CreateGroup(View):

    def get(self, request, *args, **kwargs):

        groups = Group.objects.all()
        permission_names = []
        group_users = []
        permission = Permission.objects.all()

        
        for group in groups:
            group_users.append([user.email for user in group.user_set.all()])
            permission_names.append([permission.name for permission in group.permissions.all()])

        context = {
            'groups': zip(groups, permission_names,group_users),
            'permission': permission
        }
        return render(request, 'savaari-admin/Designation.html', context)


    def post(self, request):
        group_name = request.POST.get('group_name')
        permissions_list = request.POST.getlist('permission')
        permissions_list_id = []

        if Group.objects.filter(name=group_name).exists():
            messages.error(request, "same name disignation already exists")
            return redirect('AddPermitions')
        else:
            new_group = Group.objects.create(name=group_name)

            for perm in permissions_list:
                p = Permission.objects.get(name=perm)
                permissions_list_id.append(p.id)

            new_group.permissions.set(permissions_list_id)
            return redirect('AddPermitions')


@method_decorator(login_required(login_url='admin_login'), name='dispatch')
@method_decorator(staff_member_required(), name='dispatch')
@method_decorator(check_user_able_to_see_auth_app_page('view_group', 'add_group'), name='dispatch')
class GroupUpdateView(View):
    def get(self, request, *args, **kwargs):
        # Retrieve the group object and permissions
        group = get_object_or_404(Group, pk=kwargs['pk'])
        permission_names = [permission.name for permission in group.permissions.all()]
        permission = list(Permission.objects.all())
        print(permission)

        context = {
            'group': group,
            'permission': permission,
            'permission_names': permission_names
        }
        return render(request, 'savaari-admin/Designation_update.html', context)

    def post(self, request, *args, **kwargs):
        group_name = request.POST.get('group_name')
        # Retrieve the group object
        group = get_object_or_404(Group, pk=kwargs['pk'])

        group.name = group_name

        # Retrieve the list of permission names from POST data
        permissions_list = request.POST.getlist('permission')

        # Convert the permission names to IDs
        permissions_list_ids = []
        for perm_name in permissions_list:
            perm = Permission.objects.get(name=perm_name)
            permissions_list_ids.append(perm.id)

        # Update the group's permissions
        group.permissions.set(permissions_list_ids)

        # Save the updated group object
        group.save()

        messages.success(request, f'Permissions for group {group.name} have been updated.')
        return redirect('AddPermitions')



@method_decorator(login_required(login_url='admin_login'), name='dispatch')
@method_decorator(staff_member_required(), name='dispatch')
@method_decorator(check_user_able_to_see_auth_app_page('view_agentcredit', 'add_agentcredit'), name='dispatch')
class AgentCredits(View):
    
    def get(self, request, *args, **kwargs):
        agent = Agent.objects.all()
        agent_credit = AgentCredit.objects.all()
        with open("static/flight/airlines.json", "r") as f:
            airlines_json = json.load(f)
        return render(request, 'savaari-admin/credit.html',context={'airlines_json':airlines_json,'agent':agent,'agent_credits':agent_credit})

    def post(self, request, *args, **kwargs):
        user_obj = request.POST.get('user_name')
        amount = request.POST.get('amount')
        airlines_list = request.POST.getlist('airlines')
        format_data = "%H:%M"
        start_date = request.POST.get('start_date')
        start_time = request.POST.get('start_time')
        end_date = request.POST.get('end_date')
        end_time = request.POST.get('end_time')
        start_task_name= str(user_obj)+str(start_date)+str(start_time)
        end_task_name= str(user_obj)+str(end_date)+str(end_time)
        emailId = Agent.objects.get(agent_id=user_obj)
        wall_user = User.objects.get(email=emailId)
        agent = Agent.objects.get(user=wall_user)
        transaction_number = randint(1000000000, 9999999999)
        osn_id = str(transaction_number)
        transaction_number = 'CREDIT'+osn_id

        if AgentCredit.objects.filter(agent__user=wall_user).exists():
            credit_amount = AgentCredit.objects.filter(agent__user=wall_user).last().credit_balance
        else:
            credit_amount = 0
        credit_balance= float(credit_amount)+float(amount)
        
        a = AgentCredit(agent=emailId,start_time=start_time,trasaction_num=transaction_number,credit_balance=credit_balance,agent_excepting_airlines=airlines_list,status="Credit",amount=amount,start_date=start_date,end_date=end_date,end_time=end_time)
        a.save()
        
        return redirect('AgentCredit')
        # if not WalletDetails.objects.filter(email=emailId):
        #     wallet_activated_on = date.today()
        #     if(emailId != None):
        #         wall_user = User.objects.get(email=emailId)
        #         curl = WalletDetails.objects.create(username=wall_user,email=emailId,wallet_activated_on=wallet_activated_on,wallet_balance=0)
@login_required(login_url="admin_login")
@staff_member_required
def update_credit(request, id):
    emailId = request.POST.get('emailId')
    agentId = request.POST.get('agentId')
    creditamount = request.POST.get('creditamount')
    dueamount = request.POST.get('dueamount')
    transaction_number = randint(1000000000, 9999999999)
    osn_id = str(transaction_number)
    transaction_number = 'DEBIT'+osn_id
    emailId = Agent.objects.get(agent_id=agentId)
    wall_user = User.objects.get(email=emailId)
    agent = Agent.objects.get(user=wall_user)
    deduct_date = date.today()
    # if not WalletDetails.objects.filter(email=emailId):
    #     wallet_activated_on = date.today()
    #     if(emailId != None):
    #         wall_user = User.objects.get(email=emailId)
    #         print(wall_user)
    #         curl = WalletDetails.objects.create(username=wall_user,email=emailId,wallet_activated_on=wallet_activated_on,wallet_balance=0)
    if(emailId != None):
        credit_detail = (AgentCredit.objects.filter(agent=emailId).values()).latest('id')
    if (request.method == "POST"):
        # wall_user = User.objects.get(id=credit_detail['username_id'])
        wallet_bal = credit_detail['credit_balance']
        new_bal = float(wallet_bal)- float(creditamount)
        a = AgentCredit.objects.create(agent=emailId,trasaction_num=transaction_number,credit_balance=new_bal,amount=dueamount,deduct_date=deduct_date)
    mark = AgentCredit.objects.get(id=id)
    mark.amount = creditamount
    mark.status = "Debited"
    mark.save()
    return render(request, "savaari-admin/base.html", context={})



@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_commission','add_commission')
def commission(request):
    user_type = request.POST.get('user_type')
    commission_type = request.POST.get('commission_type')
    amount_type = request.POST.get('amount_type')
    amount = request.POST.get('amount')
    airline = request.POST.getlist('airlines')
    email = request.POST.getlist('email')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    route = request.POST.get('route')
    print(user_type,commission_type,amount_type,amount,airline,email,start_date,end_date,route)
    login_user = request.user
    with open("static/flight/airlines.json", "r") as f:
        air_list = json.loads(f.read())
    all_agent = Agent.objects.all()
    all_commission = list(Commission.objects.all().values())
    print(all_commission)
    if amount_type != None :
        cust1=Commission.objects.create(user=login_user,user_type=user_type,amount_type=amount_type,amount=amount,airline_type=airline,commission_type=commission_type,email=email,route=route,start_date=start_date,end_date=end_date)
    return render(request, 'savaari-admin/commission.html', context={'all_commission':all_commission,'air_list':air_list,'all_agent':all_agent})


@login_required(login_url="admin_login")
@staff_member_required
def mailbox(request):
    if request.method == "POST":
        recipient_list = []
        # email_from = request.POST.get("from")
        email_from = settings.EMAIL_HOST_USER
        email_to = request.POST.get("to")
        cc = request.POST.get("cc")
        subject = request.POST.get("subject")
        message = request.POST.get("quill-html")
        recipient_list.extend([email_to, cc])

        email = EmailMessage(
            subject,
            message,
            email_from,
            recipient_list
        )
        if request.FILES:
            uploaded_file = request.FILES['mail_file']
            email.attach(uploaded_file.name, uploaded_file.read(),
                         uploaded_file.content_type)
        email.send()

        print(f'message: {message}')
        print(recipient_list)

    return render(request=request, template_name="savaari-admin/Mailbox.html", context={})




@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_passenger','add_passenger')
def manual_ticket(request):
    
    users = User.objects.all().order_by('id')
    context = {'users': users}
    
    if request.method == "POST":
        
        username = request.user
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        
        booking_id = request.POST.get('booking_id')
        travel_trip = request.POST.get('travel_trip')
        meal = request.POST.get('meal')
        baggage = request.POST.get('baggage')
        
        duration = request.POST.get('duration')
        flight_status = request.POST.get('flight_status')
        pnr = request.POST.get('pnr')
        flight_class = request.POST.get('flight_class')
        
        base_price = request.POST.get('base_price')
        taf = request.POST.get('taf')
        meal_charges = request.POST.get('meal_charges')
        insurance_charges = request.POST.get('insurance_charges')
        baggage_charges = request.POST.get('baggage_charges')
        total_fare = request.POST.get('total_fare')
        paid_amount = request.POST.get('paid_amount')
        seat_charges = request.POST.get('seat_charges')
        
        gst_no = request.POST.get('gst_no')
        company_name = request.POST.get('company_name')
        gst_email = request.POST.get('alt_email')
        gst_mobile = request.POST.get('gst_mobile')
        address = request.POST.get('address')
        transaction_id = request.POST.get('transaction')
        
        airline_name = request.POST.get('airline1')
        origin_airport = request.POST.get('origin_airport1')
        dest_airport = request.POST.get('dest_airport1')
        flight_code = request.POST.get('flight_code1')
        flight_number = request.POST.get('flight_number1')
        stop = request.POST.get('stop1')
        departure_date = request.POST.get('departure_date1')
        departure_time = request.POST.get('departure_time1')
        arrival_date = request.POST.get('arrival_date1')
        arrival_time = request.POST.get('arrival_time1')
        dest = request.POST.get('dest1')
        src = request.POST.get('src1')
        
        passenger_count = request.POST.get('passenger_form_count')
        
        for i in range(int(passenger_count)):
            
            id=i+1;
            passenger_type = request.POST.get(f'passenger{id}')
            title = request.POST.get(f'title{id}')
            first_name = request.POST.get(f'first_name{id}')
            last_name = request.POST.get(f'last_name{id}')
            seat_no = request.POST.get(f'seat_no{id}')
            date_of_birth = request.POST.get(f'date_of_birth{id}')
            passport_no = request.POST.get(f'passport{id}')
            
            passenger_obj = Passenger(user=username, title=title, first_name=first_name, last_name=last_name, email=email,
                                      mobile=mobile, passenger_type=passenger_type, date_of_birth= date_of_birth,
                                      meal=meal, baggage=baggage, seat_no=seat_no, bookingId=booking_id, passport_no=passport_no,
                                      airline_name=airline_name, origin_airport=origin_airport, destination_airport=dest_airport,
                                      flight_code=flight_code, flight_number=flight_number, stop=stop, departure_date=departure_date,
                                      departure_time=departure_time,arrival_date=arrival_date, arrival_time=arrival_time,
                                      src=src, dest=dest, 
                                      duration=duration, flight_status=flight_status,pnr=pnr,flight_class=flight_class,
                                      base_price=base_price, taf=taf, meal_charges=meal_charges, insurance_charges=insurance_charges,
                                      baggage_charges=baggage_charges, total_fare=total_fare, paid_amount=paid_amount,
                                      gstno=gst_no, company_name=company_name, gst_email= gst_email, gst_mobile=gst_mobile,
                                      address=address, transaction_id=transaction_id)
            passenger_obj.save()
            
        messages.success(request, 'Manual Ticket form submitted successfully.')
        return render(request=request, template_name="savaari-admin/manual_ticket.html", context = context)
        
       
    return render(request=request, template_name="savaari-admin/manual_ticket.html", context = context)



@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_card','add_card')
def card_list(request):
    card = Card.objects.all().order_by('cardholder_name')
    context={'card_list': card}
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        if Card.objects.filter(card_number=card_number).exists():
            messages.error(request, "Card Number already exists")
        
        cardholder_name = request.POST.get('cardholder_name')
        expiry = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        
        d = expiry.split('-')
        year =d[0]
        month=d[1]
        expiry_date = datetime(int(year), int(month), 1)
        
        card_obj = Card(cardholder_name = cardholder_name, card_number = card_number, expiry_date = expiry_date, cvv = cvv)
        card_obj.save()
        
        messages.success(request, 'New card added successfully.')
        
    return render(request=request, template_name="savaari-admin/card_list.html", context = context)
            


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_pcc','add_pcc')
def pcc_list(request):
    pcc = Pcc.objects.all()
    context={'pcc_list': pcc}
    
    if request.method == 'POST':
        pcc_no = request.POST.get('pcc_no')
        purpose = request.POST.get('purpose')
        
        pcc_obj = Pcc(pcc=pcc_no, purpose=purpose)
        pcc_obj.save()
    
        messages.success(request, 'New Pcc added successfully.')
    return render(request, "savaari-admin/pcc_list.html", context)


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_card','change_card')
def update_card(request, id):
    
    card_status = request.POST.get('status')
    if card_status == 'active':
        card_list = Card.objects.exclude(id = id)
        for card in card_list:
            card.card_status = "inactive"
            card.save()
    card_obj = Card.objects.get(id=id)
    card_obj.card_status = card_status
    card_obj.save()
    
    return redirect('card_list')
    

@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_card','delete_card')
def delete_card(request, id):
    card = Card.objects.filter(id = id)
    card.delete()
    
    return redirect('card_list')


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_pcc','change_pcc')
def update_pcc(request, id):
    pcc_status = request.POST.get('status')
    pcc_purpose = request.POST.get('purpose')
    print(pcc_status)
    if pcc_status == 'active':
        pcc_list = Pcc.objects.filter(purpose=pcc_purpose).exclude(id = id)
        for pcc in pcc_list:
            pcc.pcc_status = "inactive"
            pcc.save()
    pcc_obj = Pcc.objects.get(id=id)
    pcc_obj.pcc_status = pcc_status
    pcc_obj.save()
    
    return redirect('pcc_list')


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_pcc','delete_pcc')
def delete_pcc(request, id):
    pcc = Pcc.objects.filter(id = id)
    pcc.delete()
    
    return redirect('pcc_list')



@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_walletdetails','add_walletdetails')
def deduct_wallet(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        amount= request.POST.get('amount')
        description= request.POST.get('description')
        
        if not User.objects.filter(email=user_email).exists():
            messages.error(request, "User does not exists")
            return redirect('deduct_wallet')
            
        
        if not WalletDetails.objects.filter(email=user_email):
            createWallet(user_email)
                    
        if(user_email != None):
            wallet_detail = (WalletDetails.objects.filter(email=user_email).values()).latest('id')
            print(wallet_detail)
        
        wall_user = User.objects.get(id=wallet_detail['username_id'])
        print(wall_user)
        
        wallet_bal = wallet_detail['wallet_balance']
        new_bal = float(wallet_bal) - float(amount)
        
        transaction_number = randint(1000000000, 9999999999)
        osn_id = str(transaction_number)
        transaction_number = 'ADMN'+osn_id
        
        curl = WalletDetails.objects.create(username=wall_user, email=user_email, wallet_balance=new_bal, amount=amount, trasc_type="Debit",
                                            transaction_mode="DEDUCT", transaction_status="Success", transaction_id=transaction_number, note="deducted from admin panel for deduct request "+str(description))
        
        
        messages.success(request, 'Wallet Balance deducted successfully.')
        
        return redirect('deduct_wallet')
        
    return render(request, "savaari-admin/deduct_wallet.html")



@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_walletdetails','add_walletdetails')
def agent_recharge_wallet(request, id):
    if request.method == 'POST':
        # agent_id = request.POST.get('agent_id')
        user_email = request.POST.get('email')
        amount= request.POST.get('amount')
        
        
        if not User.objects.filter(username=user_email).exists():
            messages.error(request, "User does not exists")
            return redirect('view_agent_profile', id)
            
        
        if not WalletDetails.objects.filter(email=user_email):
            createWallet(user_email)
                    
        if(user_email != None):
            wallet_detail = (WalletDetails.objects.filter(email=user_email).values()).latest('id')
            print(wallet_detail)
        
        wall_user = User.objects.get(id=wallet_detail['username_id'])
        
        
        wallet_bal = wallet_detail['wallet_balance']
        new_bal = float(wallet_bal) + float(amount)
        
        transaction_number = randint(1000000000, 9999999999)
        osn_id = str(transaction_number)
        transaction_number = 'ADMN'+osn_id
        
        curl = WalletDetails.objects.create(username=wall_user, email=user_email, wallet_balance=new_bal, amount=amount, trasc_type="Credit",
                                            transaction_mode="DEPOSIT", transaction_status="Success", transaction_id=transaction_number, note="deposited from admin panel foragent recharge request")
        
        # messages.success(request, 'Wallet Balance recharged successfully.')
        
        return redirect('view_agent_profile', id)
        
    return redirect('view_agent_profile', id)




@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_hotelmarkup','add_hotelmarkup')
def hotel_markup(request):
    login_user = request.user
    hotel_markup = HotelMarkup.objects.all().order_by('-id')
    
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        amount_type = request.POST.get('amount_type')
        amount = request.POST.get('amount')
        hotel_rating = request.POST.get('hotel_rating')
        
        if HotelMarkup.objects.filter(Q(hotel_rating__contains=hotel_rating) & Q(user_type__contains=user_type)):
            messages.error(request, 'Hotel Markup with this rating already exists')
            return render(request, "savaari-admin/hotel_markup.html", context={'hotel_markup': hotel_markup})
        
        
        markup = HotelMarkup(user=login_user, user_type=user_type, amount_type=amount_type, amount=amount, hotel_rating=hotel_rating)
        
        markup.save()
        
        messages.success(request, 'Hotel Markup submitted successfully.')

    return render(request, "savaari-admin/hotel_markup.html", context={'hotel_markup': hotel_markup})



@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_hotelmarkup','change_hotelmarkup')
def update_hotel_markup(request, id):
    
    amount = request.POST.get('amount')
    print("amount: ", amount)
    

    markup_obj = HotelMarkup.objects.get(id=id)
    markup_obj.amount = amount
    markup_obj.save()
    
    messages.success(request, 'Hotel Markup updated successfully.')

    return redirect('hotel_markup')


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_hotelmarkup','delete_hotelmarkup')
def delete_hotel_markup(request, id):
    markup_obj = HotelMarkup.objects.get(id=id)

    # delete the todo
    markup_obj.delete()

    messages.success(request, 'Hotel Markup deleted successfully.')

    return redirect('hotel_markup')
    

# by biswajit
def zoho_get_Contacts( email):
    access_token = ""
    refresh_token = "1000.73d335dfcc2f913d020cff9c7738b808.c54606b5a87005aec94ad30803494238"
    # authorize_url = "https://accounts.zoho.com/oauth/v2/auth"
    # token_url = "https://accounts.zoho.in/oauth/v2/token"
    # state = 'testing'
    # scope = 'ZohoInvoice.contacts.READ'
    # callback_uri = "http://127.0.0.1:8000/"
    client_id = '1000.IEMUXBYVYT9A5S8QZDE8XV2PQYJS0F'
    client_secret = 'b58d5a8fb31a3e92f7a2f8f65a049728d73e99d9f0'
    # organization_id = 60015754747
    r = requests.post(f"https://accounts.zoho.in/oauth/v2/token?refresh_token={refresh_token}&client_id={client_id}&client_secret={client_secret}&redirect_uri=http://127.0.0.1:8000/&grant_type=refresh_token")
    if r.ok:
        access = r.json()['access_token']
        access_token = access_token.replace(access_token,access)

    print(access_token)
    resp = requests.get(
        f'https://invoice.zoho.in/api/v3/contacts', 
        headers={'Authorization':f'Zoho-oauthtoken {access_token}'})
    json_data = resp.json()

    # print(json_data)
    contact_id = None
    for i in json_data['contacts']:
        if i['email'] == email:
            contact_id =  i['contact_id']
            break
    return contact_id

def zoho_create_Customers(flight_detail):
    # print(user._wrapped.__dict__)

    access_token = ""
    refresh_token = "1000.73d335dfcc2f913d020cff9c7738b808.c54606b5a87005aec94ad30803494238"

    client_id = '1000.IEMUXBYVYT9A5S8QZDE8XV2PQYJS0F'
    client_secret = 'b58d5a8fb31a3e92f7a2f8f65a049728d73e99d9f0'
    organization_id = 60015754747

    r = requests.post(f"https://accounts.zoho.in/oauth/v2/token?refresh_token={refresh_token}&client_id={client_id}&client_secret={client_secret}&redirect_uri=http://127.0.0.1:8000/&grant_type=refresh_token")

    if r.ok:
        access = r.json()['access_token']
        access_token = access_token.replace(access_token,access)
    body = {
        "contact_name": flight_detail.user.username,
        "contact_persons": [
            {
                "first_name": flight_detail.first_name,
                "last_name": flight_detail.last_name,
                "email": flight_detail.email,
            }
        ],
    }

    resp = requests.post(
        f'https://invoice.zoho.in/api/v3/contacts',
        data=json.dumps(body),
        headers={"Content-Type": "application/json",'Authorization':f'Zoho-oauthtoken {access_token}','X-com-zoho-invoice-organizationid':f'{organization_id}'})

    return resp.json()['contact']['contact_id']
     

def create_item(flight_detail):
     
    access_token = ""
    refresh_token = "1000.73d335dfcc2f913d020cff9c7738b808.c54606b5a87005aec94ad30803494238"

    client_id = '1000.IEMUXBYVYT9A5S8QZDE8XV2PQYJS0F'
    client_secret = 'b58d5a8fb31a3e92f7a2f8f65a049728d73e99d9f0'

    body = {
        "name": flight_detail.src+'-'+flight_detail.dest +','+
                flight_detail.bookingId +','+
                flight_detail.airline_name +','+
                flight_detail.flight_code +'-'+ flight_detail.flight_number,
    
        "rate": flight_detail.paid_amount,

        }
    
    # print(body)
    
    r = requests.post(f"https://accounts.zoho.in/oauth/v2/token?refresh_token={refresh_token}&client_id={client_id}&client_secret={client_secret}&redirect_uri=http://127.0.0.1:8000/&grant_type=refresh_token")

    if r.ok:
        access = r.json()['access_token']
        access_token = access
    else:
        pass

    resp = requests.post(
        url = 'https://invoice.zoho.in/api/v3/items', 
        data=json.dumps(body),
        headers={"Content-Type": "application/json",'Authorization':f'Zoho-oauthtoken {access_token}'})
    
    print(resp.json())

    try:
        return resp.json()['item']['item_id']
    except:
        return resp.json()['message']
    
     

@login_required(login_url="admin_login")
@staff_member_required
def zoho_invoice(request, ids):
    flight_detail = Passenger.objects.get(id=ids)
    email = flight_detail.user.email

    contact_id = zoho_get_Contacts(email)
    print(contact_id)
    if contact_id is None:
        contact_id = zoho_create_Customers(flight_detail)

    item_id = create_item(flight_detail)

    if item_id.isdigit():
        access_token = ""
        refresh_token = "1000.73d335dfcc2f913d020cff9c7738b808.c54606b5a87005aec94ad30803494238"

        authorize_url = "https://accounts.zoho.com/oauth/v2/auth"
        token_url = "https://accounts.zoho.in/oauth/v2/token"
        state = 'testing'
        scope = 'ZohoInvoice.invoices.CREATE'
        callback_uri = "http://127.0.0.1:8000/"
        client_id = '1000.IEMUXBYVYT9A5S8QZDE8XV2PQYJS0F'
        client_secret = 'b58d5a8fb31a3e92f7a2f8f65a049728d73e99d9f0'
        organization_id = 60015754747

        body = {
            "customer_id": contact_id,
            "date": "2013-11-17",
            "invoice_number": flight_detail.user.username+str(randint(1, 1000)),
            "line_items": [
                {
                "item_id": item_id,
                "rate": flight_detail.paid_amount,
                "quantity": 1,
                }
            ],
            "payment_options": {
                "payment_gateways": [
                    {
                        "configured": True,
                        "additional_field1": "standard",
                        "gateway_name": "Razorpay"
                    }
                ]
            },
            "allow_partial_payments": True,
        }

        r = requests.post(f"https://accounts.zoho.in/oauth/v2/token?refresh_token={refresh_token}&client_id={client_id}&client_secret={client_secret}&redirect_uri=http://127.0.0.1:8000/&grant_type=refresh_token")
        if r.ok:
            access = r.json()['access_token']
            access_token = access_token.replace(access_token,access)
        else:
            pass

        resp = requests.post(
            f'https://invoice.zoho.in/api/v3/invoices?organization_id={organization_id}', 
            data=json.dumps(body),
            headers={"Content-Type": "application/json",'Authorization':f'Zoho-oauthtoken {access_token}','X-com-zoho-invoice-organizationid':f'{organization_id}'})

        # print(resp.text)
        try:
            invoice_id = resp.json()['invoice']['invoice_number']
            messages.success(request, 'Your invoice has been created name as '+invoice_id+', please check your Zoho Dashboard')
            return redirect('flightbooking')
        except:
            invoice_id = resp.json()['message']
            messages.error(request, invoice_id)
            return redirect('flightbooking')
    else:
        messages.error(request, item_id)
        return redirect('flightbooking')





@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_agent')
def agent_transaction_excel(request):
    if request.method == 'POST':
        agent_id = request.POST.get('agent_id')
        agent = Agent.objects.filter(email=agent_id)
        if agent.exists():
            user = Agent.objects.get(email=agent_id).user
            
            wallet_list =  WalletDetails.objects.filter(username=user).values_list('email', 'amount', 'wallet_balance', 'transaction_id', 'trasc_type', 'transaction_mode', 'transaction_date', 'transaction_status')
            
            column_list = ['Email', 'Amount', 'Wallet Balance', 'Transaction Id', 'Transaction Type', 'Transaction Mode', 'Transaction Date', 'Transaction Status']
            response = createExcelSheet(wallet_list, column_list, "transaction_list.xls")
            messages.success(request, 'Download successful')
            return response
            
        else:
            messages.error(request, 'Agent not found')
    return redirect('agent_list')


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_corporatecust')
def corporate_manager_excel(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        corp_cust = CorporateCust.objects.filter(email=email)
        if corp_cust.exists():
            user = CorporateCust.objects.get(email=email).user
            
            wallet_list =  WalletDetails.objects.filter(username=user).values_list('email', 'amount', 'wallet_balance', 'transaction_id', 'trasc_type', 'transaction_mode', 'transaction_date', 'transaction_status')
            
            column_list = ['Email', 'Amount', 'Wallet Balance', 'Transaction Id', 'Transaction Type', 'Transaction Mode', 'Transaction Date', 'Transaction Status']
            response = createExcelSheet(wallet_list, column_list, "corporate_transaction_list.xls")
            messages.success(request, 'Download successful')
            return response
            
        else:
            messages.error(request, 'Corporate Manager not found')
    return redirect('corporation_list')

@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_customer')
def customer_manager_excel(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        cust = Customer.objects.filter(email=email)
        if cust.exists():
            cust_user = Customer.objects.get(email=email).user
        
            wallet_list =  WalletDetails.objects.filter(username=cust_user).values_list('email', 'amount', 'wallet_balance', 'transaction_id', 'trasc_type', 'transaction_mode', 'transaction_date', 'transaction_status')
            
            column_list = ['Email', 'Amount', 'Wallet Balance', 'Transaction Id', 'Transaction Type', 'Transaction Mode', 'Transaction Date', 'Transaction Status']
            response = createExcelSheet(wallet_list, column_list, "cutomer_transaction_list.xls")
            messages.success(request, 'Download successful')
            return response
            
        else:
            messages.error(request, 'Customer not found')
    return redirect('customer_list')



@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_passenger')
def flight_booking_excel(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.filter(username=user_id)
        if user.exists():
            try:
                passenger_list = Passenger.objects.filter(user=User.objects.get(username=user_id)).values_list('first_name', 'last_name', 'email', 'bookingId')
                column_list = ['First Name', 'Last Name', 'Email', 'Booking Id']
                response = createExcelSheet(passenger_list, column_list, "flight_booking_list.xls")
                messages.success(request, 'Download successful')
                return response
            except Passenger.DoesNotExist:
                messages.error(request, 'Flight Booking Records not found')
        else:
            messages.error(request, 'User not found')
    
    return redirect('flightbooking')


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_hotelbookinghistory')
def hotel_booking_excel(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.filter(username=user_id)
        if user.exists():
                booking_list = HotelBookingHistory.objects.filter(user=User.objects.get(username=user_id)).values_list('first_name', 'last_name', 'email', 'hotel_name','bookingId', 'osh_bookingId')
                if booking_list.exists():
                    column_list = ['First Name', 'Last Name', 'Email', 'Hotel Name', 'BookingId', 'Osh_BookingId']
                    response = createExcelSheet(booking_list, column_list, "hotel_booking_list.xls")
                    messages.success(request, 'Download successful')
                    return response
                else:
                    messages.error(request, 'Hotel Booking Records not found')
        else:
            messages.error(request, 'User not found')
    
    return redirect('hotelbooking')


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_insurance_policy')
def insurance_booking_excel(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.filter(username=user_id)
        if user.exists():
            try:
                booking_list = Insurance_Policy.objects.filter(user=User.objects.get(username=user_id)).values_list('first_name', 'last_name', 'email', 'amount','category', 'plan_code', 'reference_id', 'policy_no')
                column_list = ['First Name', 'Last Name', 'Email', 'Amount', 'Category', 'Plan Code', 'Reference Id', 'Policy No']
                response = createExcelSheet(booking_list, column_list, "insurance_booking_list.xls")
                messages.success(request, 'Download successful')
                return response
            except Insurance_Policy.DoesNotExist:
                messages.error(request, 'Insurance Booking Records not found')
        else:
            messages.error(request, 'User not found')
    
    return redirect('insurance_booking_list')


@login_required(login_url="admin_login")
@check_user_able_to_see_adminpanel_app_page('view_refundflight')
@staff_member_required
def refund_excel(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.filter(username=user_id)
        if user.exists():
            try:
                refund_list = RefundFlight.objects.filter(user=User.objects.get(username=user_id)).values_list('Refund_bookingid', 'Refund_flight_date', 'Refund_query', 'Refund_status', 'Refund_amount')
                column_list = ['Refund_bookingid', 'Refund_flight_date', 'Refund_query', 'Refund_status', 'Refund_amount']
                response = createExcelSheet(refund_list, column_list, "refund_list.xls")
                messages.success(request, 'Download successful')
                return response
            except RefundFlight.DoesNotExist:
                messages.error(request, 'Refund Flight Records not found')
        else:
            messages.error(request, 'User not found')
    
    return redirect('refund')


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_rescheduleflight')
def reschedule_excel(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.filter(username=user_id)
        if user.exists():
            try:
                reschedule_list = RescheduleFlight.objects.filter(user=User.objects.get(username=user_id)).values_list('Reschedule_bookingid', 'Reschedule_flight_date', 'Reschedule_query', 'Reschedule_status')
                column_list = ['Reschedule_bookingid', 'Reschedule_flight_date', 'Reschedule_query', 'Reschedule_status']
                response = createExcelSheet(reschedule_list, column_list, "reschedule_list.xls")
                messages.success(request, 'Download successful')
                return response
            except RescheduleFlight.DoesNotExist:
                messages.error(request, 'Reschedule Flight Records not found')
        else:
            messages.error(request, 'User not found')
    
    return redirect('reschedule')


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_deposit')
def deposit_excel(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.filter(username=user_id)
        if user.exists():
            try:
                deposit_list = Deposit.objects.filter(user=User.objects.get(username=user_id)).values_list('email_or_phone', 'deposit_type', 'amount', 'bank_name', 'deposite_branch', 'trasaction_num', 'dep_status', 'deposit_slip')
                column_list = ['email_or_phone', 'deposit_type', 'amount', 'bank_name', 'deposite_branch', 'trasaction_num', 'dep_status', 'deposit_slip']
                response = createExcelSheet(deposit_list, column_list, "deposit_list.xls")
                messages.success(request, 'Download successful')
                return response
            except Deposit.DoesNotExist:
                messages.error(request, 'Deposit Request Records not found')
        else:
            messages.error(request, 'User not found')
    
    return redirect('deposit_request')


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_refundflight', 'change_refundflight')
def update_refund(request, id):
    booking_id = request.POST.get('booking_id')
    Refund_status = request.POST.get('Refund_status')
    Refund_amount = request.POST.get('Refund_amount')
    with open("flight_data.txt", "w") as file:
        file.write(str(booking_id))
        file.close()
    refund = RefundFlight.objects.get(id=id)
    refund.Refund_status = Refund_status
    refund.Refund_amount = Refund_amount
    refund.save()
    pass_name = list(Passenger.objects.filter(bookingId=booking_id).values())
    pass_email = pass_name[0]['email']
    transaction_number = randint(1000000000, 9999999999)
    osn_id = str(transaction_number)
    transaction_number = 'CANCEL'+osn_id
    if not WalletDetails.objects.filter(email=pass_email):
        wallet_activated_on = date.today()
        if(pass_email != None):
            wall_user = User.objects.get(email=pass_email)
            print(wall_user)
            curl = WalletDetails.objects.create(username=wall_user,email=pass_email,wallet_activated_on=wallet_activated_on,wallet_balance=0)
    if(pass_email != None):
        wallet_detail = (WalletDetails.objects.filter(email=pass_email).values()).latest('id')
        print(wallet_detail)
    if (request.method == "POST") and (Refund_status == "Completed"):
        wall_user = User.objects.get(id=wallet_detail['username_id'])
        print(wall_user)
        wallet_bal = wallet_detail['wallet_balance']
        new_bal = float(wallet_bal)+ float(Refund_amount)
        curl = WalletDetails.objects.create(username=wall_user,email=pass_email,wallet_balance=new_bal,amount=Refund_amount,trasc_type="Credit",transaction_mode="DEPOSIT",transaction_status="Success",transaction_id=transaction_number,note="Refund for Cancellation of BookingId "+booking_id)



    smtpHost = "smtp.gmail.com"
    smtpPort = 587
    mailUname = 'no-reply@onlinesavaari.com'
    mailPwd = 'afbzoctjmpppkwvk'
    fromEmail = 'no-reply@onlinesavaari.com'

    # mail body, recepients, attachment files
    mailSubject = "Refund Request Status Changed"
    mailContentHtml = "Dear "+ str(pass_email) + ", Your Refund request status has been changed to "+ Refund_status+ ". Thank You."

    recepientsMailList = [pass_email]
    attachmentFpaths = ["flight/logo.png"]
    sendEmail(smtpHost, smtpPort, mailUname, mailPwd, fromEmail,
              mailSubject, mailContentHtml, recepientsMailList, attachmentFpaths)

    print("execution complete...")

    return render(request, "savaari-admin/base.html", context={})


@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_insurance_policy', 'add_insurance_policy')
def insurance_booking_list(request):
    if request.method == "POST":
        reference_id = request.POST.get("reference_id")
        insurance_detail = Insurance_Policy.objects.get(reference_id=reference_id)
        plan_details_list = get_insurance_plan_name(insurance_detail.total_days, str(insurance_detail.date_of_birth),insurance_detail.plan_code )
        context={'insurance': insurance_detail, 'plan': plan_details_list[0]}
        return render(request, "savaari-admin/view_insurance_admin.html", context)
        # return JsonResponse(context,  safe=False)
    
    insurance_policy = Insurance_Policy.objects.all()
    context = {'insurance_policy': insurance_policy}
    return render(request, "savaari-admin/insurance_booking_list.html", context)




@login_required(login_url="admin_login")
@staff_member_required
@check_user_able_to_see_adminpanel_app_page('view_insurance_policy', 'change_insurance_policy')
def update_insurance_booking(request, id):
    insurance_status = request.POST.get('insurance_status')
    print(insurance_status, "insurance_status")
    insurance = Insurance_Policy.objects.get(id=id)
    insurance.insurance_status = insurance_status
    insurance.save()
    return redirect('insurance_booking_list')