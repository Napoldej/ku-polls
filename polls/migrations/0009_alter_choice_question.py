# Generated by Django 5.1 on 2024-08-31 15:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0008_alter_choice_question"),
    ]

    operations = [
        migrations.AlterField(
            model_name="choice",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="polls.question"
            ),
        ),
    ]
