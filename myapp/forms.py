from django import forms
from django.contrib.auth.models import User

from . import models


class BuildsForm(forms.ModelForm):
    class Meta:
        model = models.Builds
        fields = '__all__'


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
