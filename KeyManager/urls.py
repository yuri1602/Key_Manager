
from django.contrib import admin
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('keys.urls')),  # Пренасочва празния път към приложението keys
    path('keys/', include('keys.urls')),  # Приложението keys
]

