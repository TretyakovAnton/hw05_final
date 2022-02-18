# Generated by Django 2.2.9 on 2022-01-10 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20211228_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, default=django.db.models.deletion.SET_NULL, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='posts.Group'),
        ),
    ]
