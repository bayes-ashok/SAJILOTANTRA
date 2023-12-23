from django.urls import path

from . import views

urlpatterns = [
    path('', views.signup,name='index'),
    path('signup', views.signup,name='signup'),
    path('signin', views.signin,name='signin'),
    # path('admin', views.admin,name='admin'),
    path('events', views.events,name='events'),
    # path('play', views.playground,name='playground'),
    path('dashboard', views.dashboard,name='dashboard'),
<<<<<<< HEAD
    path('allguides',views.card,name='card'),
    # path('guide',views.guide_steps,name='guide_steps'),
    path("activate<uidb64>/<token>",views.activate,name="activate"),
    path('guide/<int:pk>', views.guide_blog, name='guide_blog'),

=======
    path('government_profiles',views.government_profiles,name='government_profiles'),
    path('government_profiles_details/<int:pk>/', views.government_profiles_details, name='government_profiles_details'),
    path("activate<uidb64>/<token>",views.activate,name="activate")
>>>>>>> bcca05f4e3476767a43f846b55168fd9acaea639
]