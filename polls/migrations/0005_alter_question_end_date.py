# Generated by Django 4.1.1 on 2022-09-20 10:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0004_alter_question_end_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="end_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2022, 9, 20, 10, 0, 31, 819487, tzinfo=datetime.timezone.utc
                ),
                null=True,
                verbose_name="end date",
            ),
        ),
    ]
