from django.urls import path

from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.signup,name='index'),
    path('signup', views.signup,name='signup'),
    path('signin', views.signin,name='signin'),
    # path('admin', views.admin,name='admin'),
    path('events', views.events,name='events'),
    # path('play', views.playground,name='playground'),
    path('dashboard', views.dashboard,name='dashboard'),
    path('allguides',views.card,name='card'),
    # path('guide',views.guide_steps,name='guide_steps'),
    path("activate<uidb64>/<token>",views.activate,name="activate"),
    path('guide/<int:pk>', views.guide_blog, name='guide_blog'),

]
=======
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('dashboard', views.dashboard,name='dashboard'),]
>>>>>>> c1c126ae5ef0f62a5c3523fa891ae4712722c9be
