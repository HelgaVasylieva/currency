# Generated by Django 4.0.6 on 2022-09-23 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0007_source_code_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='logo',
            field=models.FileField(default='', upload_to=''),
            preserve_default=False,
        ),
    ]
