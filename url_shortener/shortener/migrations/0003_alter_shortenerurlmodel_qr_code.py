# Generated by Django 4.2.6 on 2024-03-19 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0002_alter_shortenerurlmodel_short_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortenerurlmodel',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='E:\\Top-academy\\2 семестр\\Группа 323\\Homework\\Django\\djprojects\\url_shortener/media', verbose_name='QR-код'),
        ),
    ]