from django import forms
from .models import MessCont


class ContactForm(forms.ModelForm):

     subject = forms.CharField(
         label='Тема сообщения',
         required=True,
         max_length=100,
         widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Форма отправки сообщений'})
      )

     from_email = forms.EmailField(
         label='Почта отправителя',
         required=True,
         widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите E-mail'})
     )

     to = forms.EmailField(
          label='Почта получателя',
          required=True,
          widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите E-mail'})
      )

     plain_message = forms.CharField(
           label='Текст сообщения',
           required=True,
           widget = forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст'})
        )

     class Meta:
        model = MessCont
        fields = ['subject', 'from_email','to', 'plain_message']