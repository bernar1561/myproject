from django.contrib import admin
from .models import Section, Article, Comment, ArticleStatistic
# Register your models here.


@admin.register(ArticleStatistic)
class ArticleStatisticAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'views')  # отображаемые поля в админке
    search_fields = ('__str__', )


admin.site.register(Section)
admin.site.register(Article)
admin.site.register(Comment)