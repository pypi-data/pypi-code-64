# -*- coding: utf-8 -*-

# django-humans-txt
# humans_txt/migrations/0002_standard.py

# Generated by Django 2.1.1 on 2018-09-29 17:23


from typing import List, Tuple  # pylint: disable=W0611

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("humans_txt", "0001_initial")]  # type: List[Tuple[str, str]]

    operations = [
        migrations.CreateModel(
            name="Standard",
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
                        db_index=True, max_length=256, verbose_name="standard name"
                    ),
                ),
            ],
            options={
                "verbose_name": "standard",
                "verbose_name_plural": "standards",
                "ordering": ["name"],
            },
        )
    ]  # type: List[migrations.CreateModel]
