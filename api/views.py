from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import logout
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from random import randint
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import os
from onlinesavaari.models import Customer , Agent ,CorporateCust
from flight.models import Passenger
from wallet.models import Transaction
from rest_framework.permissions import IsAuthenticated
from adminpanel.models import *

# Create your views here.

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
class GetCountriesListAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            countries = Country.objects.filter(id=pk)
        else:
            countries = Country.objects.all()

        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)


class RegisterAgentAPI(APIView):
    authentication_classes = []
    permission_classes = []
    

    def get(self, request, pk=None):
        if pk and Agent.objects.filter(id=pk).exists():
            qs = Agent.objects.filter(id=pk)
        else:
            qs = Agent.objects.all()
        serializer = AgentSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.data.get('password', None) != request.data.get('confirm_password', None):
            return Response({"status": "Error", "errors":"Passwords do not match!"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            osn_id = randint(100000, 999999)
            osn_id = str(osn_id)
            agent_id = 'OSAG'+osn_id
        except:
            osn_id = randint(10000, 99999)
            osn_id = str(osn_id)
            agent_id = 'OSAgent'+osn_id

        user_serializer = UserSerializer(data={
            'username':request.data.get('email'),
            'first_name':request.data.get('first_name'),
            'last_name':request.data.get('last_name'),
            'email':request.data.get('email'), 
            'password':request.data.get('password'),
        })
        documents = request.FILES.get('doc')
        email = request.POST.get('email')
        print(email)
        agent_serializer = AgentSerializer(data={
            'first_name':request.data.get('first_name'),
            'last_name':request.data.get('last_name'),
            'mobile':request.data.get('mobile'),
            'email':request.data.get('email'),
            'agency_name':request.data.get('agency_name'),
            'agency_address':request.data.get('agency_address'),
            'pincode':request.data.get('pincode'),
            'country':request.data.get('country'),
            'gstin':request.data.get('gstin'),
            'gst_state':request.data.get('gst_state'),
            'agent_id':agent_id,
            'documents':documents,
        })

        user_errors = user_serializer.is_valid()
        agent_errors = agent_serializer.is_valid()

        if user_errors and agent_errors:
            user_serializer.save()
            user = User.objects.get(id=user_serializer.data.get('id'))
            user.set_password(request.data.get('password'))
            user.save()
            agent_serializer.save(user=user)
            doc = Documents.objects.create(username = email, doc=documents)
            return Response({'status':'Success','msg':'Registration successful', 'user': user_serializer.data, 'customer':agent_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error: Please Provide Valid Data", "errors":dict(user_serializer.errors, **agent_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk or not Agent.objects.filter(id=pk).exists():
            return Response({"status": "Error", "reason": 'Please provide valid Agent ID!'}, status=status.HTTP_400_BAD_REQUEST)
        
        qs = Agent.objects.get(id=pk)

        serializer = AgentSerializer(qs, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'status':'Success','msg':'Agent Updated successfully!', 'data':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error", "reason": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class RegisterCustomerAPI(APIView):
    authentication_classes = []
    permission_classes = []
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "online_savaari/sign-up.html"

    def get(self, request, pk=None):
        # if pk and Customer.objects.filter(id=pk).exists():
        #     qs = Customer.objects.filter(id=pk)
        # else:
        #     qs = Customer.objects.all()
        #     qs, many=True
        serializer = CustomerSerializer()
        return Response(serializer.data)

    def post(self, request):
        username = request.data.get('Email')
        first_name = request.data.get('Firstname')
        last_name = request.data.get('Lastname')
        email = request.data.get('Email')
        password = request.data.get('Password')
        password1 = request.data.get('Password1')
        phone = request.data.get('phone')
        
        
        if password == password1:
            # return Response({"status": "Error", "errors":"Passwords do not match!"}, status=status.HTTP_400_BAD_REQUEST)

            user_serializer = UserSerializer(data={
                'username':request.data.get('Email'),
                'first_name':request.data.get('Firstname'),
                'last_name':request.data.get('Lastname'),
                'email':request.data.get('Email'), 
                'password':make_password(request.data.get('Password'))
            })
            
            customer_serializer = CustomerSerializer(data={
                'first_name':request.data.get('Firstname'),
                'last_name':request.data.get('Lastname'),
                'email':request.data.get('Email'),
                'mobile':request.data.get('phone'),
                'gst_state':request.data.get('State'),
                'gstin':request.data.get('GST'),
                'pincode':request.data.get('Pin'),
                'address':request.data.get('Address'),
            })
            
            user_errors = user_serializer.is_valid()
            customer_errors = customer_serializer.is_valid()
            
            if user_errors:
                user_serializer.save()
                user = User.objects.get(id=user_serializer.data.get('id'))
                my_group = Group.objects.get(name='Customer') 
                print(my_group)
                my_group.user_set.add(user)
                if customer_errors:
                    customer_serializer.save(user=user)
                    # return Response({'status':'Success','msg':'Registration successful', 'user': user_serializer.data, 'customer':customer_serializer.data}, status=status.HTTP_200_OK,template_name='online_savaari/index.html')
                    return render(request, "online_savaari/index.html" )
            else:
                # return Response({"status": "Error: Please Provide Valid Data", "errors":dict(user_serializer.errors, **customer_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST , template_name="online_savaari/sign-up.html")
                return render(request, "online_savaari/sign-up.html" )
        return render(request, "online_savaari/sign-up.html" )

    def put(self, request, pk=None):
        if not pk or not Customer.objects.filter(id=pk).exists():
            return Response({"status": "Error", "reason": 'Please provide valid Customer ID!'}, status=status.HTTP_400_BAD_REQUEST)
        
        qs = Customer.objects.get(id=pk)

        serializer = CustomerSerializer(qs, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'status':'Success','msg':'Customer Updated successfully!', 'data':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error", "reason": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class RegisterCorporateCustAPI(APIView):
    authentication_classes = []
    permission_classes = []
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "online_savaari/agency-signup.html"

    def get(self, request, pk=None):
        # if pk and CorporateCust.objects.filter(id=pk).exists():
        #     qs = CorporateCust.objects.filter(id=pk)
        # else:
        #     qs = CorporateCust.objects.all()
        # qs, many=True
        serializer = CorporateCustSerializer()
        return Response(serializer.data)

    def post(self, request):
        username = request.POST.get('Email')
        first_name = request.POST.get('First_Name')
        Middle_Name = request.POST.get('Middle_Name')
        last_name = request.POST.get('Last_Name')
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        Type = request.POST.get('Type')
        Company = request.POST.get('Company')
        Address = request.POST.get('Address')
        State = request.POST.get('State')
        City = request.POST.get('City')
        Pin = request.POST.get('Pin')
        GST = request.POST.get('GST')
        phone = request.POST.get('phone')
        pan_no = request.POST.get('pan_no')
        print(username, email, password ,first_name, last_name , Type ,Company,Address,State,City,Pin,GST,phone,pan_no )
        
        
        flage = True
        
        social = ['yahoo.com','rediffmail.com','rediff.com','outlook.com']
        
        # email = request.data.get('email')
        # try:
        #     res = email.split('@')[1]
        # except:
        #     return Response({"status": "Error", "errors":"Please provide valid email address!"}, status=status.HTTP_400_BAD_REQUEST)

        # if res in social:
        #     return Response({"status": "Error", "errors":"Please enter Corporate email ID"}, status=status.HTTP_400_BAD_REQUEST)

        # if request.data.get('password', None) != request.data.get('confirm_password', None):
        #     return Response({"status": "Error", "errors":"Passwords do not match!"}, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(data={
            'username':request.data.get('Email'),
            'first_name':request.data.get('First_Name'),
            'last_name':request.data.get('Last_Name'),
            'email':request.data.get('Email'), 
            'password':make_password(request.data.get('Password'))
        })
        gstin = request.data.get('gstin')
        print(gstin)
        corporate_serializer = CorporateCustSerializer(data={
            'first_name':request.data.get('First_Name' ) ,
            'last_name':request.data.get('Last_Name' ) ,
            'mobile':request.data.get('phone'),
            'email':(request.data.get('Email')).lower(),
            'address':request.data.get('Address'),
            'gstin':request.data.get('gstin'),
            'gst_state':request.data.get('State'),
            'pincode':request.data.get('Pin'),
            'pan_no':request.data.get('pan_no'),
            'annual_spent':request.data.get('annual_spent'),
            # 'gstin':company_gstin,
        })
        try:
            osn_id = randint(10000, 99999)
            osn_id = str(osn_id)
            agent_id = 'OSAgent'+osn_id
        except:
            osn_id = randint(10000, 99999)
            osn_id = str(osn_id)
            agent_id = 'OSAgent'+osn_id
        documents = request.FILES.get('doc')
        email = request.POST.get('Email')
        print(email)
        agent_serializer = AgentSerializer(data={
            'first_name':request.data.get('First_Name' ) ,
            'last_name':request.data.get('Last_Name' ) ,
            'mobile':request.data.get('phone'),
            'email':(request.data.get('Email')).lower(),
            'agency_name':request.data.get('Company'),
            'agency_address':request.data.get('Address'),
            'gstin':request.data.get('GST'),
            'pincode':request.data.get('Pin'),
            'gst_state':request.data.get('State'),
            'pan_no':request.data.get('pan_no'),
            'annual_spent':request.data.get('annual_spent'),
            'agent_id':agent_id,
        })
        first_name = request.POST.get('First_Name')
        first_name = first_name.upper()
        print(corporate_serializer)
        user_errors = user_serializer.is_valid()
        customer_errors = corporate_serializer.is_valid()
        print("ereer",user_errors,customer_errors)
        agent_errors = agent_serializer.is_valid()
        print(user_errors)
        print(agent_errors)
        error_mgs = None
        if user_errors:
            res = email.split('@')[1]
            if request.data.get('password', None) == request.data.get('confirm_password', None):
                if Type == 'Business':
                    if res not in social:
                        if flage == True:
                            if corporate_serializer: 
                                user = user_serializer.save()
                                user.is_active = False
                                user.save()
                                user = User.objects.get(id=user_serializer.data.get('id'))
                                my_group = Group.objects.get(name='Corporate') 
                                print(customer_errors)
                                my_group.user_set.add(user)
                                if customer_errors:
                                    corporate_serializer.save(user=user)
                                    # mail server parameters
                                    smtpHost = "smtp.gmail.com"
                                    smtpPort = 587
                                    mailUname = 'no-reply@onlinesavaari.com'
                                    mailPwd = 'afbzoctjmpppkwvk'
                                    fromEmail = 'no-reply@onlinesavaari.com'

                                    # mail body, recepients, attachment files
                                    mailSubject = "Welcome to Online Savaari"
                                    mailContentHtml = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"> <head>  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <meta name="x-apple-disable-message-reformatting"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <title></title> <style type="text/css"> @media only screen and (min-width: 660px) { .u-row { width: 640px !important; } .u-row .u-col { vertical-align: top; } .u-row .u-col-100 { width: 640px !important; } } @media (max-width: 660px) { .u-row-container { max-width: 100% !important; padding-left: 0px !important; padding-right: 0px !important; } .u-row .u-col { min-width: 320px !important; max-width: 100% !important; display: block !important; } .u-row { width: calc(100% - 40px) !important; } .u-col { width: 100% !important; } .u-col > div { margin: 0 auto; } } body { margin: 0; padding: 0; } table, tr, td { vertical-align: top; border-collapse: collapse; } p { margin: 0; } .ie-container table, .mso-container table { table-layout: fixed; } * { line-height: inherit; } a[x-apple-data-detectors='true'] { color: inherit !important; text-decoration: none !important; } table, td { color: #000000; } #u_body a { color: #0000ee; text-decoration: underline; } </style> </head> <body class="clean-body u_body" style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #e7e7e7;color: #000000">   <table id="u_body" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #e7e7e7;width:100%" cellpadding="0" cellspacing="0"> <tbody> <tr style="vertical-align: top"> <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">  <div class="u-row-container" style="padding: 0px;background-color: transparent"> <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 640px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #f7dbbe;"> <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">   <div class="u-col u-col-100" style="max-width: 320px;min-width: 640px;display: table-cell;vertical-align: top;"> <div style="background-color: #ffffff;height: 100%;width: 100% !important;"> <div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"> <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:30px 10px 20px;font-family:arial,helvetica,sans-serif;" align="left"> <table width="100%" cellpadding="0" cellspacing="0" border="0"> <tr> <td style="padding-right: 0px;padding-left: 0px;" align="center"> <img align="center" border="0" src="https://onlinesavaari.com/static/main/images/logo.png" alt="Image" title="Image" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 100%;max-width: 135px;" width="135"/> </td> </tr> </table> </td> </tr> </tbody> </table> </div> </div> </div>   </div> </div> </div> <div class="u-row-container" style="padding: 0px;background-color: transparent"> <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 640px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #f7dbbe;"> <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">   <div class="u-col u-col-100" style="max-width: 320px;min-width: 640px;display: table-cell;vertical-align: top;"> <div style="background-color: #ffffff;height: 100%;width: 100% !important;"> <div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"> <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left"> <div style="line-height: 150%; text-align: left; word-wrap: break-word;"> <p style="font-size: 14px; line-height: 150%; text-align: center;"><span style="color: #444444; font-size: 14px; line-height: 21px;"><strong><span style="font-size: 38px; line-height: 57px;">Welcome</span></strong></span></p> <p style="font-size: 14px; line-height: 150%; text-align: center;"><strong><span style="font-size: 38px; line-height: 57px;"><span style="color: #ec8c30; font-size: 38px; line-height: 57px;">"""+first_name+"""</span></span></strong></p> </div> </td> </tr> </tbody> </table> <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:10px 10px 15px;font-family:arial,helvetica,sans-serif;" align="left"> <div style="line-height: 150%; text-align: left; word-wrap: break-word;"> <p style="font-size: 14px; line-height: 150%; text-align: center;">Thanks for signing up with Online Savaari. We'll be sending an conformation email </p> <p style="font-size: 14px; line-height: 150%; text-align: center;">after verifying the documents.</p> </div> </td> </tr> </tbody> </table> </div> </div> </div>   </div> </div> </div> <div class="u-row-container" style="padding: 0px;background-color: transparent"> <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 640px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #ffffff;"> <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">   <div class="u-col u-col-100" style="max-width: 320px;min-width: 640px;display: table-cell;vertical-align: top;"> <div style="height: 100%;width: 100% !important;"> <div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"> <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px 30px;font-family:arial,helvetica,sans-serif;" align="left"> <div align="center"> <div style="display: table; max-width:83px;">   <table align="left" border="0" cellspacing="0" cellpadding="0" width="32" height="32" style="width: 32px !important;height: 32px !important;display: inline-block;border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;margin-right: 10px"> <tbody><tr style="vertical-align: top"><td align="left" valign="middle" style="word-break: break-word;border-collapse: collapse !important;vertical-align: top"> <a href="https://facebook.com/OnlineSavaari" title="Facebook" target="_blank"> <img src="https://cdn.tools.unlayer.com/social/icons/circle/facebook.png" alt="Facebook" title="Facebook" width="32" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: block !important;border: none;height: auto;float: none;max-width: 32px !important"> </a> </td></tr> </tbody></table>   <table align="left" border="0" cellspacing="0" cellpadding="0" width="32" height="32" style="width: 32px !important;height: 32px !important;display: inline-block;border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;margin-right: 0px"> <tbody><tr style="vertical-align: top"><td align="left" valign="middle" style="word-break: break-word;border-collapse: collapse !important;vertical-align: top"> <a href="https://twitter.com/OnlineSavaari" title="Twitter" target="_blank"> <img src="https://cdn.tools.unlayer.com/social/icons/circle/twitter.png" alt="Twitter" title="Twitter" width="32" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: block !important;border: none;height: auto;float: none;max-width: 32px !important"> </a> </td></tr> </tbody></table>   </div> </div> </td> </tr> </tbody> </table> </div> </div> </div>   </div> </div> </div> <div class="u-row-container" style="padding: 0px;background-color: transparent"> <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 640px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;"> <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">   <div class="u-col u-col-100" style="max-width: 320px;min-width: 640px;display: table-cell;vertical-align: top;"> <div style="height: 100%;width: 100% !important;"> <div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"> <table class="addressContent" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:6px 10px 8px;font-family:arial,helvetica,sans-serif;" align="left"> <div style="line-height: 160%; text-align: left; word-wrap: break-word;"> <p style="text-align: center; font-size: 14px; line-height: 160%;"><span style="font-size: 12px; line-height: 19.200000000000003px;"><strong><span style="line-height: 19.200000000000003px; font-size: 12px;">Our mailing address is:</span></strong></span></p> <p style="text-align: center; font-size: 14px; line-height: 160%;"><span style="font-size: 12px; line-height: 19.200000000000003px;">support@onlinesavaari.com</span></p> </div> </td> </tr> </tbody> </table> </div> </div> </div>   </div> </div> </div>  </td> </tr> </tbody> </table>   </body> </html>"""
                                    recepientsMailList = [email]
                                    attachmentFpaths = ["flight/logo.png"]
                                    sendEmail(smtpHost, smtpPort, mailUname, mailPwd, fromEmail,
                                              mailSubject, mailContentHtml, recepientsMailList, attachmentFpaths)

                                    print("execution complete...")
                                    succ_mgs = 'You Are Successfully Registered!'
                                    # return Response({'status':'Success','msg':'Registration successful', 'user': user_serializer.data, 'customer':customer_serializer.data}, status=status.HTTP_200_OK,template_name='online_savaari/index.html')
                                    return render(request, "online_savaari/agency-signup.html",context={'succ_mgs': succ_mgs})
                                else:
                                    error_mgs = 'Email ID already exists'
                                    return render(request, "online_savaari/agency-signup.html",context={'error_mgs': error_mgs})
                            else:
                                error_mgs = 'please enter All fields'
                                return render(request, "online_savaari/agency-signup.html",context={'error_mgs': error_mgs})
                    else: 
                        error_mgs = 'Please enter Corporate email ID'
                        return render(request, "online_savaari/agency-signup.html",context={'error_mgs': error_mgs})
                if Type == 'Partner':
                    if flage == True:
                        if agent_serializer:
                            print("work2")
                            user =  user_serializer.save()
                            user.is_active = False
                            user.save()
                            user = User.objects.get(id=user_serializer.data.get('id'))
                            my_group = Group.objects.get(name='Agent') 
                            print(my_group)
                            my_group.user_set.add(user)
                            print("work3")
                            if agent_errors:
                                print("work4")
                                agent_serializer.save(user=user)
                                doc = Documents.objects.create(username = email, doc=documents)
                                agent_serializer.save(user=user)
                                # mail server parameters
                                smtpHost = "smtp.gmail.com"
                                smtpPort = 587
                                mailUname = 'no-reply@onlinesavaari.com'
                                mailPwd = 'afbzoctjmpppkwvk'
                                fromEmail = 'no-reply@onlinesavaari.com'

                                # mail body, recepients, attachment files
                                mailSubject = "Welcome to Online Savaari"
                                mailContentHtml = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"> <head>  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <meta name="x-apple-disable-message-reformatting"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <title></title> <style type="text/css"> @media only screen and (min-width: 660px) { .u-row { width: 640px !important; } .u-row .u-col { vertical-align: top; } .u-row .u-col-100 { width: 640px !important; } } @media (max-width: 660px) { .u-row-container { max-width: 100% !important; padding-left: 0px !important; padding-right: 0px !important; } .u-row .u-col { min-width: 320px !important; max-width: 100% !important; display: block !important; } .u-row { width: calc(100% - 40px) !important; } .u-col { width: 100% !important; } .u-col > div { margin: 0 auto; } } body { margin: 0; padding: 0; } table, tr, td { vertical-align: top; border-collapse: collapse; } p { margin: 0; } .ie-container table, .mso-container table { table-layout: fixed; } * { line-height: inherit; } a[x-apple-data-detectors='true'] { color: inherit !important; text-decoration: none !important; } table, td { color: #000000; } #u_body a { color: #0000ee; text-decoration: underline; } </style> </head> <body class="clean-body u_body" style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #e7e7e7;color: #000000">   <table id="u_body" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #e7e7e7;width:100%" cellpadding="0" cellspacing="0"> <tbody> <tr style="vertical-align: top"> <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">  <div class="u-row-container" style="padding: 0px;background-color: transparent"> <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 640px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #f7dbbe;"> <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">   <div class="u-col u-col-100" style="max-width: 320px;min-width: 640px;display: table-cell;vertical-align: top;"> <div style="background-color: #ffffff;height: 100%;width: 100% !important;"> <div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"> <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:30px 10px 20px;font-family:arial,helvetica,sans-serif;" align="left"> <table width="100%" cellpadding="0" cellspacing="0" border="0"> <tr> <td style="padding-right: 0px;padding-left: 0px;" align="center"> <img align="center" border="0" src="https://onlinesavaari.com/static/main/images/logo.png" alt="Image" title="Image" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 100%;max-width: 135px;" width="135"/> </td> </tr> </table> </td> </tr> </tbody> </table> </div> </div> </div>   </div> </div> </div> <div class="u-row-container" style="padding: 0px;background-color: transparent"> <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 640px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #f7dbbe;"> <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">   <div class="u-col u-col-100" style="max-width: 320px;min-width: 640px;display: table-cell;vertical-align: top;"> <div style="background-color: #ffffff;height: 100%;width: 100% !important;"> <div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"> <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left"> <div style="line-height: 150%; text-align: left; word-wrap: break-word;"> <p style="font-size: 14px; line-height: 150%; text-align: center;"><span style="color: #444444; font-size: 14px; line-height: 21px;"><strong><span style="font-size: 38px; line-height: 57px;">Welcome</span></strong></span></p> <p style="font-size: 14px; line-height: 150%; text-align: center;"><strong><span style="font-size: 38px; line-height: 57px;"><span style="color: #ec8c30; font-size: 38px; line-height: 57px;">"""+first_name+"""</span></span></strong></p> </div> </td> </tr> </tbody> </table> <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:10px 10px 15px;font-family:arial,helvetica,sans-serif;" align="left"> <div style="line-height: 150%; text-align: left; word-wrap: break-word;"> <p style="font-size: 14px; line-height: 150%; text-align: center;">Thanks for signing up with Online Savaari. We'll be sending an conformation email </p> <p style="font-size: 14px; line-height: 150%; text-align: center;">after verifying the documents.</p> </div> </td> </tr> </tbody> </table> </div> </div> </div>   </div> </div> </div> <div class="u-row-container" style="padding: 0px;background-color: transparent"> <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 640px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #ffffff;"> <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">   <div class="u-col u-col-100" style="max-width: 320px;min-width: 640px;display: table-cell;vertical-align: top;"> <div style="height: 100%;width: 100% !important;"> <div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"> <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px 30px;font-family:arial,helvetica,sans-serif;" align="left"> <div align="center"> <div style="display: table; max-width:83px;">   <table align="left" border="0" cellspacing="0" cellpadding="0" width="32" height="32" style="width: 32px !important;height: 32px !important;display: inline-block;border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;margin-right: 10px"> <tbody><tr style="vertical-align: top"><td align="left" valign="middle" style="word-break: break-word;border-collapse: collapse !important;vertical-align: top"> <a href="https://facebook.com/OnlineSavaari" title="Facebook" target="_blank"> <img src="https://cdn.tools.unlayer.com/social/icons/circle/facebook.png" alt="Facebook" title="Facebook" width="32" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: block !important;border: none;height: auto;float: none;max-width: 32px !important"> </a> </td></tr> </tbody></table>   <table align="left" border="0" cellspacing="0" cellpadding="0" width="32" height="32" style="width: 32px !important;height: 32px !important;display: inline-block;border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;margin-right: 0px"> <tbody><tr style="vertical-align: top"><td align="left" valign="middle" style="word-break: break-word;border-collapse: collapse !important;vertical-align: top"> <a href="https://twitter.com/OnlineSavaari" title="Twitter" target="_blank"> <img src="https://cdn.tools.unlayer.com/social/icons/circle/twitter.png" alt="Twitter" title="Twitter" width="32" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: block !important;border: none;height: auto;float: none;max-width: 32px !important"> </a> </td></tr> </tbody></table>   </div> </div> </td> </tr> </tbody> </table> </div> </div> </div>   </div> </div> </div> <div class="u-row-container" style="padding: 0px;background-color: transparent"> <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 640px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;"> <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">   <div class="u-col u-col-100" style="max-width: 320px;min-width: 640px;display: table-cell;vertical-align: top;"> <div style="height: 100%;width: 100% !important;"> <div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"> <table class="addressContent" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"> <tbody> <tr> <td style="overflow-wrap:break-word;word-break:break-word;padding:6px 10px 8px;font-family:arial,helvetica,sans-serif;" align="left"> <div style="line-height: 160%; text-align: left; word-wrap: break-word;"> <p style="text-align: center; font-size: 14px; line-height: 160%;"><span style="font-size: 12px; line-height: 19.200000000000003px;"><strong><span style="line-height: 19.200000000000003px; font-size: 12px;">Our mailing address is:</span></strong></span></p> <p style="text-align: center; font-size: 14px; line-height: 160%;"><span style="font-size: 12px; line-height: 19.200000000000003px;">support@onlinesavaari.com</span></p> </div> </td> </tr> </tbody> </table> </div> </div> </div>   </div> </div> </div>  </td> </tr> </tbody> </table>   </body> </html>"""
                                recepientsMailList = [email]
                                attachmentFpaths = ["flight/logo.png"]
                                sendEmail(smtpHost, smtpPort, mailUname, mailPwd, fromEmail,
                                          mailSubject, mailContentHtml, recepientsMailList, attachmentFpaths)

                                print("execution complete...")
                                succ_mgs = 'You Are Successfully Registered!'
                                # return Response({'status':'Success','msg':'Registration successful', 'user': user_serializer.data, 'customer':customer_serializer.data}, status=status.HTTP_200_OK ,template_name='online_savaari/index.html')
                                return render(request, "online_savaari/agency-signup.html",context={'succ_mgs': succ_mgs})
                            else:
                                error_mgs = 'Email ID already exists'
                                return render(request, "online_savaari/agency-signup.html",context={'error_mgs': error_mgs})
                        else:
                            error_mgs = 'please enter All fields'
                            return render(request, "online_savaari/agency-signup.html",context={'error_mgs': error_mgs})
            else:
                error_mgs = 'Passwords do not match!'
                return render(request, "online_savaari/agency-signup.html",context={'error_mgs': error_mgs})
        else:
            error_mgs = 'Email ID already exists'
            return render(request, "online_savaari/agency-signup.html",context={'error_mgs': error_mgs})  

    def put(self, request, pk=None):
        if not pk or not CorporateCust.objects.filter(id=pk).exists():
            return Response({"status": "Error", "reason": 'Please provide valid Corporate Customer ID!'}, status=status.HTTP_400_BAD_REQUEST)
        
        qs = CorporateCust.objects.get(id=pk)

        serializer = CorporateCustSerializer(qs, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'status':'Success','msg':'Corporate Customer Updated successfully!', 'data':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error", "reason": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def User_logout(request):

    request.user.auth_token.delete()

    logout(request)

    return Response('User Logged out successfully')

class WalletDetailsAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
            
        if WalletDetails.objects.filter(username_id = request.user.id).exists():
            wallet = WalletDetails.objects.filter(username_id =request.user.id)
            walletserializer = WalletSerializer(wallet,many=True)
            return Response(walletserializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'status':status.HTTP_200_OK, 'msg':"User don't have any transaction objects"})

    def post(self, request):
        wallet_serializer = WalletSerializer(data={
            'username':request.data.get('username'),
            'email':request.data.get('email'),
            'amount':request.data.get('amount'),
            'is_kyc_done':request.data.get('is_kyc_done'),
            'last_balance_added':request.data.get('last_balance_added'),
            'wallet_activated_on':request.data.get('wallet_activated_on'),
            'is_active':request.data.get('is_active'),
        })

        wallet_errors = wallet_serializer.is_valid()

        if wallet_errors:
            wallet_serializer.save()
            return Response({'status':'Success','msg':'Wallet created successfully', 'wallet':wallet_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error: Please Provide Valid Data", "errors":dict(**wallet_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk or not WalletDetails.objects.filter(id=pk).exists():
            return Response({"status": "Error", "reason": 'Please provide valid Data!'}, status=status.HTTP_400_BAD_REQUEST)
        
        qs = WalletDetails.objects.get(id=pk)

        serializer = WalletSerializer(qs, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'status':'Success','msg':'Wallet Updated successfully!', 'data':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error", "reason": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class TransactionAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        login_user = request.user
        if not login_user.is_authenticated:
            return JsonResponse({'status':status.HTTP_400_BAD_REQUEST, 'msg':"User is not logged In!"})
            
        else:
            if Transaction.objects.filter(username_id = request.user.id).exists():
                transaction = Transaction.objects.filter(username_id =request.user.id)
                transactionserializer = TransactionSerializer(transaction,many=True)
                return Response(transactionserializer.data, status=status.HTTP_200_OK)
            return JsonResponse({'status':status.HTTP_200_OK, 'msg':"User don't have any transaction objects"})

    def post(self, request):
        transaction_serializer = TransactionSerializer(data={
            'username':request.data.get('username'),
            'email':request.data.get('email'),
            'amount':request.data.get('amount'),
            'trasc_type':request.data.get('trasc_type'),
            'transaction_date':request.data.get('transaction_date'),
            'transaction_mode':request.data.get('transaction_mode'),
            'transaction_status':request.data.get('transaction_status'),
            'note':request.data.get('note'),
        })

        transaction_errors = transaction_serializer.is_valid()

        if transaction_errors:
            transaction_serializer.save()
            return Response({'status':'Success','msg':'Transaction Done successfully', 'wallet':transaction_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error: Please Provide Valid Data", "errors":dict(**transaction_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk or not Transaction.objects.filter(id=pk).exists():
            return Response({"status": "Error", "reason": 'Please provide valid Data!'}, status=status.HTTP_400_BAD_REQUEST)
        
        qs = Transaction.objects.get(id=pk)

        serializer = TransactionSerializer(qs, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'status':'Success','msg':'Transaction Status Changed', 'data':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error", "reason": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class RewardPointAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk=None):
        if pk and RewardPoints.objects.filter(id=pk).exists():
            qs = RewardPoints.objects.filter(id=pk)
        else:
            qs = RewardPoints.objects.all()
        serializer = RewardSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        reward_serializer = RewardSerializer(data={
            'username':request.data.get('username'),
            'reward_points':request.data.get('reward_points'),
            'reward_type':request.data.get('reward_type'),
            'operation_type':request.data.get('operation_type'),
            'note':request.data.get('note'),
            'credit_date' : datetime.now(),
            'expiry_date' : datetime.now() + timedelta(days = 30)
        })


        reward_errors = reward_serializer.is_valid()

        if reward_errors:
            reward_serializer.save()
            return Response({'status':'Success','msg':'Reward Points Added successfully', 'reward':reward_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error: Please Provide Valid Data", "errors":dict(**reward_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        reward =  RewardPoints.objects.get(pk=pk)

        # delete the todo
        reward.delete()

        return Response({
            'message': 'Reward Points Expired'
        })

class GetFlightPriceAPI(APIView):
    def get(self, request, Destination=None):
        with open("static/flight/FlightPrice.json", "r") as f:
            data = json.loads(f.read())
        print(data)
        return Response({"data":data})

class GetFlightBookAPI(APIView):
    def get(self, request, Destination=None):
        with open("static/flight/FlightBook.json", "r") as f:
            data = json.loads(f.read())
        print(data)
        return Response({"data":data})

class GetFlightInfoAPI(APIView):
    def get(self, request, Destination=None):
        with open("static/flight/FlightInformation.json", "r") as f:
            data = json.loads(f.read())
        print(data)
        return Response({"data":data})

class GetFlightDetailsAPI(APIView):
    def get(self, request, Destination=None):
        with open("static/flight/FlightDetails.json", "r") as f:
            data = json.loads(f.read())
        print(data)
        return Response({"data":data})

class GetFlightTTAPI(APIView):
    def get(self, request, Destination=None):
        with open("static/flight/FlightTT.json", "r") as f:
            data = json.loads(f.read())
        print(data)
        return Response({"data":data})

class GetFlightFareAPI(APIView):
    def get(self, request, Destination=None):
        with open("static/flight/FlightFare.json", "r") as f:
            data = json.loads(f.read())
        print(data)
        return Response({"data":data})


class RegisterHotelAPI(APIView):    
    authentication_classes = [] 
    permission_classes = []
    def get(self, request, pk=None):    
        if pk and HotelRegister.objects.filter(id=pk).exists(): 
            qs = HotelRegister.objects.filter(id=pk)    
        else:   
            qs = HotelRegister.objects.all()    
        serializer = HotelSerializer(qs, many=True) 
        return Response(serializer.data)    
    def post(self, request):    
        if request.data.get('password', None) != request.data.get('confirm_password', None):    
            return Response({"status": "Error", "errors":"Passwords do not match!"}, status=status.HTTP_400_BAD_REQUEST)    
        user_serializer = UserSerializer(data={ 
            'username':request.data.get('email'),   
            'first_name':request.data.get('first_name'),    
            'last_name':request.data.get('last_name'),  
            'email':request.data.get('email'),  
            'password':request.data.get('password'),    
        })  
            
        hotel_serializer = HotelSerializer(data={   
            'hotelname':request.data.get('hotelname'),  
            'mobile':request.data.get('mobile'),    
            'email':request.data.get('email'),  
            'telephone':request.data.get('telephone'),  
            'address':request.data.get('address'),  
            'city':request.data.get('city'),    
            'pincode':request.data.get('pincode'),  
            'staffname':request.data.get('staffname'),  
            'staffdesignation':request.data.get('staffdesignation'),    
            'staffemail':request.data.get('staffemail'),    
        })  
        user_errors = user_serializer.is_valid()    
        hotel_errors = hotel_serializer.is_valid()  
        if user_errors and hotel_errors:    
            user_serializer.save()  
            user = User.objects.get(id=user_serializer.data.get('id'))  
            user.set_password(request.data.get('password')) 
            user.save() 
            hotel_serializer.save(user=user)    
            return Response({'status':'Success','msg':'Registration successful', 'user': user_serializer.data, 'hotel':hotel_serializer.data}, status=status.HTTP_200_OK)   
        else:   
            return Response({"status": "Error: Please Provide Valid Data", "errors":dict(user_serializer.errors, **hotel_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)   
    def put(self, request, pk=None):    
        if not pk or not HotelRegister.objects.filter(id=pk).exists():  
            return Response({"status": "Error", "reason": 'Please provide valid Hotel ID!'}, status=status.HTTP_400_BAD_REQUEST)    
            
        qs = HotelRegister.objects.get(id=pk)   
        serializer = HotelSerializer(qs, data=request.data, partial=True)   
        if serializer.is_valid():   
            serializer.save()   
            return Response({'status':'Success','msg':'Hotel Updated successfully!', 'data':serializer.data}, status=status.HTTP_200_OK)    
        else:   
            return Response({"status": "Error", "reason": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)        


#by biswajit paloi

class ProfileListApi(APIView):
    

    def get(self, request,*args, **kwargs):

        if CorporateCust.objects.filter(user_id =request.user.id).exists():
            response = {}
            corporat = CorporateCust.objects.get(user_id =request.user.id)
            corporatserializer = CorporateCustSerializer(corporat )
            response = corporatserializer.data
            return Response(response,status=status.HTTP_200_OK)

        if Agent.objects.filter(user_id =request.user.id).exists():
            response = {}
            agent = Agent.objects.get(user_id =request.user.id)
            agentserializer = AgentSerializer(agent)
            response = agentserializer.data
            return Response(response,status=status.HTTP_200_OK)

        if Customer.objects.filter(user_id =request.user.id).exists():
            response = {}
            customer = Customer.objects.get(user =request.user.id)
            Customerserializer = CustomerSerializer(customer)
            response = Customerserializer.data
            return Response(response,status=status.HTTP_200_OK)

        if User.objects.filter(id =request.user.id).exists():
            response = {}
            user = User.objects.filter(id =request.user.id)
            userserializer = UserSerializer(user,many=True)
            response = userserializer.data
            return Response(response,status=status.HTTP_200_OK)

        return Response({'error': 'For access the profile page you need to login first'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):

        if CorporateCust.objects.filter(user_id =request.user.id).exists():
            corporat = CorporateCust.objects.get(user_id =request.user.id)
            corporatserializer = CorporateCustSerializer(corporat, data=request.data )
            if corporatserializer.is_valid():
                corporatserializer.save()
                return Response(corporatserializer.data,status=status.HTTP_200_OK)
            return Response(corporatserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if Agent.objects.filter(user_id =request.user.id).exists():
            agent = Agent.objects.get(user_id =request.user.id)
            agentserializer = AgentSerializer(agent, data=request.data )
            if agentserializer.is_valid():
                agentserializer.save()
                return Response(agentserializer.data,status=status.HTTP_200_OK)
            return Response(agentserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if Customer.objects.filter(user_id =request.user.id).exists():
            customer = Customer.objects.get(user_id =request.user.id)
            customerserializer = CustomerSerializer(customer, data=request.data )
            if customerserializer.is_valid():
                customerserializer.save()
                return Response(customerserializer.data,status=status.HTTP_200_OK)
            return Response(customerserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            User.objects.filter(id =request.user.id).exists()
            user = User.objects.get(id =request.user.id)
            userserializer = UserSerializer(user, data=request.data )
            if userserializer.is_valid():
                userserializer.save()
                return Response(userserializer.data,status=status.HTTP_200_OK)
            return Response(userserializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class AllBookingHistoryAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,*args, **kwargs):
        login_user = request.user

        if not login_user.is_authenticated:
            return JsonResponse({'status':status.HTTP_400_BAD_REQUEST, 'msg':"User is not logged In!"})
            
        else:
            if Passenger.objects.filter(user_id = request.user.id).exists():
                passengers = Passenger.objects.filter(user_id =request.user.id)
                passengerserializer = PassengerSerializer(passengers,many=True)
                return Response(passengerserializer.data, status=status.HTTP_200_OK)
            return JsonResponse({'status':status.HTTP_200_OK, 'msg':"User don't have any passengers objects"})

class BookingHistoryAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "booking_id"

    def get(self, request,*args, **kwargs):
        if self.kwargs.get(self.lookup_url_kwarg) is not None:
            booking_id = self.kwargs.get(self.lookup_url_kwarg)
            print(booking_id)
            if Passenger.objects.filter(os_bookingId = booking_id).exists():
                passengers = Passenger.objects.filter(os_bookingId = booking_id)
                passengerserializer = PassengerSerializer(passengers,many=True)
                return Response(passengerserializer.data, status=status.HTTP_200_OK)
            return JsonResponse({'status':status.HTTP_200_OK, 'msg':"User don't have any passengers objects"})

class AllAirlinesAPI(APIView):
    def get(self, request):
        with open("static/flight/airlines.json", "r") as f:
            airlines_json = json.load(f)
        return Response(airlines_json)

class AllAirportsAPI(APIView):
    def get(self, request):
        with open("static/flight/airport_list.json", "r") as f:
            airlines_json = json.load(f)
        return Response(airlines_json)

class AllBannersAPI(APIView):

    def get(self, request, *args, **kwargs):
        banner = Banner.objects.latest('id')
        banner1 = SmallBanner1.objects.latest('id')
        banner2 = SmallBanner2.objects.latest('id')
        bannerserializer = BannerSerializer(banner).data
        smallbanner1Serializer = SmallBanner1Serializer(banner1).data
        smallbanner2Serializer = SmallBanner2Serializer(banner2).data
        data = {'big_banner':bannerserializer,'small_banner1':smallbanner1Serializer,'small_banner2':smallbanner2Serializer}
        return Response(data, status=status.HTTP_200_OK)

class AllPromocodeAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request ,*args, **kwargs):
        promocode = Promocode.objects.all()
        promocodeserializer = PromocodeSerializer(promocode,many = True)
        return Response(promocodeserializer.data, status=status.HTTP_200_OK)