from translator.executables.nlp.commons import get_model_from_atomic_action, get_model_from_atomic_condition
from translator.executables.nlp.components.moves.demo_moves import *
from translator.executables.nlp.components.robot_commands import *

__author__ = 'nina'

from django.db import models, migrations


def create_atomic(something, something_else):
    actions = [say_command(), wait_command(),
               cry, dance, stand, crouch]

    conditions = [button_press()]

    # action_models = [get_model_from_atomic_action(a) for a in actions]
    # condition_models = [get_model_from_atomic_condition(c) for c in conditions]

    for a in actions:
        action_model = get_model_from_atomic_action(a)
        action_model.save()
        for t in a.tags:
            action_model.tags.add(t)
        action_model.save()

    for c in conditions:
        action_model = get_model_from_atomic_condition(c)
        action_model.save()
        for t in c.tags:
            action_model.tags.add(t)
        action_model.save()


class Migration(migrations.Migration):
    dependencies = [
        ('translator', '0002_components'),
    ]

    operations = [
        migrations.RunPython(create_atomic)
    ]
