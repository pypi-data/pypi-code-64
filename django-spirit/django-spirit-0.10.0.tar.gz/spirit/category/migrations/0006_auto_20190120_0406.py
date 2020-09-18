# Generated by Django 2.1.5 on 2019-01-20 04:06

from django.db import migrations, models


def reorder(apps, schema_editor):
    Category = apps.get_model("spirit_category", "Category")
    order = 0
    for item in Category.objects.all().order_by('title','pk'):
        order += 1
        item.sort = order
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_category', '0005_category_reindex_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='sort',
            field=models.PositiveIntegerField(default=0, verbose_name='sorting order'),
        ),
        migrations.RunPython(reorder),
    ]
