# Generated by Django 3.0.8 on 2020-07-15 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0006_registry_updates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registry',
            name='alt_acy',
            field=models.CharField(blank=True, max_length=300, verbose_name='Altitude Accuracy'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='alt_method',
            field=models.CharField(blank=True, max_length=300, verbose_name='Altitude Method'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='alt_va',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True, verbose_name='Altitude'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='dec_lat_va',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True, verbose_name='Latitude(decimal degrees)'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='dec_long_va',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True, verbose_name='Longitude(decimal degrees)'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='display_flag',
            field=models.BooleanField(default=False, verbose_name='Display Site?'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='horz_acy',
            field=models.CharField(blank=True, max_length=300, verbose_name='Lat/Long Accuracy'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='horz_method',
            field=models.CharField(blank=True, max_length=300, verbose_name='Lat/Long Method'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='nat_aqfr',
            field=models.ForeignKey(blank=True, db_column='nat_aqfr_cd', null=True, on_delete=django.db.models.deletion.PROTECT, to='registry.NatAqfrLookup', to_field='nat_aqfr_cd', verbose_name='National Aquifer'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='qw_baseline_flag',
            field=models.BooleanField(default=False, verbose_name='QW Baseline?'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='qw_network_name',
            field=models.CharField(blank=True, db_column='qw_sys_name', max_length=50, verbose_name='QW Network Name'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='qw_sn_flag',
            field=models.BooleanField(default=False, verbose_name='In QW Sub-Network?'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='qw_well_chars',
            field=models.CharField(blank=True, choices=[('1', 'Background'), ('2', 'Suspected/Anticipated Changes'), ('3', 'Known Changes')], max_length=3, verbose_name='QW Well Characteristics'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='qw_well_purpose',
            field=models.CharField(blank=True, choices=[('1', 'Dedicated Monitoring/Observation'), ('2', 'Other')], max_length=15, verbose_name='QW Well Purpose'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='qw_well_purpose_notes',
            field=models.CharField(blank=True, max_length=4000, verbose_name='QW Well Purpose Notes'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='qw_well_type',
            field=models.CharField(blank=True, choices=[('1', 'Surveillance'), ('2', 'Trend'), ('3', 'Special')], max_length=3, verbose_name='QW Well Type'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='wl_baseline_flag',
            field=models.BooleanField(default=False, verbose_name='WL Baseline?'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='wl_network_name',
            field=models.CharField(blank=True, db_column='wl_sys_name', max_length=50, verbose_name='WL Network Name'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='wl_sn_flag',
            field=models.BooleanField(default=False, verbose_name='In WL Sub-Network?'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='wl_well_chars',
            field=models.CharField(blank=True, choices=[('1', 'Background'), ('2', 'Suspected/Anticipated Changes'), ('3', 'Known Changes')], max_length=3, verbose_name='WL Well Characteristics'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='wl_well_purpose',
            field=models.CharField(blank=True, choices=[('1', 'Dedicated Monitoring/Observation'), ('2', 'Other')], max_length=15, verbose_name='WL Well Purpose'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='wl_well_purpose_notes',
            field=models.CharField(blank=True, max_length=4000, verbose_name='WL Well Purpose Notes'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='wl_well_type',
            field=models.CharField(blank=True, choices=[('1', 'Surveillance'), ('2', 'Trend'), ('3', 'Special')], max_length=3, verbose_name='WL Well Type'),
        ),
    ]
