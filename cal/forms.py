from django.forms import ModelForm, DateInput,Select,PasswordInput,ChoiceField,ModelChoiceField
from cal.models import Event
from datetime import datetime
from django import forms



class EventForm(ModelForm):
#  title = forms.ChoiceField(choices=USER_NMAE)
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local','value': datetime.now().strftime("%d-%m-%Y")}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local','value': datetime.now().strftime("%d-%m-%Y")}, format='%Y-%m-%dT%H:%M')
    }
    fields = '__all__'


  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    #users = Event.objects.all()
    #self.fields['Users']=forms.ModelChoiceField(queryset = Event.objects.all())
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

    #注释信息
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

    #类的方法：保存数据
	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user 