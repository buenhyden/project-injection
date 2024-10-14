# Generated by Django 5.1.2 on 2024-10-13 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0002_alter_injectionmoldingmachines_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='injectionmoldingmachines',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'POWEROFF'), (1, 'READY'), (2, 'RUNNING'), (3, 'PENDING'), (4, 'PAUSE'), (5, 'ERROR')], default=1),
        ),
        migrations.CreateModel(
            name='MachinesHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_datetime', models.DateTimeField()),
                ('command', models.CharField(max_length=64)),
                ('worker', models.BigIntegerField()),
                ('machine_id', models.BigIntegerField()),
                ('machine_owner_id', models.BigIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'machines_history',
                'indexes': [models.Index(fields=['machine_id', 'machine_owner_id'], name='mo-index')],
            },
        ),
    ]
