from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
# from django.db import models
# from django.forms import ModelForm


class UserRegForm(UserCreationForm):
    email = forms.EmailField(
    label='Введите E-mail',
    required=True,
    widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите E-mail'})
    )

    username = forms.CharField(
    label='Введите Login',
    required=True,
    help_text='Нельзя вводить символы: @, /, _',
    widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите Login'})
    )
    # some = forms.ModelChoiceField(queryset=User.objects.all())
    password1 = forms.CharField(
    label='Введите Password',
    required=True,
    help_text='Пароль не должент быть простым',
    widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите Password'}))

    password2 = forms.CharField(label='Подтвержите Password', required=True, widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите Password'}))
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
     email = forms.EmailField(
         label='Введите E-mail',
         required=True,
         widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите E-mail'})
     )
     username = forms.CharField(
         label='Введите Login',
         required=True,
          help_text='Нельзя вводить символы: @, /, _',
          widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите Login'})
      )

     class Meta:
          model = User
          fields = ['username', 'email']


class ProfileImageForm(forms.ModelForm):
     # img = forms.ImageField(
     #     label='Загрузить фото',
     #     required=False,
     #     widget= forms.FileInput)
     def __init__(self, *args, **kwards):
         super(ProfileImageForm, self).__init__(*args, **kwards)
         self.fields['img'].label = "Изображение профиля"
         # Меняме названия для полей что будут отображаться в самой форме
         self.fields['sex'].label = "Выберите пол"
         self.fields['mails'].label = "Соглашение про отправку уведомлений на почту"

     class Meta:
         model = Profile
         fields = ['img','sex', 'mails']
