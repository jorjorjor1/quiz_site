# Generated by Django 2.2.1 on 2019-09-17 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20190917_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='quiz_questions',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='questions.Quiz'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='score',
            name='value',
            field=models.IntegerField(default=0, verbose_name='Ценность вопроса'),
            preserve_default=False,
        ),
    ]
