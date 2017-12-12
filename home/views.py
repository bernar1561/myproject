from django.shortcuts import render
from django.template import RequestContext
from django.template.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from knowledge.models import Article
from django.core.mail import send_mail
from .forms import ContactForm
from myproject import settings
# Create your views here.


class EIndexView(View):
    template_name = 'knowledge/index.html'

    def get(self, request, *args, **kwargs):
        context = {}
        # Забираем все опубликованные статье отсортировав их по дате публикации
        all_articles = Article.objects.filter(article_status=True).order_by('-article_date')
        # Создаём Paginator, в который передаём статьи и указываем,
        # что их будет 10 штук на одну страницу
        current_page = Paginator(all_articles, 10)
        # Pagination в django_bootstrap3 посылает запрос вот в таком виде:
        # "GET /?page=2 HTTP/1.0" 200,
        # Поэтому нужно забрать page и попытаться передать его в Paginator,
        # для нахождения страницы
        page = request.GET.get('page')
        try:
            # Если существует, то выбираем эту страницу
            context['article_lists'] = current_page.page(page)
        except PageNotAnInteger:
            # Если None, то выбираем первую страницу
            context['article_lists'] = current_page.page(1)
        except EmptyPage:
            # Если вышли за последнюю страницу, то возвращаем последнюю
            context['article_lists'] = current_page.page(current_page.num_pages)

        return render(request, 'home/index.html', context)


class EContactsView(View):
    template_name = 'home/contacts.html'

    # В случае get запроса, мы будем отправлять просто страницу с контактной формой
    def get(self, request, *args, **kwargs):
        context = {}
        context.update(csrf(request))    # Обязательно добавьте в шаблон защитный токен
        context['contact_form'] = ContactForm()

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context = {}

        form = ContactForm(request.POST)

        # Если не выполнить проверку на правильность ввода данных,
        # то не сможем забрать эти данные из формы... хотя что здесь проверять?
        if form.is_valid():
            email_subject = 'EVILEG :: Сообщение через контактную форму '
            email_body = "С сайта отправлено новое сообщение\n\n" \
                         "Имя отправителя: %s \n" \
                         "E-mail отправителя: %s \n\n" \
                         "Сообщение: \n" \
                         "%s " % \
                         (form.cleaned_data['name'], form.cleaned_data['email'], form.cleaned_data['message'])

            # и отправляем сообщение
            send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, ['target_email@example.com'], fail_silently=False)

        return render(request, template_name=self.template_name, context=context)


def any_request(request):
    context = {}
    context.update(csrf(request))
    return render(request, 'home/any_request.html', context=context)


def csrf_failure(request, reason=""):
    context = RequestContext(request)
    response = render(request, 'home/error403.html', context)
    response.status_code = 403
    return response


def e_handler404(request):
    context = RequestContext(request)
    response = render(request,'home/error404.html', context)
    response.status_code = 404
    return response


def e_handler500(request):
    context = RequestContext(request)
    response = render(request, 'home/error500.html', context)
    response.status_code = 500
    return response




