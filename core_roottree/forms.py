from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from core_roottree.models import *

class ClientUserSignUpForm(UserCreationForm):
    username = forms.CharField(required=False)
    password2 = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ['username','email', 'password1']
    
    def clean(self):
        cleaned_data = super(ClientUserSignUpForm, self).clean()        
        cleaned_data['username'] = cleaned_data['email']
        return cleaned_data
        
    def save(self, commit=True):
        ret = super(UserSignUpForm, self).save(commit=commit)
        u = self.instance
        ClientUser.objects.create(user=u)
        return ret

class DevSignUpForm(UserCreationForm):
    username = forms.CharField(required=False)
    password2 = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ['username','email', 'password1']
    
    def __init__(self, *args, **kwargs):
        super(DevSignUpForm, self).__init__(*args, **kwargs)
        self.fields['company'] = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super(DevSignUpForm, self).clean()
        cleaned_data['username'] = cleaned_data['email']
        return cleaned_data

    def save(self, commit=True):
        ret = super(DevSignUpForm, self).save(commit=commit)
        u = self.instance
        Developer.objects.create(user=u, company=self.data['company'])
        return ret
