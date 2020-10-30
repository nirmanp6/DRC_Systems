from django import forms

class form1(forms.Form):
	email = forms.EmailField(max_length=255)
	password = forms.CharField(max_length=50)