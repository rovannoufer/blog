from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>', views.user_profile, name="user_profile"),
    
    path('login/', views.login, name='login'),
    path('login/signup', views.sign_up, name='sign_up'),
    path('logout/', views.logout, name='logout')
]