from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Model


class RobotProgram(models.Model):
    text_description = models.TextField
    pickled_formal_description = models.TextField
    user = models.ForeignKey(User)