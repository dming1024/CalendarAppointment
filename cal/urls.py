from django.urls import path,include
from . import views

app_name = 'cal'
urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),
    path('index/', views.index, name='index'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.event, name='event_new'),
	path('event/edit/(?P<event_id>\d+)/', views.eventView, name='event_edit'),
    path('event/edit/new/', views.eventDelete, name='event_delete'),
    
    path("login/", views.login_request, name="login"),
    path("register/", views.register_request, name="register"),
    path("logout/", views.logout_request, name= "logout"),
    path("setPasswd/", views.setPasswd, name= "setPasswd"),
    path("updatePasswd/", views.updatePasswd, name= "updatePasswd")
#    path('test/', views.test, name='test'),
]
