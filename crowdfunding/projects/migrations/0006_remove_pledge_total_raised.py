# Generated by Django 3.0.8 on 2020-09-26 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_pledge_total_raised'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pledge',
            name='total_raised',
        ),
    ]
