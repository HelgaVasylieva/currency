# Generated by Django 4.0.6 on 2022-09-06 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0005_remove_rate_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='source',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='currency.source'),
        ),
    ]
