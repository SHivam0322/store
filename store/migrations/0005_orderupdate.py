# Generated by Django 2.2.13 on 2021-06-25 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_orders'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderUpdate',
            fields=[
                ('update_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_id', models.IntegerField(default='')),
                ('update_desc', models.CharField(max_length=5000)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
