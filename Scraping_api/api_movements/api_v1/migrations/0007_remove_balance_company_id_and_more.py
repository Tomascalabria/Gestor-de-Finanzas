# Generated by Django 4.1.4 on 2023-06-08 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0006_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='balance',
            name='company_id',
        ),
        migrations.RemoveField(
            model_name='buysellmovement',
            name='company_id',
        ),
        migrations.RemoveField(
            model_name='cocoscredentials',
            name='company_id',
        ),
        migrations.RemoveField(
            model_name='depositextractionmovement',
            name='company_id',
        ),
        migrations.RemoveField(
            model_name='holding',
            name='company_id',
        ),
        migrations.RemoveField(
            model_name='iolcredentials',
            name='company_id',
        ),
        migrations.AddField(
            model_name='balance',
            name='company',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='api_v1.company'),
        ),
        migrations.AddField(
            model_name='buysellmovement',
            name='company',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='api_v1.company'),
        ),
        migrations.AddField(
            model_name='cocoscredentials',
            name='company',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='api_v1.company'),
        ),
        migrations.AddField(
            model_name='depositextractionmovement',
            name='company',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='api_v1.company'),
        ),
        migrations.AddField(
            model_name='holding',
            name='company',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='api_v1.company'),
        ),
        migrations.AddField(
            model_name='iolcredentials',
            name='company',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='api_v1.company'),
        ),
    ]
