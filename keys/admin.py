from django.contrib import admin
from .models import Key, KeyHistory
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('username', 'department', 'code')
    search_fields = ('username', 'department', 'code')

@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode', 'location', 'is_issued', 'issued_to', 'issued_at')
    list_filter = ('is_issued', 'location')
    search_fields = ('name', 'barcode', 'location')


@admin.register(KeyHistory)
class KeyHistoryAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'issued_at', 'returned_at')
    list_filter = ('issued_at', 'returned_at')
    search_fields = ('key__name', 'user__username')

