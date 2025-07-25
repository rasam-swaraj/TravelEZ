# Generated by Django 4.2 on 2025-06-24 06:54

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passengers', models.IntegerField()),
                ('totalprice', models.FloatField()),
                ('booking_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'booking_info',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('country', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'client_info',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
                ('package_code', models.CharField(max_length=20)),
                ('package_name', models.CharField(max_length=50)),
                ('package_type', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('days', models.IntegerField()),
                ('description', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('slug', models.SlugField(default='')),
            ],
            options={
                'db_table': 'package_info',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=150)),
                ('amount_paid', models.CharField(max_length=150)),
                ('status', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('booking_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travelapp.booking')),
                ('clientid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travelapp.client')),
            ],
            options={
                'db_table': 'payment_info',
            },
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=30)),
                ('pincode', models.IntegerField()),
                ('passport_id', models.IntegerField()),
                ('journey_date', models.DateField()),
                ('booking_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travelapp.booking')),
            ],
            options={
                'db_table': 'passanger_info',
            },
        ),
        migrations.AddField(
            model_name='booking',
            name='clientid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travelapp.client'),
        ),
        migrations.AddField(
            model_name='booking',
            name='packageid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travelapp.package'),
        ),
    ]
