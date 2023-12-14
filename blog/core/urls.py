from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.blogs, name="blogs"),
    path('blog/<str:pk>/', views.blog_project, name='blog'),
    path('create-blog/', views.create_blog, name='create'),
    path('update-blog/<str:pk>/', views.update_blog, name='update'),
     path('delete-blog/<str:pk>/', views.delete_blog, name='delete')

]
