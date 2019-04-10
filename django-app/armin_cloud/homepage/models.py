from django.db import models
from django.contrib.auth.models import User


class ArminCloudComponent(models.Model):
    """Abstract class for all components"""
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ArminRobot(ArminCloudComponent):
    """ArminRobot"""
    name = models.CharField(max_length=80, null=True, blank=True)
    serial_number = models.IntegerField(null=True, blank=True, unique=True)
    armin_of_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_id', null=True, blank=True)

