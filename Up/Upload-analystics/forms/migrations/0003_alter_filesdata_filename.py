# Generated by Django 5.0.2 on 2024-03-04 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0002_rename_filedata_filesdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filesdata',
            name='filename',
            field=models.CharField(max_length=100),
        ),
    ]
