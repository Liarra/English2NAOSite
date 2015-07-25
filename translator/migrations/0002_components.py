# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('translator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('regex', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=200)),
                ('summary', models.TextField()),
                ('params', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ActionComponent',
            fields=[
                ('component_ptr', models.OneToOneField(serialize=False, auto_created=True, to='translator.Component', primary_key=True, parent_link=True)),
            ],
            bases=('translator.component',),
        ),
        migrations.CreateModel(
            name='ConditionComponent',
            fields=[
                ('component_ptr', models.OneToOneField(serialize=False, auto_created=True, to='translator.Component', primary_key=True, parent_link=True)),
            ],
            bases=('translator.component',),
        ),
        migrations.AddField(
            model_name='component',
            name='tags',
            field=taggit.managers.TaggableManager(through='taggit.TaggedItem', help_text='A comma-separated list of tags.', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='AtomicActionComponent',
            fields=[
                ('actioncomponent_ptr', models.OneToOneField(serialize=False, auto_created=True, to='translator.ActionComponent', primary_key=True, parent_link=True)),
                ('command', models.TextField(default='')),
                ('component_class', models.CharField(default='Component', max_length=500)),
            ],
            bases=('translator.actioncomponent',),
        ),
        migrations.CreateModel(
            name='AtomicConditionComponent',
            fields=[
                ('conditioncomponent_ptr', models.OneToOneField(serialize=False, auto_created=True, to='translator.ConditionComponent', primary_key=True, parent_link=True)),
                ('command', models.TextField(default='')),
                ('component_class', models.CharField(default='Condition', max_length=500)),
            ],
            bases=('translator.conditioncomponent',),
        ),
        migrations.CreateModel(
            name='UserActionComponent',
            fields=[
                ('actioncomponent_ptr', models.OneToOneField(serialize=False, auto_created=True, to='translator.ActionComponent', primary_key=True, parent_link=True)),
                ('icon', models.ImageField(upload_to='')),
                ('program', models.ForeignKey(to='translator.Scenario')),
            ],
            bases=('translator.actioncomponent',),
        ),
        migrations.CreateModel(
            name='UserConditionComponent',
            fields=[
                ('conditioncomponent_ptr', models.OneToOneField(serialize=False, auto_created=True, to='translator.ConditionComponent', primary_key=True, parent_link=True)),
                ('icon', models.ImageField(upload_to='')),
                ('program', models.ForeignKey(to='translator.Scenario')),
            ],
            bases=('translator.conditioncomponent',),
        ),
    ]
