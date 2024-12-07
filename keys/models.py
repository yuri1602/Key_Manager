from django.db import models

# Create your models here
from django.db import models
from django.contrib.auth.models import User  # Вграден модел за потребители
from django.db import models

class Employee(models.Model):
    username = models.CharField(max_length=150, unique=True, verbose_name="Потребителско име")
    department = models.CharField(max_length=100, verbose_name="Отдел")
    code = models.CharField(max_length=20, unique=True, verbose_name="Код")

  

    class Meta:
        verbose_name = "Служител"
        verbose_name_plural = "Служители"

class Key(models.Model):
    name = models.CharField(max_length=100)  # Име на ключа
    barcode = models.CharField(max_length=50, unique=True)  # Уникален баркод
    location = models.CharField(max_length=100)  # Локация на ключа
    is_issued = models.BooleanField(default=False)  # Дали е издаден
    issued_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="issued_keys"
    )  # Кой потребител го е взел
    issued_at = models.DateTimeField(null=True, blank=True)  # Кога е издаден

    def __str__(self):
        return self.name


class KeyHistory(models.Model):
    key = models.ForeignKey(
        Key, on_delete=models.CASCADE, related_name="history"
    )  # Връзка към ключа
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )  # Потребител, който е взел/върнал ключа
    issued_at = models.DateTimeField()  # Време на издаване
    returned_at = models.DateTimeField(null=True, blank=True)  # Време на връщане

    def __str__(self):
        return f"{self.key.name} - {self.user.username if self.user else 'Unknown'}"