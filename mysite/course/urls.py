from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^flights$', views.flights, name='flights'),
    url(r'^find$', views.find, name='find'),
    url(r'^add$', views.add, name='add'),
    url(r'^edit/(?P<id>[0-9]+)$', views.edit, name='edit'),
]