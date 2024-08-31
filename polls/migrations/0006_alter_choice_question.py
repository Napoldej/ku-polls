# Generated by Django 5.1 on 2024-08-31 15:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0005_alter_question_pub_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="choice",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="choices",
                to="polls.question",
            ),
        ),
    ]
