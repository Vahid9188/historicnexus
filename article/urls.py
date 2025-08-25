from django.contrib import admin
from django.urls import path
from .import views

app_name='article'

urlpatterns = [
    path('addarticle/', views.addArticle,name="addarticle"),
    path('dashboard/', views.dashboard_view,name="dashboard"),
    path('edit/<int:pk>/', views.edit_article, name='edit_article'),
    path('delete/<int:pk>/', views.delete_article, name='delete_article'),
    path('all/', views.articles_list, name='articles_list'),
    path('<int:pk>/', views.articles_detail, name='articles_detail'),  # mövcud
    path('search/', views.search_view, name='search'),






   
    








]
