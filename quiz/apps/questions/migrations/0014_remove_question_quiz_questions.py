# Generated by Django 2.2.6 on 2019-10-09 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0013_auto_20191009_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='quiz_questions',
        ),
    ]
