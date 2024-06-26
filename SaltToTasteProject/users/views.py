from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin, messages
from .forms import CustomUserCreationForm
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

    # # Функция для кастомной валидации полей формы модели
    def form_valid(self, form):
        # создаем форму, но не отправляем его в БД, пока просто держим в памяти
        fields = form.save(commit=False)
        print(self.request.user)
        # Через реквест передаем недостающую форму, которая обязательна
        fields.username = self.request.POST.get('nickname')
        # Наконец сохраняем в БД
        fields.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(f"--------------------")
        # Сохраняем сообщение об ошибке в сессию
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)

        # Возвращаем HTTP-ответ с кодом ошибки
        return super().form_invalid(form)


# class SignUp(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('home_page')
#     template_name = 'users/signup.html'

class LoginUser(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_message = 'Успешная авторизация'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def form_invalid(self, form):
        # Сохраняем сообщение об ошибке в сессию
        messages.error(self.request, ('Ошибка аутентификации'))
        # Возвращаем HTTP-ответ с кодом ошибки
        return super().form_invalid(form)

    def get_success_url(self):
        print(self.request.user)
        return reverse_lazy('home')
