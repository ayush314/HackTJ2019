from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register', views.register, name='register'),
    url(r'^login', views.log_in, name='login'),
    url(r'^manage', views.manage_profile, name='manage'),
    url(r'^paramount', views.paramount, name='paramount'),
]
