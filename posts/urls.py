from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),

    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('posts/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('posts/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('posts/<slug:slug>/comment/', views.add_comment, name='add_comment'),

    path('category/<str:category>/', views.post_category, name='post_category'),
    path('new/', views.post_create, name='post_create'),
]