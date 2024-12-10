from django.urls import path
from . import views
from .views import login_view


urlpatterns = [
    path('', views.main_page, name='main_page'),  # Главна страница
    path('issue/', views.issue_key, name='issue_key'),  # Издаване на ключ
    path('return/', views.return_key, name='return_key'),  # Връщане на ключ
    path('reports/', views.view_reports, name='view_reports'),  # Справки
    path('create_user/', views.create_user, name='create_user'),
    path('search-users/', views.search_users, name='search_users'),  # Нова справка
    path("login/", login_view, name="login"),
]
