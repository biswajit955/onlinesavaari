from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(WalletDetails)
admin.site.register(Transaction)
admin.site.register(KYCDetails)
admin.site.register(RewardPoints)

