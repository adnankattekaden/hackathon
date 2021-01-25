from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.consumer_homepage,name='consumer_homepage'),
    path('login/', views.consumer_login,name='consumer_login'),
    path('login_popup/',views.popup_login,name='login_popup'),
    path('register/',views.consumer_registration,name='consumer_register'),
    path('mobile_login/',views.mobile_login,name='mobile_login'),
    path('verify_otp/', views.verify_otp,name='verify_otp'),
    path('forgot_password/', views.consumer_forgot_password, name='consumer_forgot_password'),
    path('logout/',views.consumer_logout,name='consumer_logout'),
    path('profile/',views.consumer_profile, name='consumer_profile'),
    path('edit_profile/<int:id>/', views.consumer_profile_edit, name='consumer_profile_edit'),
    path('change_password/<int:id>/',views.consumer_password_change,name='consumer_password_change'),
    path('music_player/<int:id>/',views.music_player,name='music_player'),
    path('playlist/', views.consumer_playlist,name='playlist'),
    path('latest/',views.consumer_latest_feed,name='latest'),
    path('next/<int:id>/',views.next_music_data,name='nextsong'),
    path('previous/<int:id>/', views.previous_music_data,name='previousmusic'),
]