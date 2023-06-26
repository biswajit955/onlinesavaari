from django import forms
from django.contrib.auth.models import Group

class UserGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'