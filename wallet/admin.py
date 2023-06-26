from django.contrib import admin
from .models import *
from import_export.admin import ImportExportMixin

# Register your models here.

class walletAdmin(ImportExportMixin,admin.ModelAdmin):
    search_fields = ['email', 'amount','transaction_date','trasc_type' ]
    list_display = ['email', 'amount', 'trasc_type', 'tds']
admin.site.register(WalletDetails,walletAdmin)
admin.site.register(Transaction)
admin.site.register(KYCDetails)
admin.site.register(RewardPoints)

