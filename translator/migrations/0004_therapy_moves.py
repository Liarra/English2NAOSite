from django.db import migrations
from translator.executables.nlp.commons import get_model_from_atomic_action
from translator.executables.nlp.components.moves.therapy_moves import *

__author__ = 'NBUCHINA'


def create_therapy(something, something_else):
    actions = [sit, nod, shake_no, stretch_hand]

    for a in actions:
        action_model = get_model_from_atomic_action(a)
        action_model.save()
        for t in a.tags:
            action_model.tags.add(t)
        action_model.save()


class Migration(migrations.Migration):
    dependencies = [
        ('translator', '0003_create_atomic_components'),
    ]

    operations = [
        migrations.RunPython(create_therapy)
    ]
