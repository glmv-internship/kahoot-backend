# Generated by Django 5.0.8 on 2024-08-08 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_question_quiz_description_quiz_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='number_of_questions',
            field=models.IntegerField(default=0),
        ),
    ]
