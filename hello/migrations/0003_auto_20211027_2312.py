# Generated by Django 3.2.8 on 2021-10-27 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_auto_20211027_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='stuff',
            name='qr_url',
            field=models.CharField(max_length=250, null=True, verbose_name='Вакцина'),
        ),
        migrations.AlterField(
            model_name='stuff',
            name='doc',
            field=models.CharField(max_length=20, verbose_name='Документ'),
        ),
        migrations.AlterField(
            model_name='stuff',
            name='status',
            field=models.CharField(max_length=1, verbose_name='С'),
        ),
    ]
