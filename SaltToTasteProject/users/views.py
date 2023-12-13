from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, DetailView, View
from django.contrib.messages.views import SuccessMessageMixin, messages
from .forms import CustomUserCreationForm
from django.shortcuts import render
from .models import CustomUser, Subscription
from recipes.models import Recipe, Selection

from django.core.serializers import serialize
import json

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
        context['subscriptions'] = Subscription.objects.filter(follower=self.request.user).values_list('follower', flat=True) if self.request.user.is_authenticated else None
        context['subscribers'] = Subscription.objects.filter(following=self.request.user).values_list('following', flat=True) if self.request.user.is_authenticated else None

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

    # def profile(request):
    #     return render(request, 'users/profile.html')


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
    if request.user != following_user:
        try:
            subscription = Subscription.objects.get(follower=request.user, following=following_user)
            subscription.delete()
            status = 'unsubscribed'
        except Subscription.DoesNotExist:
            Subscription.objects.create(follower=request.user, following=following_user)
            status = 'subscribed'
        # print(following_user.get_sum_followers)
        return JsonResponse({'status': status, 'subs_count': following_user.get_sum_followers})



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

def subscribers(request, pk):
    user_subs = Subscription.objects.filter(following=pk)
    subs = [sub.follower for sub in user_subs]
    data = {
        'title': 'Мои подписчики',
        'title_another_user': 'Подписчики',
        'profile': CustomUser.objects.get(pk=pk),
        'subs': subs,
        'type': 'subscribers',
        'subscriptions': Subscription.objects.filter(follower=request.user).values_list('follower',
                                                                                                   flat=True) if request.user.is_authenticated else None,
        'subscribers': Subscription.objects.filter(following=request.user).values_list('following',
                                                                                                  flat=True) if request.user.is_authenticated else None,
    }
    return render(request, 'users/subscribers.html', data)


def subscriptions(request, pk):
    user_subs = Subscription.objects.filter(follower=pk)
    subs = [sub.following for sub in user_subs]
    data = {
        'title': 'Мои подписки',
        'title_another_user': 'Подписки',
        'profile': CustomUser.objects.get(pk=pk),
        'subs': subs,
        'type': 'subscriptions',
        'subscriptions': Subscription.objects.filter(follower=request.user).values_list('follower',
                                                                                             flat=True) if request.user.is_authenticated else None,
        'subscribers': Subscription.objects.filter(following=request.user).values_list('following',
                                                                                            flat=True) if request.user.is_authenticated else None,
    }
    return render(request, 'users/subscribers.html', data)



def profile_edit(request, pk):
    return render(request, 'users/editing_profile.html')



class search_subscribers(View):
    def get(self, request, pk):
        search_query = request.GET.get('search', '')
        if len(search_query) > 0:
            subs = Subscription.objects.filter(follower__username__icontains=search_query)
            subs = [sub.follower for sub in subs if sub.following.pk == pk]
        else:
            subs = Subscription.objects.filter(following=pk)
            subs = [sub.follower for sub in subs]
        subs_data = serialize('json', subs)
        subs_json = json.loads(subs_data)

        if request.user.is_authenticated:
            for sub in subs_json:
                sub['is_subscribed'] = Subscription.objects.filter(follower=request.user, following=sub['pk']).exists()

        user_data = {
            'is_authenticated': request.user.is_authenticated,
        }

        return JsonResponse({'subs': subs_json, 'user': user_data}, safe=False)


class search_subscriptions(View):
    def get(self, request, pk):
        search_query = request.GET.get('search', '')
        if len(search_query) > 0:
            subs = Subscription.objects.filter(following__username__icontains=search_query)
            subs = [sub.following for sub in subs if sub.follower.pk == pk]
        else:
            subs = Subscription.objects.filter(follower=pk)
            subs = [sub.following for sub in subs]
        subs_data = serialize('json', subs)
        subs_json = json.loads(subs_data)

        if request.user.is_authenticated:
            for sub in subs_json:
                sub['is_subscribed'] = Subscription.objects.filter(follower=request.user, following=sub['pk']).exists()

        user_data = {
            'is_authenticated': request.user.is_authenticated,
        }

        return JsonResponse({'subs': subs_json, 'user': user_data}, safe=False)