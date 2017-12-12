from django.conf.urls import url
from .views import ELoginView

app_name = 'accounts'
urlpatterns = [
    url(r'^login/$', ELoginView.as_view(), name='login'),
]
