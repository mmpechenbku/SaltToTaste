from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, DetailView
from django.contrib.messages.views import SuccessMessageMixin, messages
from .forms import CustomUserCreationForm
from django.shortcuts import render
from .models import CustomUser, Subscription
from recipes.models import Recipe, Selection

# def index(request):
#     return render(request, 'index.html')


def profile(request):
    return render(request, 'users/profile.html')


class ProfileDetailView(DetailView):
    model = CustomUser
    context_object_name = 'profile'
    template_name = 'users/profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        recipes = Recipe.objects.filter(author=self.object)
        context['recipes'] = recipes
        context['selections'] = Selection.objects.filter(user=self.object)

        recipe_ingr_dict = []
        for recipe in recipes:
            ingredients = []
            for ingredient in recipe.ingredients.all():
                ingredients.append(ingredient.name)
            recipe_ingr_dict.append({recipe: ingredients})

        context['recipes_ingr'] = recipe_ingr_dict

        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = f'Страница пользователя: {self.object.user.username}'
    #     return context


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'users/sign.html'

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


class Login(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'users/sign.html'
    success_message = 'Успешная авторизация'

    # print('in views')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        context['form'] = self.get_form()
        # print('in get')
        return context

    def form_invalid(self, form):
        # Сохраняем сообщение об ошибке в сессию
        messages.error(self.request, ('Ошибка аутентификации'))

        return HttpResponseRedirect('/search')

        # Возвращаем HTTP-ответ с кодом ошибки
        # print('invalid')
        return super().form_invalid(form)

    def get_success_url(self):
        print(self.request.user)
        # print('success')
        return reverse_lazy('home')

    def profile(request):
        return render(request, 'users/profile.html')

    @login_required
    def toggle_subscription(request, user_id):
        # Получаем пользователя, на которого будет подписка
        following_user = User.objects.get(pk=user_id)

        # Пытаемся найти существующую подписку
        try:
            subscription = Subscription.objects.get(follower=request.user, following=following_user)
            # Если подписка существует, удаляем ее
            subscription.delete()
            status = 'unsubscribed'
        except Subscription.DoesNotExist:
            # Если подписка не существует, создаем ее
            Subscription.objects.create(follower=request.user, following=following_user)
            status = 'subscribed'

        # Возвращаем JSON-ответ
        return JsonResponse({'status': status})


@login_required
def subscription(request, user_id):
    # Получаем пользователя, на которого будет подписка
    following_user = CustomUser.objects.get(pk=user_id)

    # Пытаемся найти существующую подписку
    try:
        subscription = Subscription.objects.get(follower=request.user, following=following_user)
        # Если подписка существует, удаляем ее
        subscription.delete()
        status = 'unsubscribed'
    except Subscription.DoesNotExist:
        # Если подписка не существует, создаем ее
        Subscription.objects.create(follower=request.user, following=following_user)
        status = 'subscribed'

    # Возвращаем JSON-ответ
    return JsonResponse({'status': status})


# def get_user_recipes(request):
#     user_id = request.GET.get('user_id')
#     user_recipes = Recipe.objects.filter(author=user_id)
#
#     data = {'recipes': user_recipes}
#     return JsonResponse(data)
#
# def get_user_collections(request):
#     # Логика для получения подборок пользователя
#     user_id = request.GET.get('user_id')
#     user_collections = Selection.objects.filter(user=user_id)
#
#     data = {'collections': user_collections}
#     return JsonResponse(data)