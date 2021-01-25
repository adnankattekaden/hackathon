from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.login_creator, name='login_creator'),
    path('logout_creator/', views.creator_logout, name='logout_creator'),
    path('register_creator/', views.register_creator, name='register_creator'),
    path('profile/', views.creator_profile,name='creator_profile'),
    path('edit_profile/<int:id>', views.edit_creator_profile,name='edit_creator_profile'),
    path('dashboard/', views.creator_dashboard, name='creator_dashboard'),
    path('contents/', views.display_contents, name='display_content'),
    path('create_content/', views.create_content, name='create_content'),
    path('edit_content/<int:id>/', views.edit_content, name='edit_content'),
    path('delete_content/<int:id>/',views.delete_content, name='delete_content'),
]