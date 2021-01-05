from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Создаем значения для выбора в выпадающем списке
CHOICES = (('male', 'Мужской пол'),('female', 'Женский пол'))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField('Фото пользователя', default='user.png', upload_to='user_images')
    # Создаем новые поля в самой таблице
    # Первое поле будет с галочкой, поэтому используем класс BooleanField
    mails = models.BooleanField(default=True)
    # Второе поле будет как выпадающий список, поэтому используем CharField
    # и в него помещаем список вариантов - choices
    sex = models.CharField(choices=CHOICES, default="Мужской пол", max_length=40)


    def __str__(self):
        return f'Профайл пользователя {self.user.username}'

    def save(self, *args, **kwargs):
        super().save()

        image = Image.open(self.img.path)

        if image.height > 256 or image.width > 256:
           resize = (256, 256)
           image.thumbnail(resize)
           image.save(self.img.path)

    class Meta:
        verbose_name = 'Профайл'
        verbose_name_plural = 'Профайлы'