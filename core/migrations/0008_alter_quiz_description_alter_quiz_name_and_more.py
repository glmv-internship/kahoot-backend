# Generated by Django 5.0.8 on 2024-08-14 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_game_userresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='name',
            field=models.CharField(default='quiz_name', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='uid',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]