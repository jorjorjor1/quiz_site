# Generated by Django 2.2.1 on 2019-09-15 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=500, verbose_name='Текст вопроса')),
                ('variant_1', models.CharField(max_length=200, verbose_name='Вариант 1')),
                ('variant_2', models.CharField(max_length=200, verbose_name='Вариант 2')),
                ('variant_3', models.CharField(max_length=200, verbose_name='Вариант 3')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]