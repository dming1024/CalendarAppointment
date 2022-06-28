from django.db import models
from django.urls import reverse
from django import forms



class Event(models.Model):
    Users = models.CharField(max_length=100,null=True)#搞成一个下拉框，选择人名字
    description = models.CharField(max_length=100)#
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.Users} </a>'+"\n"+str(self.start_time.strftime("%H:%M"))+"~"+str(self.end_time.strftime("%H:%M"))
        
    def __str__(self):
        return self.Users

        
class Users(models.Model):
    Users = models.CharField(max_length=100,null=True)#搞成一个下拉框，选择人名字
    description = models.CharField(max_length=100)#
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.Users} </a>'
        
    def __str__(self):
        return self.Users