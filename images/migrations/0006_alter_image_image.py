# Generated by Django 3.2.3 on 2021-06-02 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0005_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='media/images/%Y/%m/%d/'),
        ),
    ]
