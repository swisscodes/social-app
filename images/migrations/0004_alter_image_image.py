# Generated by Django 3.2.3 on 2021-06-02 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_auto_20210602_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='media/%Y/%m/%d/'),
        ),
    ]