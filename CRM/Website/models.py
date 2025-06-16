from django.db import models
import os
from django.core.exceptions import ValidationError
from django.core import validators



def starts_with_capital_M(value):
	if not value.startswith("M"):
		raise ValidationError("Please define your Honorifics")

def get_upload_path(instance, filename):
	return os.path.join('profile_pics', str(instance.id), filename)
# Create your models here.



class Record(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=50,validators=[starts_with_capital_M])
	last_name =  models.CharField(max_length=50,null=True,blank=True)
	email =  models.EmailField(max_length=100)
	phone = models.CharField(max_length=15)
	address =  models.CharField(max_length=100)
	city =  models.CharField(max_length=50)
	state =  models.CharField(max_length=50)
	Pincode =  models.CharField(max_length=6)
	Profile = models.ImageField(upload_to=get_upload_path, null=True, blank=True)

	def __str__(self):
		return(f"{self.first_name} {self.last_name}")