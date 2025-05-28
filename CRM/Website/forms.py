from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class SignUpForm(UserCreationForm):
    email=forms.EmailField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}))
    first_name=forms.CharField(label="",max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'first name'}))
    last_name=forms.CharField(label="",max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'last name'}))


    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']


    def __init__(self, *args, **kwargs):
            super(SignUpForm, self).__init__(*args, **kwargs)

            self.fields['username'].widget.attrs['class'] = 'form-control'
            self.fields['username'].widget.attrs['placeholder'] = 'User Name'
            self.fields['username'].label = ''
            self.fields['username'].help_text = ''

            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password1'].widget.attrs['placeholder'] = 'Password'
            self.fields['password1'].label = ''
            self.fields['password1'].help_text = '' 

            self.fields['password2'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
            self.fields['password2'].label = ''
            self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'    



class Addrecords(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"First Name", "class":"form-control"}), label="")
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Last Name", "class":"form-control"}), label="")
    email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control"}), label="")
    phone = forms.IntegerField(required=True,widget=forms.widgets.TextInput(attrs={"placeholder":"Phone", "class":"form-control"}), label="")
    address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Address", "class":"form-control"}), label="")
    city = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"City", "class":"form-control"}), label="")
    state = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"State", "class":"form-control"}), label="")
    Pincode = forms.IntegerField(required=True,widget=forms.widgets.TextInput(attrs={"placeholder":"Pincode", "class":"form-control"}), label="")
    Profile = forms.ImageField(required=True,widget=forms.widgets.FileInput(attrs={"class":"form-control","accept": "image/*"}),label="Profile Picture"
    )
    
    
    
    
    class Meta:
        model= Record
        exclude = ('user',)