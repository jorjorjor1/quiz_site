# Generated by Django 2.2.6 on 2019-10-09 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0012_auto_20191009_1021'),
    ]

    operations = [
        migrations.RenameField(
            model_name='score',
            old_name='question_id',
            new_name='question',
        ),
        migrations.RenameField(
            model_name='score',
            old_name='user_id',
            new_name='user',
        ),
    ]
