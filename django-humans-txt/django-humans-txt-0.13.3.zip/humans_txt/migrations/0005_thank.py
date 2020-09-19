# -*- coding: utf-8 -*-

# django-humans-txt
# humans_txt/migrations/0005_thank.py

# Generated by Django 2.1.1 on 2018-09-29 18:30


from typing import List, Tuple  # pylint: disable=W0611

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("humans_txt", "0004_software")]  # type: List[Tuple[str, str]]

    operations = [
        migrations.CreateModel(
            name="Thank",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        max_length=256,
                        verbose_name="thank to person or organization name",
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        blank=True,
                        db_index=True,
                        max_length=256,
                        null=True,
                        verbose_name="thank to person or organization site URL",
                    ),
                ),
            ],
            options={
                "verbose_name": "thank",
                "verbose_name_plural": "thanks",
                "ordering": ["name"],
            },
        )
    ]  # type: List[migrations.CreateModel]
