# Generated by Django 4.1.5 on 2023-02-06 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_no', models.CharField(max_length=50)),
                ('max_distance', models.FloatField(max_length=10)),
                ('max_stiffner_distance', models.FloatField(max_length=10)),
                ('edge_distance', models.FloatField(max_length=10)),
                ('stiffner_type', models.CharField(max_length=50)),
                ('sttifner_block', models.CharField(help_text='hi', max_length=50)),
                ('angle_plan_block', models.CharField(help_text='hi', max_length=50)),
                ('material', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=50)),
                ('approved', models.CharField(max_length=50)),
                ('checked', models.CharField(max_length=50)),
                ('client', models.CharField(max_length=50)),
                ('project', models.CharField(max_length=50)),
                ('Creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
                ('Total_area', models.FloatField(blank=True, max_length=10, null=True)),
                ('state', models.CharField(default='1', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=120)),
                ('phone', models.CharField(max_length=50)),
                ('company', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('Total_area', models.FloatField(blank=True, default=0, max_length=30, null=True)),
                ('register_date', models.DateField(auto_now_add=True)),
                ('last_login_date', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=10)),
                ('right', models.FloatField(max_length=30)),
                ('left', models.FloatField(max_length=30)),
                ('down', models.FloatField(max_length=30)),
                ('right_angle', models.FloatField(max_length=30)),
                ('left_angle', models.FloatField(max_length=30)),
                ('down_angle', models.FloatField(max_length=30)),
                ('qty', models.FloatField(max_length=10)),
                ('bend', models.FloatField(max_length=10)),
                ('new_bend', models.FloatField(default=0, max_length=10, null=True)),
                ('bend_top', models.FloatField(default=1, max_length=1, null=True)),
                ('bend_right', models.FloatField(default=1, max_length=1, null=True)),
                ('bend_left', models.FloatField(default=1, max_length=1, null=True)),
                ('bend_down', models.FloatField(default=1, max_length=1, null=True)),
                ('angle_plan_right', models.FloatField(default=1, max_length=1, null=True)),
                ('angle_plan_left', models.FloatField(default=1, max_length=1, null=True)),
                ('angle_plan_down', models.FloatField(default=1, max_length=1, null=True)),
                ('angle_plan_up', models.FloatField(default=1, max_length=1, null=True)),
                ('stiffner_length', models.FloatField(blank=True, max_length=10, null=True)),
                ('stiffner_no', models.FloatField(blank=True, max_length=10, null=True)),
                ('screw', models.FloatField(blank=True, max_length=10, null=True)),
                ('pop_revit', models.FloatField(blank=True, max_length=10, null=True)),
                ('area', models.FloatField(blank=True, max_length=10, null=True)),
                ('Total_area', models.FloatField(blank=True, max_length=10, null=True)),
                ('Creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
                ('state', models.CharField(default='1', max_length=1)),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dxf.job')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dxf.user'),
        ),
    ]
