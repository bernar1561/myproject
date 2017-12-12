from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.db.models import Sum
from .models import *
from .forms import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.template.context_processors import csrf
# Create your views here.


class ENewsIndex(View):
    template_name = 'knowledge/index.html'

    def get(self, request, *args, **kwargs):
        context = {}
        context['section_list'] = Section.objects.all().order_by('section_title')
        return render(request, template_name=self.template_name, context=context)


class ESectionView(View):
    template_name = 'knowledge/section.html'

    def get(self, request, *args, **kwargs):
        context = {}
        section = get_object_or_404(Section, section_url=self.kwargs['section'])
        context['section'] = section
        return render(request, template_name=self.template_name, context=context)


class EArticleView(View):
    template_name = 'knowledge/article.html'
    comment_form = CommentForm

    def get(self, request,  *args, **kwargs):
        article = get_object_or_404(Article, id=self.kwargs['article_id'])
        context = {}
        # Далее забираем объект сегодняшней статистики или создаём новый, если требуется
        obj, created = ArticleStatistic.objects.get_or_create(
            defaults={
                "article": article,
                "date": timezone.now()
            },
            # При этом определяем, забор объекта статистики или его создание по двум полям: дата и внешний ключ на статью
            date=timezone.now(), article=article
        )
        obj.views += 1  # инкрементируем счётчик просмотров и обновляем поле в базе данных
        obj.save(update_fields=['views'])

        context.update(csrf(request))
        user = auth.get_user(request)
        context['article'] = article
        # Помещаем в контекст все комментарии, которые относятся к статье попутно сортируя их по пути, ID автоинкрементируемые, поэтому
        # проблем с иерархией комментариев не должно возникать
        # А теперь забираем список 5 последний самых популярных статей за неделю
        popular = ArticleStatistic.objects.filter(
            # отфильтровываем записи за последние 7 дней
            date__range=[timezone.now() - timezone.timedelta(7), timezone.now()]
        ).values(
            # Забираем интересующие нас поля, а именно id и заголовок
            # К сожалению забрать объект по внешнему ключу в данном случае не получится
            # Только конкретные поля из объекта
            'article_id', 'article__article_name', 'article__article_section__section_title'
        ).annotate(
            # Суммируем записи по просмотрам
            # Всё суммируется корректно с соответствием по запрашиваемым полям объектов
            views=Sum('views')
        ).order_by(
            # отсортируем записи по убыванию
            '-views')[:5]  # Заберём последние пять записей
        print(popular)
        context['popular_list'] = popular  # Отправим в контекст список статей
        context['comments'] = article.comment_set.all().order_by('path')
        context['next'] = article.get_absolute_url()
        # Будем добавлять форму только в том случае, если пользователь авторизован
        if user.is_authenticated:
            context['form'] = self.comment_form

        return render(request, template_name=self.template_name, context=context)

    # Декораторы по которым, только авторизованный пользователь
    # может отправить комментарий и только с помощью POST запроса
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        # if request.method == 'POST':

        form = CommentForm(request.POST)
        article = get_object_or_404(Article, id=self.kwargs['article_id'])
        if form.is_valid():
            comment = Comment(
                path=[],
                article_id=article,
                author_id=request.user,
                content=form.cleaned_data['comment_area']
            )
            comment.save()

            # Django не позволяет увидеть ID комментария по мы не сохраним его,
            # хотя PostgreSQL имеет такие средства в своём арсенале, но пока не будем
            # работать с сырыми SQL запросами, поэтому сформируем path после первого сохранения
            # и пересохраним комментарий
            try:
                comment.path.extend(Comment.objects.get(id=form.cleaned_data['parent_comment']).path)
                comment.path.append(comment.id)
            except ObjectDoesNotExist:
                comment.path.append(comment.id)
            comment.save()
        return redirect(article.get_absolute_url())

