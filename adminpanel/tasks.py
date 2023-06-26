# from celery import task 
from celery import shared_task 
from random import randint
from django_celery_beat.models import PeriodicTask,ClockedSchedule
from django.contrib.auth.models import User
from wallet.models import *
from .models import *
# We can have either registered task 
@shared_task(name='summary') 
def send_import_summary(*args, **kwargs):
	print("‘Here Im every hr’")
	
	# Magic happens here ... 
# or 
@shared_task 
def start_debit(*args, **kwargs):
	user_id = args[0]
	amount = args[1]
	task_name = args[2]
	emailId = User.objects.get(id=user_id)
	transaction_number = randint(1000000000, 9999999999)
	osn_id = str(transaction_number)
	transaction_number = 'DEBIT'+osn_id
	if not WalletDetails.objects.filter(email=emailId):
		wallet_activated_on = date.today()
		if(emailId != None):
			wall_user = User.objects.get(email=emailId)
			curl = WalletDetails.objects.create(username=wall_user,email=emailId,wallet_activated_on=wallet_activated_on,wallet_balance=0)
	if(emailId != None):
		wallet_detail = (WalletDetails.objects.filter(email=emailId).values()).latest('id')
		wall_user = User.objects.get(id=wallet_detail['username_id'])
		wallet_bal = wallet_detail['wallet_balance']
		new_bal = float(wallet_bal)- float(amount)
		curl = WalletDetails.objects.create(username=wall_user,email=emailId,wallet_balance=new_bal,amount=amount,trasc_type="Debit",transaction_mode="CREDITMODEL",transaction_status="Success",transaction_id=transaction_number,note="debited against  CREDIT given by admin")
	task = ClockedSchedule.objects.filter(clocked_time=task_name)
	task.delete()
	return True

@shared_task 
def start_credit(*args, **kwargs):
	user_obj = args[0]
	amount = args[1]
	task_name = args[2]
	transaction_number = randint(1000000000, 9999999999)
	osn_id = str(transaction_number)
	transaction_number = 'CREDIT'+osn_id
	agent = Agent.objects.get(agent_id=user_obj)
	if not WalletDetails.objects.filter(email=agent):
		wallet_activated_on = date.today()
		if(agent != None):
			wall_user = User.objects.get(email=agent)
			curl = WalletDetails.objects.create(username=wall_user,email=agent,wallet_activated_on=wallet_activated_on,wallet_balance=0)
	if(agent != None):
		wallet_detail = (WalletDetails.objects.filter(email=agent).values()).latest('id')
	wall_user = User.objects.get(id=wallet_detail['username_id'])
	wallet_bal = wallet_detail['wallet_balance']
	new_bal = float(wallet_bal)+ float(amount)
	curl = WalletDetails.objects.create(username=wall_user,email=agent,wallet_balance=new_bal,amount=amount,trasc_type="Credit",transaction_mode="CREDITMODEL",transaction_status="Success",transaction_id=transaction_number,note="added from admin panel for CREDIT MODEL")
	task = ClockedSchedule.objects.filter(clocked_time=task_name)
	task.delete()
	return True

