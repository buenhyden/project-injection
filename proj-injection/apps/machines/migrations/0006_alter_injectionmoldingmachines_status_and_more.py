# Generated by Django 5.1.2 on 2024-10-13 17:57

from django.db import migrations, models


def create_initial_data(apps, schema_editor):
    InjectionMoldingMachines = apps.get_model("machines", "InjectionMoldingMachines")
    InjectionMoldingMachines.objects.create(name="test1", location="test-1", owner_id=1)
    InjectionMoldingMachines.objects.create(name="test2", location="test-2", owner_id=1)
    InjectionMoldingMachines.objects.create(name="test3", location="test-3", owner_id=2)
    InjectionMoldingMachines.objects.create(name="test4", location="test-4", owner_id=2)
    InjectionMoldingMachines.objects.create(name="test5", location="test-5", owner_id=2)
    InjectionMoldingMachines.objects.create(name="test6", location="test-6", owner_id=2)


class Migration(migrations.Migration):
    """app(machines) Database Migration."""

    dependencies = [
        ("machines", "0005_alter_injectionmoldingmachines_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="injectionmoldingmachines",
            name="status",
            field=models.SmallIntegerField(
                choices=[
                    (0, "POWEROFF"),
                    (1, "READY"),
                    (2, "RUNNING"),
                    (3, "PENDING"),
                    (4, "ERROR"),
                ],
                default=1,
            ),
        ),
        migrations.AlterField(
            model_name="machineshistory",
            name="result",
            field=models.SmallIntegerField(
                choices=[
                    (1, "SUCCESS"),
                    (2, "REMOTEFAILED"),
                    (3, "INTERNALFAILED"),
                    (4, "PENDING"),
                    (5, "PERMISSIONDENIED"),
                ]
            ),
        ),
        migrations.RunPython(create_initial_data),
    ]
