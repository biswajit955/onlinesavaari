from django.contrib import admin

# Register your models here.
from .models import *
from import_export.admin import ImportExportMixin
class VideoAdminModel(admin.ModelAdmin):
    search_fields=('email',)
class DocAdmin(ImportExportMixin,admin.ModelAdmin):
    search_fields = ['username']
    list_display = ['username']



admin.site.register(Country)
admin.site.register(State)
admin.site.register(PinCodes)
admin.site.register(Documents,DocAdmin)

admin.site.register(Agent,VideoAdminModel)
admin.site.register(Customer)
admin.site.register(CorporateCust)