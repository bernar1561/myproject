from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', SearchView.as_view(), name='index'),
]