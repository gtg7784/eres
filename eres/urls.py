from django.conf.urls import url

from . import views

urlpatterns = [
    url('index/', views.index, name='index'),
    url(r'^$', views.index, name='index'),
    url('generic/', views.generic, name='generic'),
    url('post/', views.post, name='post'),
    url('signin/', views.signin, name='signin'),
    url('signup/', views.signup, name='signup'),
    url('signout/', views.signout, name='signout'),
    url('myinfo/', views.myinfo, name="myinfo")
]
