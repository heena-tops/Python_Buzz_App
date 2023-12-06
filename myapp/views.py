from django.shortcuts import render,redirect
from .models import User,Services,Techno,Package,Blog,Blog_comment,Work,Cart,Transaction
from django.conf import settings
from django.core.mail import send_mail
import random
from .forms import MyForm
import razorpay
import requests
from django.http import JsonResponse

# Create your views here.

def validate(request):
	email=request.GET.get('email')
	print(">>>>>>>>>>>>>>>>AJAX DATA : ",email)
	data={'is_taken':User.objects.filter(email__iexact=email).exists()}

	return JsonResponse(data)

def index(request):
	blogs=Blog.objects.all()
	techno=Techno.objects.all()
	work=Work.objects.all()

	return render(request,'index.html',{'blogs':blogs,'techno':techno,'works':work})

def work(request):
	print(">>>>>>>>>>>>>>work url call")
	techno=Techno.objects.all()
	work=Work.objects.all()
	return render(request,'work.html',{'works':work,'techno':techno})

def filter(request,pk):
	print(">>>>>>>>>>>>>>filter url call")
	techno=Techno.objects.all()
	technox=Techno.objects.get(pk=pk)
	work=Work.objects.filter(techno=technox)
	return render(request,'work.html',{'works':work,'techno':techno})

def filter_index(request,pk):
	print(">>>>>>>>>>>>>>filter url call")
	blogs=Blog.objects.all()
	techno=Techno.objects.all()
	technox=Techno.objects.get(pk=pk)
	work=Work.objects.filter(techno=technox)
	return render(request,'index.html',{'works':work,'techno':techno,'blogs':blogs})

def show(request,pk):
	work=Work.objects.get(pk=pk)
	return render(request,'show.html',{'work':work})

def signup(request):
	if request.method=="POST":

		try:
			user=User.objects.get(email=request.POST['uemail'])
			msg="User Already Exist !!!"
			return render(request,'signup.html',{'msg':msg})

		except:
			user=User.objects.create(
				name=request.POST['uname'],
				user_type=request.POST['user_type'],
				email=request.POST['uemail'],
				pswd=request.POST['upswd'],
				contact=request.POST['ucontact'],
				address=request.POST['uaddress'],
				)

			url = "https://www.fast2sms.com/dev/bulkV2"
			otp=random.randint(1111,9999)
			querystring = {"authorization":"NVRk2utaImAEYPfci1W6KGZO9QXhel5vUjn7wDLd0s8xro3pBCZ1A2yptsi0uxNFqQVlXKmPEYJLhS5D","variables_values":str(otp),"route":"otp","numbers":user.contact}

			headers = {
			    'cache-control': "no-cache"
				}

			response = requests.request("GET", url, headers=headers, params=querystring)
			print(response.text)


			return render(request,'signup.html')

	else:
		return render(request,'signup.html')

def signin(request):
	if request.method=="POST":
		user=User.objects.get(email=request.POST['uemail'],pswd=request.POST['upswd'])
		print(">>>>>>>>>>>>>>>>>>>User Object : ",user)
		request.session['email']=user.email
		request.session['name']=user.name
		if user.user_type=="service_provider":
			request.session['dashborad']=True
			return redirect('index')
		else:
			request.session['customer']=True
			return redirect('index')

	else:
		return render(request,'signin.html')

def signout(request):
	del request.session['email']
	del request.session['name']
	
	try:
		del request.session['dashborad']
	except:
		pass

	try:
		del request.session['customer']
	except:
		pass

	return redirect('signin')

def fpswd(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['uemail'])
			subject = 'OTP for Forgot Password'
			otp=random.randint(1000,9999)
			message = f'Hi {user.name}, Your OTP is : '+str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )
			return render(request,'verify_otp.html',{'email':user.email,'otp':str(otp)})

		except:
			msg="Not a Registered User !!!"
			return render(request,'signup.html')

	else:
		return render(request,'fpswd.html')

def verify_otp(request):
	if request.method=="POST":
		email=request.POST['email']
		otp=request.POST['otp']
		uotp=request.POST['uotp']

		if otp==uotp:
			return render(request,'change_pswd.html',{'email':email})
		else:
			msg="Invalid OTP!!!!"
			return render(request,'change_pswd.html',{'msg':msg})

	else:
		return render('verify_otp.html')

def change_pswd(request):
	if request.method=="POST":
		email=request.POST['email']
		np=request.POST['npswd']
		cnp=request.POST['cnpswd']

		if np==cnp:
			user=User.objects.get(email=email)
			user.pswd=np
			user.save()
			return redirect('signin')
		else:
			msg="New password and Confirm new Password Doesn't Matched !!"
			return render(request,'change_pswd.html',{'msg':msg})

	else:
		return render(request,'change_pswd.html')


#======================ADMIN DASHBOARD START=============================

def admin_dashboard(request):
	user=User.objects.get(email=request.session['email'])
	return render(request,'admin_dashboard.html',{'user':user})

def admin_charts(request):
	return render(request,'admin_charts.html')

def add_services(request):
	if request.method=="POST":
		Services.objects.create(
			service_type=request.POST['service_type']
			)
		return render(request,'add_services.html')
		
	else:
		return render(request,'add_services.html')

def add_techno(request):
	service=Services.objects.all()
	print(">>>>>>>>>>>>>>>>>>>>>>>>All Services : ",service)

	if request.method=="POST":
		single_service=Services.objects.get(service_type=request.POST['service_type'])
		# need to fetch object as of to assign foreign key

		Techno.objects.create(
			service_type=single_service, 
			techno_area=request.POST['techno_type']
			)
		return render(request,'add_techno.html',{'service':service})
	else:
		return render(request,'add_techno.html',{'service':service})

def add_package(request):
	techno=Techno.objects.all()
	user=User.objects.get(email=request.session['email'])
	print(">>>>>>>>>>>>>>>>>>>>All techno : ",techno)
	if request.method=="POST":
		single_techno=Techno.objects.get(techno_area=request.POST['techno_type'])

		Package.objects.create(
			user=user,
			techno=single_techno,
			pname=request.POST['pname'],
			price=request.POST['price'],
			image=request.FILES['image'],
			desc=request.POST['desc'],
			)

		return render(request,'add_package.html',{'techno':techno})
	else:
		return render(request,'add_package.html',{'techno':techno})


def my_packages(request):
	packages=Package.objects.all()
	return render(request,'my_packages.html',{'packages':packages})


def modify_package(request):
	packages=Package.objects.all()
	return render(request,'modify_package.html',{'packages':packages})


def delete_package(request,pk):
	package=Package.objects.get(pk=pk)
	print(">>>>>>>>>>>>>package to be delete : ",package)
	package.delete()
	return redirect('modify_package')

def update_package(request,pk):
	techno=Techno.objects.all()
	package=Package.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	print(">>>>>>>>>>>>>package to be update : ",package)
	if request.method=="POST":

		single_techno=Techno.objects.get(techno_area=request.POST['techno_type'])

		package.user=user
		package.techno=single_techno
		package.pname=request.POST['pname']
		package.price=request.POST['price']
		package.image=request.FILES['image']
		package.desc=request.POST['desc']
		package.save()
		return redirect('modify_package')
	else:
		return render(request,'update_package.html',{'techno':techno,'package':package})

def search(request):
	if request.method=="POST":
		item=request.POST['search_item']
		try:
			techno=Techno.objects.get(techno_area=item.capitalize())
			package=Package.objects.filter(techno=techno)
			return render(request,'search_item.html',{'package':package,'techno':techno})
		except:
			msg="No Product Found !!!!!!!"
			return render(request,'search_item.html',{'msg':msg})
	else:
		pass
#=============All Techno==========================================================
def all_techno(request):
	techno=Techno.objects.all()
	return render(request,'all_techno.html',{'techno':techno})

def delete_techno(request,pk):
	spec_techno=Techno.objects.get(pk=pk)
	spec_techno.delete()
	return redirect('all_techno')

def update_techno(request,pk):
	service=Services.objects.all()
	techno=Techno.objects.get(pk=pk)
	if request.method=="POST":
		spec_service=Services.objects.get(service_type=request.POST['service_type'])
		techno.service_type=spec_service
		techno.techno_area=request.POST['techno_area']
		techno.save()
		return redirect('all_techno')
	else:
		return render(request,'update_techno.html',{'service':service,'techno':techno})
	

#==========================Blogs================================

def blogs(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		Blog.objects.create(
			user=user,
			title=request.POST['title'],
			image=request.FILES['image'],
			desc=request.POST['desc']
			)
		return render(request,'blogs.html')

	else:
		return render(request,'blogs.html')

def single_blog(request,pk):
	blog=Blog.objects.get(pk=pk)
	comment=Blog_comment.objects.filter(blog=blog)
	all_blogs=Blog.objects.all()
	return render(request,'single_blog.html',{'blog':blog,'comments':comment,'all_blogs':all_blogs})

def my_blogs(request):
	user=User.objects.get(email=request.session['email'])
	blogs=Blog.objects.filter(user=user)
	return render(request,'my_blogs.html',{'blogs':blogs})

#comment on blog

def post_comment(request,pk):
	blog=Blog.objects.get(pk=pk)
	all_blogs=Blog.objects.all()
	all_comments=Blog_comment.objects.filter(blog=blog)
	count=0
	for i in all_comments:
		count+=1

	if request.method=="POST":
		comment=Blog_comment.objects.create(
			blog=blog,
			comment=request.POST['comment'],
			name=request.POST['name'],
			email=request.POST['email'],
			)
		comment=Blog_comment.objects.filter(blog=blog)
		# work remaining : comment_count
		return render(request,'single_blog.html',{'blog':blog,'comments':comment,'all_blogs':all_blogs})

	else:
		return render(request,'single_blog.html',{'blog':blog,'all_blogs':all_blogs})


#=====================================Wrok Space==========================================


def work_space(request):
	form = MyForm()
	techno=Techno.objects.all()
	if request.method=='POST':
		technox=Techno.objects.get(techno_area=request.POST['techno_area'])
		work=Work.objects.create(
		techno=technox,
		title=request.POST['title'],
		price=request.POST['price'],
		desc=request.POST['content'],
		front_img=request.FILES['image'],
		file=request.FILES['demo_website'],
		)
		return render(request,'work_space.html', {'form': form,'techno':techno})

	else:
		return render(request,'work_space.html', {'form': form,'techno':techno})

#====================ADMIN DASHBOARD END====================================================
#==============================================================================


#==============================CART START=============================================

def add_to_cart(request,pk):
	package=Package.objects.get(pk=pk)
	cart=Cart.objects.create(
		customer=User.objects.get(email=request.session['email']),
		package=package,
		)
	return redirect('cart')

def cart(request):
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.filter(customer=user)
	net_price=0
	for i in cart:
		net_price+=i.package.price

	try:
		client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
		payment = client.order.create({ "amount": net_price*100, "currency": "INR", "receipt": "order_rcptid_11" })

		global pay_id
		pay_id=payment['id']

		trans=Transaction.objects.create(
			customer=user,
			amount=net_price,
			razorpay_order_id=payment['id']
		
			)

		request.session['amount']=net_price

		return render(request,'cart.html',{'cart':cart,'user':user,'net_price':net_price,'trans':trans,'payment':payment})
	except:
		return render(request,'cart.html',{'user':user,'net_price':net_price})


def remove_from_cart(request,pk):
	customer=User.objects.get(email=request.session['email'])
	cart=Cart.objects.get(pk=pk)
	cart.delete()
	return redirect('cart')


def callback(request):
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.filter(customer=user)
	trans=Transaction.objects.get(razorpay_order_id=pay_id)
	for i in cart:
		i.payment_status=True
		i.save()
		i.delete()
	del request.session['amount']
	return render(request,'callback.html',{'trans':trans,'cart':cart,'user':user})

#==============================CART END===============================================



# ORM Query : Object Relational Mapping

# .create() : to enter data into data table
# Syntax : model_name.objects.create(col=val,...,coln=valn)

# .get() : to fetch data from data table : It returns a single data object
# Syntax : model_name.objects.get(condition)

# .all() : to fetch all data from table without any condition : It returns list of objects (ie. : QuerySet)
# Syntax : model_name.objects.all()

# .filter() : to fetch one or more data based on conidtion
# Syntax : model_name.objects.filter(condition)