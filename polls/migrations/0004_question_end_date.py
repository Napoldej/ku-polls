# Generated by Django 5.1 on 2024-08-30 15:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0003_rename_question_text_choice_question"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="end_date",
            field=models.DateTimeField(null=True, verbose_name="date ended"),
        ),
    ]
