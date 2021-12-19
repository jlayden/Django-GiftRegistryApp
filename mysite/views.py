import re
from django.shortcuts import render
from django.views import View
from mysite import models
from .models import MyUser
from .models import Gift

# This is the login page. Users are presented with input elements for user name and password. Also displayed is a message suggesting users register on the Registration page if they have not yet done so.
class Home(View):
  def get(self, request):
    n = request.session.get('name','')
    if n:
      u = models.MyUser.objects.get(name=n)
      request.session["name"]=u.name
    else:
      request.session["name"]=''
    request.session.set_expiry(300)
    return render(request, 'main/home.html')
  def post(self, request):
    n = request.POST.get("name","")
    if models.MyUser.objects.filter(name=n).exists():
      errmsg = ''
      msg = 'Successful login!'
      u = models.MyUser.objects.get(name=n)
      request.session["name"]=u.name
    else:
      msg = ''
      errmsg = 'User does not exist. Please register'    
    request.session.set_expiry(300)
    return render(request, 'main/home.html',{"msg":msg,"errmsg":errmsg})


# Users provide an email address, user name, and password to create an account. The email address must be of the correct format, and the user name cannot already exist. On successful creation a page displaying only a "success!" message is returned. On failure, the same registration page is displayed with the same data the user entered originally, but with error messages describing the problem.
class Registration(View):
  def get(self, request):
    n = request.session.get('name','')
    if n:
      u = models.MyUser.objects.get(name=n)
      p = u.password
    else:
      p = ''
    request.session.set_expiry(300)
    return render(request, 'main/registration.html',{"password":p,"name":n})
  def post(self, request):
    msg=''
    umsg=''
    emsg=''
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if models.MyUser.objects.filter(name=request.POST['name']).exists():
      umsg = 'Username not available!'
      email = request.POST['email']
      name = request.POST['name']
    if(not re.fullmatch(regex, request.POST['email'])):
      emsg = 'Email is not valid!'
      email = request.POST['email']
      name = request.POST['name']
    if (not umsg) and (not emsg):
      email = request.POST['email']
      name = request.POST['name']
      password = request.POST['password']
      u = MyUser(email=email,name=name,password=password)
      u.save()
      msg = 'Successful registration!'
    request.session.set_expiry(300)
    return render(request, 'main/registration.html',{'msg':msg,'emsg':emsg,'umsg':umsg,'name':name,'email':email})


# If a valid user is logged in this page displays a link to each user's gift list (see Other Users' Gifts below). If no user is logged in a message saying log in is required, and suggesting registration is displayed.
class Users(View):
  def get(self, request):
    n = request.session.get('name','')
    if n:
      users = MyUser.objects.all()
      msg=''
    else:
      users=''
      msg = 'Login required'
    request.session.set_expiry(300)
    return render(request, 'main/users.html',{"users":users, 'msg':msg})

# If a valid user is logged in, that user's current list of gifts is displayed, and an input element allows them to add a new gift. If no user is logged in a message saying log in is required, and suggesting registration is displayed.
class Gifts(View):
  def get(self, request):
    n = request.session.get('name','')
    # print('session name is '+n)
    if n:
      u = models.MyUser.objects.get(name=n)
      gifts = Gift.objects.filter(owner=u)
      msg=''
    else:
      gifts=''
      msg = 'Login required'
    request.session.set_expiry(300)
    return render(request, 'main/gifts.html',{"gifts":gifts, "msg":msg})
  def post(self, request):
    n = request.session.get('name','')
    if models.MyUser.objects.filter(name=n).exists():
      u = models.MyUser.objects.get(name=n)
      gifts = Gift.objects.filter(owner=u)
      # add new gift
      owner = u
      name = request.POST['name']
      newGift = Gift(owner=owner, name=name)
      newGift.save()
      msg = ''
      request.session["name"]=u.name
    else:
      gifts=''
      msg = 'Error message'
    # request.session["name"]=u.name
    request.session.set_expiry(300)
    return render(request, 'main/gifts.html',{"gifts":gifts, "msg":msg})

# There is no entry in the menu for this, but from the Users page one can reach a page to view (but not add to) the gift list of any other user. If no user is logged in a message saying log in is required, and suggesting registration is displayed.
class OtherGifts(View):
  def get(self, request):
    n = request.session.get('name','')
    if n:
      user = models.MyUser.objects.get(name=request.GET.get('name'))
      gifts = Gift.objects.filter(owner=user)
      msg=''
    else:
      gifts=''
      msg = 'Login required'
    request.session.set_expiry(300)
    return render(request, 'main/other.html',{"gifts":gifts,'msg':msg})