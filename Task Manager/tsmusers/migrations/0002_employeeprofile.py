# Generated by Django 4.2.16 on 2024-11-22 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tsmusers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('role', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=15)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='tsmusers.employee')),
            ],
        ),
    ]
