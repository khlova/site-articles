from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class News(models.Model):
    title = models.CharField('Название статьи', max_length=100, unique=True)
    text = models.TextField('Основной текст статьи')
    date = models.DateTimeField(default = timezone.now)
    avtor = models.ForeignKey(User, on_delete=models.CASCADE)


    views = models.IntegerField('Просмотры', default=1)
    # sizes = (
    #     ('S', 'Small'),
    #     ('M', 'Medium'),
    #     ('L', 'Large'),
    #     ('XL', 'X Large'),
    # )
    #
    # shop = models.CharField(max_length=2, choices = sizes, default='L')

    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'pk':self.pk}) #создание url для каждой статьи

    def __str__(self):
        return f'Новость: {self.title}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class MessCont(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField('Тема сообщения', max_length=100)
    plain_message = models.TextField('Текст сообщения')
    from_email = models.EmailField('Почта отправителя')
    to = models.EmailField('Почта получателя')

    def __str__(self):
        return f'Сообщение пользователя {self.user.username}'


