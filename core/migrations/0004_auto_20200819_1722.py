# Generated by Django 3.1 on 2020-08-19 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_event_in_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='musician',
            name='cashapp_name',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='musician',
            name='cashapp_qr',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='musician',
            name='paypal_donation_url',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='musician',
            name='paypal_qr',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='musician',
            name='venmo_qr',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
