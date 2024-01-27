from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (PasswordResetConfirmView,
                                       PasswordResetView)
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
    path('government_profile/<int:pk>', views.government_profiles_details, name='government_profiles_details'),    path('government_profile/<int:pk>', views.government_profiles_details, name='government_profiles_details'),
    path('all_events/', views.all_events, name='all_events'),
    path('map/', views.map, name='map'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('view_profile/<str:username>/', views.view_profile, name='view_profile'),
    path('feedback', views.feedback, name='feedback'),
    path('create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('get-names/', views.get_names, name='get_names'),
    path('change_password/<str:username>/', views.change_password, name='change_password'),
    path('post/<int:post_id>/comment/', views.add_comment, name='comment_post'),
    path('report-post/<int:post_id>/', views.report_post, name='report_post'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='passwordreset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='resetdone.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='resetcomplete.html'), name='password_reset_complete'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),

]