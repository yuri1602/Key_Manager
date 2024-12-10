from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView


urlpatterns = [
    path('', views.main_page, name='main_page'),  # Главна страница
    path('issue/', views.issue_key, name='issue_key'),  # Издаване на ключ
    path('return/', views.return_key, name='return_key'),  # Връщане на ключ
    path('reports/', views.view_reports, name='view_reports'),  # Справки
    path('create_user/', views.create_user, name='create_user'),
     path('search-users/', views.search_users, name='search_users'),  # Нова справка.
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

