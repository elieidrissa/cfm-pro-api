# Generated by Django 4.1.7 on 2023-04-06 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cfm_pro_api', '0003_rename_authorization_transporteur_authorisation'),
    ]

    operations = [
        migrations.AddField(
            model_name='transporteur',
            name='sex',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=10, null=True),
        ),
    ]
