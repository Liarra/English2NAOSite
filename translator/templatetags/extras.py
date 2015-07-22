from translator.executables.nlp.components.robot_commands import move_command, Command

__author__ = 'NBUCHINA'
from django import template

register = template.Library()


@register.filter(name='get_class')
def get_class(value):
    return value.__class__.__name__


@register.filter(name='str')
def get_str(value):
    return str(value)


@register.filter(name='icon')
def get_icon(value):
    folder = '/static/translator/img/icons/'
    icon = ''
    if isinstance(value, Command):
        body_part = value.params['body_part']

        if body_part == 'crouch':
            icon = 'crouch.png'
        elif body_part == 'sit':
            icon = 'sit.png'

        elif body_part == 'stand':
            icon = 'stand.png'
        elif body_part == 'stand-arm':
            icon = 'stand-arm.png'
        elif body_part == 'stand-head':
            icon = 'stand-head.png'
        elif body_part == 'stand-legs':
            icon = 'stand-legs.png'

        elif body_part == 'tts':
            icon = 'say.png'
        elif body_part == 'timer':
            icon = 'wait.png'

        return folder + icon

    else:
        return None
