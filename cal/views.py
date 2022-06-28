from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar

from .models import *
from .utils import Calendar
from .forms import EventForm
#from .forms import ExampleForm

def index(request):
    return HttpResponse('hello')

class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)#将这个返回值，布局到ui界面
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['footer'] = mark_safe("<a href='#'>首页</a>")
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
    
        
def event(request, event_id=None):
    if request.user.is_authenticated:
        instance = Event()
        if event_id:
            instance = get_object_or_404(Event, pk=event_id)
        else:
            instance = Event(Users=request.user.username,
            start_time=datetime.now(),end_time=datetime.now())

        form = EventForm(request.POST or None, instance=instance)
        #request.user.username
        #form.instance.Users=request.user.username
        if request.POST and form.is_valid():
            if infer_time(form):
                form.save()
                return HttpResponseRedirect(reverse('cal:calendar'))
            else:
                contents="已被占用，请重新选择时间段进行预约"
                #return HttpResponseRedirect(reverse('cal:index'))#无法预约成功
                return render(request, 'cal/occupied.html', {'contents': contents})
        return render(request, 'cal/event.html', {'form': form})
    else:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("cal:calendar")
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        form = AuthenticationForm()
        return render(request=request, template_name="cal/login.html", context={"login_form": form})

#获取当天已有的预约时间
def booked(day):
    all_users = Event.objects.all()
    befor_day=day-timedelta(days=1)
    after_day=day+timedelta(days=1)
#    select_user=all_users.filter(start_time > after_day).filter(start_time < befor_day)
    select_user=all_users.filter(start_time__lte=after_day.strftime("%Y-%m-%d")).filter(start_time__gte=befor_day.strftime("%Y-%m-%d"))
    #返回一系列时间值
    time_intervel=[[m.start_time,m.end_time]  for  m in select_user]
    return(time_intervel)


def infer_time(form):
    day_start=form.instance.start_time
    day_end=form.instance.end_time
    
    correct_date=day_start < day_end
    #先判断start
    time_intervel=booked(day_start)
    rs=[]
    for x,y in time_intervel:
        if x <= day_start <= y:
            rs.append(False)
        else:        
            if x <= day_end <= y:
                rs.append(False)
            else:
            #起始和终止均不再两者之间
                rs.append(True)
    if all(rs) and correct_date:
        return True
    else:
        return False



import pytz
def eventView(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    form = EventForm(None, instance=instance)
    username=form.instance.Users
    
    utc=pytz.UTC
    ctime = utc.localize(datetime.now()) 
    avaliable=ctime.replace(tzinfo=utc) < form.instance.start_time
    
    return render(request, 'cal/eventView.html', {'form': form,"username":username,"avaliable":avaliable})
 

def eventDelete(request):
    query = request.GET.get('Users')
    start_time = request.GET.get('start_time')
    #form= EventForm(request.GET)
    #x=form.instance.id
    print(Event.objects.all().filter(Users=query).filter(start_time=start_time))
    Event.objects.all().filter(Users=query).filter(start_time=start_time).delete()
    return HttpResponseRedirect(reverse('cal:event_new'))


''' 
def test(request, event_id=None):
    instance = ExampleForm()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = ExampleForm()

    form = ExampleForm()
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:test'))
    return render(request, 'cal/event.html', {'form': form})
'''
from django.shortcuts import  render, redirect
from .forms import NewUserForm#待定义forms,NewUserForm类
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.shortcuts import  render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from . import  models

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)#需要定义NewUserForm
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("cal:calendar")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="cal/register.html", context={"register_form":form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("cal:calendar")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="cal/login.html", context={"login_form":form})
 
from django.contrib.auth import login, authenticate, logout #add this
def logout_request(request):
    logout(request)
    message="You have successfully logged out ~"
    return render(request=request, template_name="cal/logout.html", context={"message":message})


#https://ordinarycoders.com/blog/article/django-password-reset 

#登录之后才能修改密码
def setPasswd(request):
    if request.user.is_authenticated:
        return render(request, 'cal/changepwd.html')
    else:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("cal:setPasswd")
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        form = AuthenticationForm()
        return render(request=request, template_name="cal/login.html", context={"login_form": form})
   
#获取用户修改后的密码，并进行数据库更新
from django.contrib.auth.models import User
#https://stackoverflow.com/questions/35308015/how-to-update-django-auth-user-with-queryset
def updatePasswd(request):
    if request.user.is_authenticated:
        passwd = request.GET.get('Newpassword')
        username=request.user.username
        UsermodelUpdate=User.objects.get(username=username)
        UsermodelUpdate.set_password(passwd)
        UsermodelUpdate.save()
#        print(username+""+passwd)
        message="Your password has been reseted!"
        logout(request)
        return render(request=request, template_name="cal/logout.html", context={"message":message})
        



