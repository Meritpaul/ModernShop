from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email  = models.EmailField(unique=True)
    phone  = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio    = models.TextField(blank=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Address(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name    = models.CharField(max_length=200)
    phone        = models.CharField(max_length=20)
    address_line = models.TextField()
    city         = models.CharField(max_length=100)
    state        = models.CharField(max_length=100, blank=True)
    zip_code     = models.CharField(max_length=20, blank=True)
    country      = models.CharField(max_length=100, default='Bangladesh')
    is_default   = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{self.full_name} — {self.city}"

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
