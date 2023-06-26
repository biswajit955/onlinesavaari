from django.shortcuts import render,redirect
from .models import WalletDetails,Transaction,KYCDetails,RewardPoints
thisset = {'1','2'}
  


def ecash(request):
    login_user_wallet = WalletDetails.objects.filter(username_id=request.user.id)
    login_user_transaction = Transaction.objects.filter(username_id=request.user.id).last()
    print("-1")
    if login_user_transaction:
        print("0")
        if login_user_transaction.transaction_mode == 'Wallet':
            if login_user_transaction.transaction_status == 'Success':
                print("1")
                print(thisset)
                if login_user_transaction.transaction_id not in thisset:
                    print(thisset)
                    print("2")
                    thisset.add(login_user_transaction.transaction_id)
                    print(thisset)
                    obj = WalletDetails(username_id=request.user.id,
                                        email_id=request.user.id,
                                        current_amount=login_user_transaction.amount)
                    obj.save()
                    login_user_wallets = WalletDetails.objects.filter(username_id=request.user.id).all()
                    print("3")
                    ammount = 0
                    for i in login_user_wallets:
                        print(i.current_amount)
                        ammount += i.current_amount
                    login_user_transactions = Transaction.objects.filter(username_id=request.user.id)
                    return render(request, "online_savaari/ecash.html", context={
                                                        'ammount':ammount,
                                                        'wallet': login_user_wallets,
                                                        'transaction':login_user_transactions,
                                                        })
                login_user_wallets = WalletDetails.objects.filter(username_id=request.user.id)
                login_user_transactions = Transaction.objects.filter(username_id=request.user.id)
                ammount = 0
                for i in login_user_wallets:
                    print(i.current_amount)
                    ammount += i.current_amount
                return render(request, "online_savaari/ecash.html", context={
                                                        # 'wallet': login_user_wallets,
                                                        'transaction':login_user_transactions,
                                                        'ammount':ammount,
                                                        })
    ammount = 0
    padding = 0
    for i in login_user_wallet:
        ammount += i.current_amount
        padding += i.pending_ammount
    return render(request, "online_savaari/ecash.html",context={
                                                        'ammount':ammount,
                                                        'wallet': login_user_wallet,
                                                        'transaction':login_user_transaction,} )


