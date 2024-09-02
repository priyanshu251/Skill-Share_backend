from django.db import models


class User(models.Model):
    uid = models.CharField(max_length=128, unique=True, primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(unique=True)
    picture = models.TextField()

# User._meta.fields_map