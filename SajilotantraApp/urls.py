from django.urls import path
from .views import report_post, view_reported_post
from .views import password_reset, verify_code, reset_password, verification_sent


from . import views

urlpatterns = [
    path('', views.signup,name='index'),
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
    path('change_password/', views.change_password, name='change_password'),
    path('change_password/<str:username>/', views.change_password, name='change_password'),

    path('report_post/<int:post_id>/', views.report_post, name='report_post'),
    path('view_reported_post/<int:reported_post_id>/', view_reported_post, name='view_reported_post'),
    path('report_post/', report_post, name='report_post'),
    path('view_reported_post/<int:post_id>/', view_reported_post, name='view_reported_post'),

    path('password_reset/', password_reset, name='password_reset'),
    path('verify_code/', verify_code, name='verify_code'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('verification_sent/', verification_sent, name='verification_sent'),
]