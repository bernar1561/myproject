from django import template
from django.db.models import Sum
from django.utils import timezone
from knowledge.models import ArticleStatistic

register = template.Library()


# Пишем тег для публикации популярных новостей
@register.simple_tag
def get_popular_articles_for_week():

    popular = ArticleStatistic.objects.filter(
        # отфильтровываем записи за последние 7 дней
        date__range=[timezone.now() - timezone.timedelta(7), timezone.now()]
    ).values(
        # Забираем интересующие нас поля, а именно id и заголовок
        # К сожалению забрать объект по внешнему ключу в данном случае не получится
        # Только конкретные поля из объекта
        'article_id', 'article__article_name', 'article__articlestatistic__views', 'article__article_section__section_title'
    ).annotate(
        # Суммируем записи по просмотрам
        sum_views=Sum('views')
    ).order_by(
        # отсортируем записи по убыванию
        '-sum_views')[:5]
    # Заберём последние пять записей

    return popular
