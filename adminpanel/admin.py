from django.contrib import admin

from .models import *
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django import forms

from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy  as _
from django.contrib.admin.widgets import FilteredSelectMultiple    
from django.contrib.auth.models import Group



admin.site.register(Card)
admin.site.register(Pcc)


admin.site.register(Commission)
@admin.register(Markup)
class MarkupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'user_type',
        'amount_type',
        'amount',
        'airline_type',
        'markup_type',
    )
    list_filter = ('user',)


@admin.register(SeriesMarkup)
class SeriesMarkupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'amount_type',
        'amount',
        'airport_name',
        'start_date',
        'end_date',
    )
    list_filter = ('user', 'start_date', 'end_date')


@admin.register(RescheduleFlight)
class RescheduleFlightAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'Reschedule_bookingid',
        'Reschedule_flight_date',
        'Reschedule_query',
        'Reschedule_status',
    )
    list_filter = ('user',)


@admin.register(RefundFlight)
class RefundFlightAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'Refund_bookingid',
        'Refund_flight_date',
        'Refund_query',
        'Refund_status',
    )
    list_filter = ('user',)


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'promo_code',
        'amount',
        'description',
        'start_date',
        'end_date',
    )
    list_filter = ('user', 'start_date', 'end_date')


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'big_banner')
    list_filter = ('user',)


@admin.register(SmallBanner1)
class SmallBanner1Admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'small_banner1')
    list_filter = ('user',)


@admin.register(SmallBanner2)
class SmallBanner2Admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'small_banner2')
    list_filter = ('user',)


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'email',
        'mobile',
        'designation',
        'first_name',
        'last_name',
        'user_status',
    )
    list_filter = ('user',)


@admin.register(APIbalance)
class APIbalanceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'company_name',
        'balance',
        'email',
        'mobile',
    )
    list_filter = ('user',)


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'email_or_phone',
        'deposit_type',
        'amount',
        'bank_name',
        'deposite_branch',
        'trasaction_num',
        'dep_status',
        'deposit_slip',
    )
    list_filter = ('user',)


@admin.register(AgentCredit)
class AgentCreditAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'agent',
        'agent_excepting_airlines',
        'amount',
        'start_date',
        'end_date',
        'hours',
    )
    list_filter = ('agent', 'start_date', 'end_date')

admin.site.register(Permission)



class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
         queryset=User.objects.all(), 
         required=False,
         # Use the pretty 'filter_horizontal widget'.
         widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance


class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']

admin.site.unregister(Group)

admin.site.register(Group, GroupAdmin)