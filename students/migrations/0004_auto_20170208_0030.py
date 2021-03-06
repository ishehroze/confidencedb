# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 18:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20170207_2318'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='department',
            field=models.ForeignKey(default='Other', on_delete=django.db.models.deletion.CASCADE, to='students.Department'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='blood_group',
            field=models.CharField(blank=True, choices=[('Positive (+ve)', (('o+', 'O+'), ('a+', 'A+'), ('b+', 'B+'), ('ab+', 'AB+'))), ('Negetive (-ve)', (('o-', 'O-'), ('a-', 'A-'), ('b-', 'B-'), ('ab-', 'AB-')))], max_length=3),
        ),
        migrations.AlterField(
            model_name='student',
            name='father_name',
            field=models.CharField(blank=True, max_length=30, verbose_name="father's name"),
        ),
        migrations.AlterField(
            model_name='student',
            name='is_assistive',
            field=models.BooleanField(verbose_name='assistive?'),
        ),
        migrations.AlterField(
            model_name='student',
            name='is_problematic',
            field=models.BooleanField(verbose_name='problematic?'),
        ),
        migrations.AlterField(
            model_name='student',
            name='is_prospective',
            field=models.BooleanField(verbose_name='prospective?'),
        ),
        migrations.AlterField(
            model_name='student',
            name='mother_name',
            field=models.CharField(blank=True, max_length=30, verbose_name="mother's name"),
        ),
        migrations.AlterField(
            model_name='test',
            name='test_description',
            field=models.TextField(blank=True),
        ),
    ]
