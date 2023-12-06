from django.db import models
from ckeditor.widgets import CKEditorWidget
from tinymce.models import HTMLField
from django.utils import timezone
from datetime import datetime
from datetime import date 

# Create your models here.

class User(models.Model):
	name=models.CharField(max_length=100)
	user_type=models.CharField(max_length=100,default="service_provider")
	email=models.EmailField()
	pswd=models.CharField(max_length=100)
	contact=models.CharField(max_length=100)
	address=models.TextField(max_length=100)

	def __str__(self):
		return self.name

class Services(models.Model):
	service_type=models.CharField(max_length=100)

	def __str__(self):
		return self.service_type


class Techno(models.Model):
	service_type=models.ForeignKey(Services,on_delete=models.CASCADE)
	techno_area=models.CharField(max_length=100)

	def __str__(self):
		return self.techno_area


class Package(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	techno=models.ForeignKey(Techno,on_delete=models.CASCADE)
	pname=models.CharField(max_length=100)
	price=models.IntegerField()
	image=models.ImageField(upload_to='images/')
	desc=models.CharField(max_length=500)

	def __str__(self):
		return self.pname+" - "+self.techno.techno_area

class Blog(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	title=models.CharField(max_length=100)
	image=models.ImageField(upload_to='blogs/')
	desc = HTMLField()

	def __str__(self):
		return self.title

class Blog_comment(models.Model):
	blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
	comment=HTMLField()
	comment_count=models.ImageField(default=0)
	like_count=models.ImageField(default=0)
	name=models.CharField(max_length=100)
	dop=models.DateField(default=date.today)
	email=models.EmailField()

	def __str__(self):
		return self.blog.title+" by "+self.name

class Work(models.Model):
	techno=models.ForeignKey(Techno,on_delete=models.CASCADE)
	title=models.CharField(max_length=100)
	price=models.IntegerField()
	desc=HTMLField()
	front_img=models.ImageField(upload_to='work_image/')
	file=models.FileField(upload_to='work_demo/')

	def __str__(self):
		return self.title+" - "+self.techno.techno_area


class Cart(models.Model):
	customer=models.ForeignKey(User,on_delete=models.CASCADE)
	package=models.ForeignKey(Package,on_delete=models.CASCADE)
	created_on=models.DateTimeField(default=timezone.now(),null=True)
	payment_status=models.BooleanField(default=False)
	

class Transaction(models.Model):
	customer=models.ForeignKey(User,on_delete=models.CASCADE)
	amount=models.IntegerField()
	razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)
	razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
	razorpay_payment_signature=models.CharField(max_length=100,null=True,blank=True)
	created_on=models.DateField(default=datetime.today(),null=True)