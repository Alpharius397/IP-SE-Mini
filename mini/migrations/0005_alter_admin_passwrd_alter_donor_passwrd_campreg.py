# Generated by Django 5.0.7 on 2024-10-08 15:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini', '0004_alter_admin_passwrd_alter_donor_passwrd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='passwrd',
            field=models.CharField(default='pbkdf2_sha256$720000$pzgE6KQTc9J0EuAzPqgtz3$LnAl1fpULp3xRP4vEkjMtChGq1blarS9CHbMi+8aVaY=', max_length=225),
        ),
        migrations.AlterField(
            model_name='donor',
            name='passwrd',
            field=models.CharField(default='pbkdf2_sha256$720000$w87YEEiqthT5JuDwxPB3wN$G5Owg9JfOBBMxj7cESBNo2jzKBe3IOsTnI7/zyA07q0=', max_length=225),
        ),
        migrations.CreateModel(
            name='CampReg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('camp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mini.camp')),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mini.donor')),
            ],
        ),
    ]
