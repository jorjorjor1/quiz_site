# Generated by Django 2.2.6 on 2019-10-09 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0014_remove_question_quiz_questions'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='questions.Quiz'),
            preserve_default=False,
        ),
    ]