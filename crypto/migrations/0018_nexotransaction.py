# Generated by Django 3.2.5 on 2022-05-06 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0017_alter_cryptocomapptransaction_kind'),
    ]

    operations = [
        migrations.CreateModel(
            name='NexoTransaction',
            fields=[
                ('log_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='crypto.log')),
            ],
            bases=('crypto.log',),
        ),
    ]
