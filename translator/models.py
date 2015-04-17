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