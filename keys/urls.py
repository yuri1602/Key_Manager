from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),  # Главна страница
    path('issue/', views.issue_key, name='issue_key'),  # Издаване на ключ
    path('return/', views.return_key, name='return_key'),  # Връщане на ключ
    path('reports/', views.view_reports, name='view_reports'),  # Справки
    path('create_user/', views.create_user, name='create_user'),
]
