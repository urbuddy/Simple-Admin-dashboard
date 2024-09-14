from django.db import models

class Partner(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    mobile_no = models.CharField(max_length=20, unique=True, null=True, blank=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

