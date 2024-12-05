from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # За използване на AUTH_USER_MODEL

# Персонализиран потребителски модел
class CustomUser(AbstractUser):
    nfc_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return self.username

# Модел за ключове
class Key(models.Model):
    name = models.CharField(max_length=100)  # Име на ключа
    barcode = models.CharField(max_length=50, unique=True)  # Уникален баркод
    location = models.CharField(max_length=100)  # Локация на ключа
    is_issued = models.BooleanField(default=False)  # Дали е издаден
    issued_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="issued_keys"
    )  # Кой потребител го е взел
    issued_at = models.DateTimeField(null=True, blank=True)  # Кога е издаден

    def __str__(self):
        return self.name

# История на ключовете
class KeyHistory(models.Model):
    key = models.ForeignKey(
        Key, on_delete=models.CASCADE, related_name="history"
    )  # Връзка към ключа
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )  # Потребител, който е взел/върнал ключа
    issued_at = models.DateTimeField()  # Време на издаване
    returned_at = models.DateTimeField(null=True, blank=True)  # Време на връщане

    def __str__(self):
        return f"{self.key.name} - {self.user.username if self.user else 'Unknown'}"
