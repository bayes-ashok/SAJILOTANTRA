from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('dashboard', views.dashboard,name='dashboard'),]
