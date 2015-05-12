from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Model


class RobotProgram(models.Model):
    pickled_formal_description = models.BinaryField()
    # user = models.ForeignKey(User)


class ProgramStep(models.Model):
    program = models.ForeignKey(RobotProgram)
    step_name = models.CharField(max_length=100)
    step_description = models.TextField()


class ActionComponent(models.Model):
    tags = models.TextField()
    regex = models.CharField(max_length=500)
    name = models.CharField(max_length=200)
    summary = models.TextField()
    params = models.TextField()


class AtomicActionComponent(ActionComponent):
    command = models.TextField()


class UserActionComponent(ActionComponent):
    program = models.ForeignKey(RobotProgram)
    icon = models.ImageField()
