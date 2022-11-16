# Generated by Django 3.2 on 2022-10-05 11:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('url_creation', models.CharField(blank=True, max_length=20)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Super User Accreditation')),
                ('is_manager', models.BooleanField(default=False, verbose_name='Manager Accreditation')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff Accreditation')),
                ('is_customer', models.BooleanField(default=True, verbose_name='Customer Accreditation')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active Status')),
                ('created_by', models.CharField(default=1, max_length=1)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('groups', models.ManyToManyField(to='auth.Group', verbose_name='Accreditation')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='EmployeePayDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(blank=True, max_length=45, null=True, verbose_name='Bank')),
                ('BIC', models.CharField(blank=True, max_length=45, null=True, verbose_name='BIC')),
                ('IBAN', models.CharField(blank=True, max_length=45, null=True, verbose_name='IBAN')),
                ('SWIFT', models.CharField(blank=True, max_length=45, null=True, verbose_name='SWFIT')),
                ('protocol', models.CharField(blank=True, max_length=45, null=True, verbose_name='Blockchain Protocol')),
                ('wallet_address', models.CharField(blank=True, max_length=45, null=True, verbose_name='Wallet Address')),
                ('created_by', models.CharField(max_length=1, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employe_bank_detail', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Employee pay details',
                'verbose_name_plural': 'Employess pay details',
            },
        ),
        migrations.CreateModel(
            name='EmployeeDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peronnal_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('entry_date', models.DateField()),
                ('departure_date', models.DateField(blank=True, null=True)),
                ('fname', models.CharField(help_text='First Name of the employee', max_length=150, verbose_name='First Name')),
                ('lname', models.CharField(help_text='Last Name o the employee', max_length=150, verbose_name='Last Name')),
                ('address_1', models.CharField(blank=True, help_text='employee address information', max_length=150, verbose_name='Address Line 1')),
                ('address_2', models.CharField(blank=True, help_text='for complementary info if needed', max_length=150, verbose_name='Address Line 2 ')),
                ('zip_code', models.CharField(blank=True, help_text=' Employee Zip code', max_length=150, verbose_name='Zip code')),
                ('city', models.CharField(blank=True, help_text='Employee City name', max_length=150, verbose_name='City Name')),
                ('states', models.CharField(blank=True, help_text='Employee States or Region', max_length=150, verbose_name='States')),
                ('country', models.CharField(blank=True, help_text='Employee Country', max_length=150, verbose_name='Country')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employee_creator', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_created_email', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Employee Details',
                'verbose_name_plural': 'Employees Details',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='CustomerShippingDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('same_as_billing', models.BooleanField(default=False)),
                ('fname', models.CharField(blank=True, help_text='First Name', max_length=150, verbose_name='First Name')),
                ('lname', models.CharField(blank=True, help_text='Last Name', max_length=150, verbose_name='Last Name')),
                ('address_1', models.CharField(blank=True, help_text='Your address information here', max_length=150, verbose_name='Address Line 1')),
                ('address_2', models.CharField(blank=True, help_text='for complementary info if needed', max_length=150, verbose_name='Address Line 2 ')),
                ('zip_code', models.CharField(blank=True, help_text='Zip code', max_length=150, verbose_name='Zip code')),
                ('city', models.CharField(blank=True, help_text='City name', max_length=150, verbose_name='City Name')),
                ('states', models.CharField(blank=True, help_text='States or Region', max_length=150, verbose_name='States')),
                ('country', models.CharField(blank=True, help_text='Country', max_length=150, verbose_name='Country')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer Shipping Details',
                'verbose_name_plural': 'Customers Shipping Details',
            },
        ),
        migrations.CreateModel(
            name='CustomerMarketingDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_letter', models.BooleanField(default=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer Marketing',
                'verbose_name_plural': 'Customers Marketting',
            },
        ),
        migrations.CreateModel(
            name='CustomerBillingDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(help_text='First Name', max_length=150, verbose_name='First Name')),
                ('lname', models.CharField(help_text='Last Name', max_length=150, verbose_name='Last Name')),
                ('address_1', models.CharField(help_text='Your address information here', max_length=150, verbose_name='Address Line 1')),
                ('address_2', models.CharField(help_text='for complementary info if needed', max_length=150, null=True, verbose_name='Address Line 2 ')),
                ('zip_code', models.CharField(help_text='Zip code', max_length=150, verbose_name='Zip code')),
                ('city', models.CharField(help_text='City name', max_length=150, verbose_name='City Name')),
                ('states', models.CharField(help_text='States or Region', max_length=150, verbose_name='States')),
                ('country', models.CharField(help_text='Country', max_length=150, verbose_name='Country')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer Billing Details',
                'verbose_name_plural': 'Customers Billing Details',
            },
        ),
    ]
