# Generated by Django 4.2 on 2023-04-13 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagen',
            name='doc',
            field=models.FileField(null=True, upload_to='docs'),
        ),
        migrations.AlterField(
            model_name='imagen',
            name='img',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]