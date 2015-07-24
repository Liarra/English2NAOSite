from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager

# Create your models here.
from django.db.models import Model


class Scenario(models.Model):
    pickled_formal_description = models.BinaryField()
    # user = models.ForeignKey(User)


class Step(models.Model):
    scenario = models.ForeignKey(Scenario)
    step_name = models.CharField(max_length=100)
    step_description = models.TextField()


class Component(models.Model):
    tags = TaggableManager()
    regex = models.CharField(max_length=500)
    name = models.CharField(max_length=200)
    summary = models.TextField()
    params = models.TextField()


class ActionComponent(Component):
    pass


class AtomicActionComponent(ActionComponent):
    command = models.TextField(default="")
    component_class = models.CharField(max_length=500, default="Component")


class UserActionComponent(ActionComponent):
    program = models.ForeignKey(Scenario)
    icon = models.ImageField()
    tags = TaggableManager()
