# Generated by Django 4.2 on 2024-03-06 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('working_day', models.PositiveIntegerField(default=22)),
                ('phone', models.CharField(max_length=13)),
                ('payment', models.BooleanField(default=True)),
                ('data', models.DateField(auto_now_add=True)),
                ('chief', models.BooleanField(default=False)),
                ('token_id', models.CharField(blank=True, max_length=10)),
                ('token_code', models.CharField(blank=True, max_length=10)),
                ('payment_summa', models.CharField(blank=True, max_length=15, verbose_name='oylik tolov')),
                ('balans_summa', models.IntegerField(default=0, verbose_name='balans summa')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
                ('phone', models.CharField(blank=True, max_length=13, null=True)),
                ('active', models.BooleanField(default=True)),
                ('day_summa', models.BooleanField(default=False)),
                ('checked', models.BooleanField(default=False)),
                ('total_summa', models.PositiveIntegerField(default=0, verbose_name='tolash kerak bolgan summa')),
                ('chief', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chiefs', to='main.client')),
                ('educator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educators', to='main.client')),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chief', models.CharField(max_length=30, verbose_name='chief nameni saqlaydi ')),
                ('educator', models.CharField(max_length=30, verbose_name=' educator nameni saqlaydi ')),
                ('text', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('summa', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=55, verbose_name='tolovni kim oldi ')),
                ('date', models.DateField(auto_now_add=True)),
                ('summa', models.PositiveIntegerField(default=0, verbose_name='tolangan summa')),
                ('chief_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cpayment_chiefs', to='main.client')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_customers', to='main.customer')),
                ('educator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_educators', to='main.client')),
            ],
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField(auto_now_add=True)),
                ('came_and_went', models.TextField(blank=True)),
                ('summa', models.PositiveIntegerField(default=0, verbose_name='Bolani  bergan summa')),
                ('cost_summa', models.PositiveIntegerField(default=0, verbose_name='chqim summasi')),
                ('total_summa', models.PositiveIntegerField(default=0, verbose_name='chief va educator Toplangan summa bolani berishi kerak bolgan summa ')),
                ('chief', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='months_chiefs', to='main.client')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='months_customers', to='main.customer')),
                ('educator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='months_educators', to='main.client')),
            ],
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55, verbose_name='kim chiqim qilgan ')),
                ('summa', models.PositiveIntegerField()),
                ('text', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('chief', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cost_chiefs', to='main.client')),
                ('educator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cost_educators', to='main.client')),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cost_months', to='main.month')),
            ],
        ),
    ]