from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import News, MessCont
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Эта функция уже не нужна,т.к используется ListView
# def Home(request):
#
#     data = {
#         'news': News.objects.all(),
#         'title': 'Главная страница'
#     }
#
#     return render(request, 'home/index.html', data)

class ShowNewsView(ListView):
    model = News
    template_name = 'home/index.html'
    context_object_name = 'news'
    ordering = ['-date'] #Сортировка
    paginate_by = 3 #На одной стр выводится ток 2 записи

    def get_context_data(self, **kwards):
        ctx = super(ShowNewsView, self).get_context_data(**kwards)

        ctx['title'] = 'Главная страница'
        return ctx

class NewsDetailView(DeleteView):
    model = News
    template_name = 'home/news_datail.html' #вызов шаблона
    context_object_name = 'post' #Передаваемый объёект идёт по пост

    def get_context_data(self, **kwards):
        ctx = super(NewsDetailView, self).get_context_data(**kwards)

        ctx['title'] = News.objects.get(pk=self.kwargs['pk']) #находим одну запись у которой совпадает url с pk вытягиваем только название статьи
        return ctx

class DeleteNewsView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    success_url = '/' #После успешного удаление переадресация на главную стр.
    template_name = 'home/delete-news.html'

    def test_func(self): #Если условие не верно, то пользователя перекидывает на другую страничку
        news = self.get_object()
        if self.request.user == news.avtor: #Если это один и тот же автор то мы остаёмся, если нет, то выходим
            return True

        return False

class CreateNewsView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'home/create_news.html'

    fields = ['title', 'text']

    def get_context_data(self, **kwards):
        ctx = super(CreateNewsView, self).get_context_data(**kwards)

        ctx['title'] = 'Добовление статьи'
        ctx['btn_text'] = 'Добавить'
        return ctx

    def form_valid(self, form): #Отслеживание данных из фломы (получаем автора)
        form.instance.avtor = self.request.user #Обращаемся к значению зарегистрированного пользователя
        return super().form_valid(form) #Вызываем функцию в классе родителя

class UpdateNewsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    template_name = 'home/create_news.html'

    fields = ['title', 'text']

    def test_func(self): #Если условие не верно, то пользователя перекидывает на другую страничку
        news = self.get_object()
        if self.request.user == news.avtor: #Если это один и тот же автор то мы остаёмся, если нет, то выходим
            return True

        return False

    def get_context_data(self, **kwards):
        ctx = super(UpdateNewsView, self).get_context_data(**kwards)

        ctx['title'] = 'Обновление статьи'
        ctx['btn_text'] = 'Обновить'
        return ctx

    def form_valid(self, form): #Отслеживание данных из фломы (получаем автора)
        form.instance.avtor = self.request.user #Обращаемся к значению зарегистрированного пользователя
        return super().form_valid(form) #Вызываем функцию в классе родителя

class UserAllNewsView(ListView):
    model = News
    template_name = 'home/user_news.html'
    context_object_name = 'news'
    paginate_by = 3 #На одной стр выводится ток 2 записи

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username')) #Получаем login пользователя из url адреса  /user/...
        return News.objects.filter(avtor=user).order_by('-date') #Находим статью у которого поле автор будет равно поьзователю, где хранится имеил из таблицы юзер, сортировка по дате в обратном порядке

    def get_context_data(self, **kwards):
        ctx = super(UserAllNewsView, self).get_context_data(**kwards)

        ctx['title'] = f"Статьи от пользователя {self.kwargs.get('username')}" #название страницы
        return ctx

# def contacti(request):
#     return render(request, 'home/contact.html', {'title': 'Страница с контактами'})


# class MessagesCont(ListView):
#     model = User
#     template_name = 'home/contact.html'
#
#     def get_context_data(self, **kwards):
#         ctx = super(MessagesCont, self).get_context_data(**kwards)
#
#         ctx['title'] = 'Страница с контактами'
#         return ctx

@login_required
# def messagecont(request):
#     if request.method == "POST":
#         mess = ContactForm(request.POST)
#         if mess.is_valid():
#             order = mess.save(commit=False)
#             order.user = request.user
#             order.save()
#
#
#             return redirect('contacti')
#     else:
#         mess = ContactForm()
#
#     return render(request, 'home/contact.html',
#      {'title': 'Страница с контактами',
#      'form': mess})


def messagecont(request):
    if request.method == "POST":
        mess = ContactForm(request.POST)
        if mess.is_valid():
            order = mess.save(commit=False)
            order.user = request.user
            order.save()
            subject = request.POST.get('subject', '')
            plain_message = request.POST.get('plain_message', '')
            from_email = request.POST.get('from_email', 'admin@mail.ru')
            to = request.POST.get('to', '')
            if subject and plain_message and from_email and to:
                try:
                    send_mail(subject, plain_message, from_email, [to])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(request, 'Сообщение было успешно отправлено.')
                return HttpResponseRedirect('contacti')
            else:

                return HttpResponse('Make sure all fields are entered and valid.')
            return redirect('contacti')
    else:
        mess = ContactForm()

    return render(request, 'home/contact.html',
     {'title': 'Страница с контактами',
     'form': mess})
