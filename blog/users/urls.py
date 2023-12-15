from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>', views.user_profile, name="user_profile"),
    path('account/', views.user_account,name='user_account'),
    path('edit_account/', views.edit_account,name='edit_account'),
    path('login/', views.login, name='login'),
    path('login/signup', views.sign_up, name='sign_up'),
    path('logout/', views.logout, name='logout'),

    path('create_skill/', views.create_skill, name="create_skill"),
    path('update_skill/<str:pk>/', views.update_skill, name="update_skill"),
    path('delete_skill/<str:pk>/', views.delete_skill, name="delete_skill"),

]