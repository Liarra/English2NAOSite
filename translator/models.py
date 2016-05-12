from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager

# Create your models here.
from django.db.models import Model


class Scenario(models.Model):
    pickled_formal_description = models.BinaryField()
    user = models.ForeignKey(User)


class UserLibrary(models.Model):
    user = models.ForeignKey(User)
    pass


class Step(models.Model):
    scenario = models.ForeignKey(Scenario)
    step_name = models.CharField(max_length=100)
    step_description = models.TextField()


class Component(models.Model):
    tags = TaggableManager()
    regex = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=200)
    summary = models.TextField()
    params = models.TextField()


class Behaviour(models.Model):
    is_atomic = models.BooleanField()
    implementation = models.OneToOneField(Component)
    user_library=models.ManyToManyField(UserLibrary)


class ActionComponent(Component):
    pass


class AtomicActionComponent(ActionComponent):
    command = models.TextField(default="")
    component_class = models.CharField(max_length=500, default="Component")


class UserActionComponent(ActionComponent):
    program = models.ForeignKey(Scenario)
    icon = models.ImageField()


class ConditionComponent(Component):
    pass


class AtomicConditionComponent(ConditionComponent):
    command = models.TextField(default="")
    component_class = models.CharField(max_length=500, default="Condition")


class UserConditionComponent(ConditionComponent):
    program = models.ForeignKey(Scenario)
    icon = models.ImageField()
