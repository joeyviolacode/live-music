# Generated by Django 3.1 on 2020-08-20 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200820_0124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musician',
            name='cashapp_qr',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='musician',
            name='paypal_qr',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='musician',
            name='venmo_qr',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
