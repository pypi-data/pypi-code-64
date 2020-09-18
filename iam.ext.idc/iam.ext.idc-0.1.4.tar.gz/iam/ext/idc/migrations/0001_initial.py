# Generated by Django 3.1.1 on 2020-09-09 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssertedSubject',
            fields=[
                ('lsid', models.BigAutoField(db_column='lsid', editable=False, primary_key=True, serialize=False, verbose_name='Local Subject ID')),
                ('asid', models.CharField(db_column='asid', max_length=254, unique=True, verbose_name='Asserted Identity')),
                ('external', models.BooleanField(db_column='is_external', default=True, verbose_name='External')),
                ('is_superuser', models.BooleanField(db_column='is_superuser', default=False, verbose_name='Superuser')),
            ],
            options={
                'verbose_name': 'Asserted Subject',
                'verbose_name_plural': 'Asserted Subjects',
                'db_table': 'assertedsubjects',
                'default_permissions': [],
            },
        ),
        migrations.AddConstraint(
            model_name='assertedsubject',
            constraint=models.CheckConstraint(check=models.Q(('external', True), ('is_superuser', True), _negated=True), name='assertedsubjects_not_superuser_and_external'),
        ),
    ]
