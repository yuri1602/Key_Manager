from django.db import models
from django.contrib.auth.models import User  # Ако използвате вградените потребители

class Key(models.Model):
    name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=100)
    is_issued = models.BooleanField(default=False)
    issued_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    issued_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class KeyHistory(models.Model):
    key = models.ForeignKey(Key, on_delete=models.CASCADE, related_name="history")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    issued_at = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.key.name} - {self.user.username} ({self.issued_at})"
