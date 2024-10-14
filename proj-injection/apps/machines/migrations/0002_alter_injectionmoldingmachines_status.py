# Generated by Django 5.1.2 on 2024-10-12 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='injectionmoldingmachines',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'POWEROFF'), (1, 'READY'), (2, 'RUNNING'), (3, 'PAUSE'), (4, 'FAILURE'), (5, 'ERROR')], default=1),
        ),
    ]