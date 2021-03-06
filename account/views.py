from urllib.parse import urlparse
from django.shortcuts import redirect, render
from django.contrib import auth
from django.template.context_processors import csrf
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from .special_func import get_next_url
from django.contrib.auth.views import logout
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def logout_view(request):
    logout(request)
    return redirect('home:index')


class ELoginView(View):
    def get(self, request):
        # если пользователь авторизован, то делаем редирект на главную страницу
        if auth.get_user(request).is_authenticated:
            return redirect('/')
        else:
            # Иначе формируем контекст с формой авторизации и отдаём страницу
            # с этим контекстом.
            # работает, как для url - /admin/login/ так и для /account/login/
            context = create_context_username_csrf(request)
            return render(request, 'account/login.html', context=context)

    def post(self, request):
        # получив запрос на авторизацию
        form = AuthenticationForm(request, data=request.POST)

        # проверяем правильность формы, что есть такой пользователь
        # и он ввёл правильный пароль
        if form.is_valid():
            # в случае успеха авторизуем пользователя
            auth.login(request, form.get_user())
            # получаем предыдущий url
            next = urlparse(get_next_url(request)).path
            # и если пользователь из числа персонала и заходил через url /admin/login/
            # то перенаправляем пользователя в админ панель
            if next == '/admin/login/' and request.user.is_staff:
                return redirect('/admin/')
            # иначе делаем редирект на предыдущую страницу,
            # в случае с /account/login/ произойдёт ещё один редирект на главную страницу
            # в случае любого другого url, пользователь вернётся на данный url
            return redirect(next)

        # если данные не верны, то пользователь окажется на странице авторизации
        # и увидит сообщение об ошибке
        context = create_context_username_csrf(request)
        context['login_form'] = form

        return render(request, 'account/login.html', context=context)


# вспомогательный метод для формирования контекста с csrf_token
# и добавлением формы авторизации в этом контексте
def create_context_username_csrf(request):
    context = {}
    context.update(csrf(request))
    context['login_form'] = AuthenticationForm
    return context


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})
# class RegisterFormView(FormView):
#     form_class = UserCreationForm
#
#     # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
#     # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
#     success_url = "/login/"
#
#     # Шаблон, который будет использоваться при отображении представления.
#     template_name = "registration/register.html"
#
#     def form_valid(self, form):
#         # Создаём пользователя, если данные в форму были введены корректно.
#         form.save()
#
#         # Вызываем метод базового класса
#         return super(RegisterFormView, self).form_valid(form)

# class EditProfileView(ListView):


class EditProfileView(View):
    template_name = 'account/edit.html'
    user_form = UserEditForm
    profile_form = ProfileEditForm

    def get(self, request, *args, **kwargs):
        context = {}
        context.update(csrf(request))
        user = auth.get_user(request)
        if user.is_authenticated:
            context['user_form'] = self.user_form
            context['profile_form'] = self.profile_form
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            user_form = UserEditForm(instance=request.user, data=request.POST)
            profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()

                return redirect('profile')

        # else:
        #     user_form = UserEditForm(instance=request.user)
        #     profile_form = ProfileEditForm(instance=request.user.profile)
        #     return render(request,
        #                   'account/edit.html',
        #                   {'user_form': user_form,
        #                    'profile_form': profile_form})


class ProfileView(View):
    template_name = 'account/profile.html'

    def get(self, request, *args, **kwargs):
        context = {}
        context.update(csrf(request))
        a = User.objects.filter(username=auth.get_user(request))
        for i in a:
            print(i)
        context['profile'] = User.objects.filter(username=auth.get_user(request))
        return render(request, template_name=self.template_name, context=context)
