from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Usuario(models.Model):
    role = models.CharField(
        max_length=2,
        choices=settings.SOLICITUD_ESTATUS_CHOICES,
        default=settings.SOLICITUD_ESTATUS_CHOICES[0][0],
    )
    user = models.ForeignKey(User, related_name='owner', blank=True, null=True)
    # class Meta:
    #     proxy = True
