from django.conf.urls.defaults import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
