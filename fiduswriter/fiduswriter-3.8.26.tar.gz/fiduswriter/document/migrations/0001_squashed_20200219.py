# Generated by Django 2.2.9 on 2020-02-19 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import document.models
import uuid


class Migration(migrations.Migration):

    replaces = [('document', '0001_squashed_0032_document_listed'), ('document', '0002_auto_20180814_1946'), ('document', '0003_auto_20181115_0926'), ('document', '0004_documenttemplate'), ('document', '0005_document_template'), ('document', '0006_auto_20190118_1342'), ('document', '0007_auto_20190227_2105'), ('document', '0008_documenttemplate_doc_version'), ('document', '0009_documentrevision_doc_version'), ('document', '0008_auto_20190701_0943'), ('document', '0010_merge_20190701_1737'), ('document', '0011_auto_20190701_1744'), ('document', '0012_auto_20190704_1219'), ('document', '0013_auto_20190808_1126'), ('document', '0014_auto_20190811_1204'), ('document', '0015_auto_20190828_1108'), ('document', '0016_auto_20190829_2147'), ('document', '0017_remove_documenttemplate_citation_styles'), ('document', '0018_documenttemplate_import_id'), ('document', '0019_remove_documenttemplate_definition_hash')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=255)),
                ('definition', models.TextField(default='{}')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('doc_version', models.DecimalField(decimal_places=1, default=3.1, max_digits=3)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('import_id', models.CharField(blank=True, default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=255)),
                ('contents', models.TextField(default='{}')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('last_diffs', models.TextField(default='[]')),
                ('version', models.PositiveIntegerField(default=0)),
                ('comments', models.TextField(default='{}')),
                ('doc_version', models.DecimalField(decimal_places=1, default=3.1, max_digits=3)),
                ('bibliography', models.TextField(default='{}')),
                ('listed', models.BooleanField(default=True)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document.DocumentTemplate')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='AccessRight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rights', models.CharField(choices=[('write', 'Writer'), ('write-tracked', 'Write with tracked changes'), ('comment', 'Commentator'), ('review', 'Reviewer'), ('read', 'Reader'), ('read-without-comments', 'Reader without comment access')], max_length=21)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document.Document')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('document', 'user')},
            },
        ),
        migrations.CreateModel(
            name='AccessRightInvite',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('rights', models.CharField(choices=[('write', 'Writer'), ('write-tracked', 'Write with tracked changes'), ('comment', 'Commentator'), ('review', 'Reviewer'), ('read', 'Reader'), ('read-without-comments', 'Reader without comment access')], max_length=21)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document.Document')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentRevision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(blank=True, default='', max_length=255)),
                ('date', models.DateTimeField(auto_now=True)),
                ('file_object', models.FileField(upload_to=document.models.revision_filename)),
                ('file_name', models.CharField(blank=True, default='', max_length=255)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document.Document')),
                ('doc_version', models.DecimalField(decimal_places=1, default=3.1, max_digits=3)),
            ],
        ),
    ]
