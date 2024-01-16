from django.urls import path

from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('signup', views.signup,name='signup'),
    path('signin', views.signin,name='signin'),
    # path('admin', views.admin,name='admin'),
    path('events', views.events,name='events'),
    # path('play', views.playground,name='playground'),
    path('dashboard', views.dashboard,name='dashboard'),
    path("activate<uidb64>/<token>",views.activate,name="activate"),
    path('allguides',views.card,name='card'),
    path('guide/<int:pk>', views.guide_blog, name='guide_blog'),
    path('government_profiles',views.government_profiles,name='government_profiles'),
    path('government_profile/<int:pk>', views.government_profiles_details, name='government_profiles_details'),
    path('all_events/', views.all_events, name='all_events'),
    path('map/', views.map, name='map'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('view_profile/<str:username>/', views.view_profile, name='view_profile'),
    path('feedback', views.feedback, name='feedback'),
    path('create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('get-names/', views.get_names, name='get_names'),
]