# Generated by Django 4.1.4 on 2023-06-17 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0009_remove_company_logo_company_logo_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='logo_url',
            new_name='logo',
        ),
    ]