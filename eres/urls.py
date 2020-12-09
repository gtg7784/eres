from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.index, name='index'),
    path('category/<slug:category>', views.category, name='category'),
    path('generic/<int:post_id>', views.generic, name='generic'),
    path('post/', views.post, name='post'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('myinfo/', views.myinfo, name="myinfo")
]

app_name = "eres"