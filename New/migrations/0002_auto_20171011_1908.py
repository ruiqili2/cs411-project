# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-11 19:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('New', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='Creator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='iid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='mcontains',
            name='cid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='meals',
            name='Creator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='meals',
            name='mid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='rcontains',
            name='cid2',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='recipes',
            name='Creator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recipes',
            name='rid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='mcontains',
            name='MID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='New.Meals'),
        ),
        migrations.AlterField(
            model_name='rcontains',
            name='RID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='New.Recipes'),
        ),
        migrations.RemoveField(
             model_name='ingredient',
             name='CreatorID',
        ),
         migrations.RemoveField(
             model_name='ingredient',
             name='IID',
        ),
        migrations.RemoveField(
             model_name='meals',
             name='MID',
        ),
        migrations.RemoveField(
             model_name='recipes',
             name='CreatorID',
        ),
        migrations.RemoveField(
             model_name='recipes',
             name='RID',
        ),
    ]
