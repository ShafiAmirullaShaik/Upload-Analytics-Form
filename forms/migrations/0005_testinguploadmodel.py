# Generated by Django 5.0.2 on 2024-03-04 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0004_filedata_delete_filesdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='testingUploadModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataSource', models.CharField(max_length=255)),
                ('filename', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('filePath', models.TextField()),
            ],
        ),
    ]
