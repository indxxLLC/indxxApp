# Generated by Django 2.1.8 on 2019-07-17 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190705_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='registerindex',
            name='QC_Date',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='registerindex',
            name='QC_Date_review',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='ruleslist',
            name='qc_rule',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='ruleslist',
            name='qc_rule_review',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='registerindex',
            name='backtest_comp_date',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='registerindex',
            name='etf_launch_date',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='registerindex',
            name='live_date',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
