# Generated by Django 4.1.7 on 2024-05-04 07:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resume_builder', '0006_templatesinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume_file', models.FileField(upload_to='resumes/')),
                ('template_id', models.CharField(default='0', max_length=50)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Extracted_ResumeDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_id', models.CharField(default='0', max_length=50)),
                ('summary', models.CharField(default='Add Your Summry', max_length=5000)),
                ('skills', models.CharField(default='Add Your Skills', max_length=5000)),
                ('projects', models.CharField(default='Add Your projects', max_length=5000)),
                ('languages', models.CharField(default='Add Your languages', max_length=5000)),
                ('education', models.CharField(default='Add Your education', max_length=5000)),
                ('internship', models.CharField(default='Add Your internship', max_length=5000)),
                ('experience', models.CharField(default='Add Your experience', max_length=5000)),
                ('contact', models.CharField(default='Add Your contact', max_length=5000)),
                ('certifications', models.CharField(default='Add Your certifications', max_length=5000)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Extracted_ExperienceDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_id', models.CharField(default='0', max_length=50)),
                ('company_name', models.CharField(default='Add Your university', max_length=5000)),
                ('designation', models.CharField(default='Add Your Designation', max_length=5000)),
                ('start_date', models.CharField(default='Add Your Start date', max_length=5000)),
                ('end_date', models.CharField(default='Add Your end date', max_length=5000)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Extracted_EducationDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_id', models.CharField(default='0', max_length=50)),
                ('degree', models.CharField(default='Add Your Degree', max_length=5000)),
                ('university', models.CharField(default='Add Your university', max_length=5000)),
                ('year_of_passing', models.CharField(default='Add Your year of passing', max_length=5000)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]