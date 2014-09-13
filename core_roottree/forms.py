from django import forms
from django.contrib.auth.models import User

class UserSignUpForm(forms.ModelForm):
	class Meta:
		model = User