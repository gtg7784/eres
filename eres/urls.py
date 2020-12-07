from django.conf.urls import url

from . import views

urlpatterns = [
    url('index/', views.index, name='index'),
    url('generic/', views.generic, name='generic'),
    url('signin/', views.signin, name='signin'),
    url('signup/', views.signup, name='signup'),
    url('signout/', views.signout, name='signout'),
    url('post/', views.post, name='post')
]

