from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import (
    User, 
    EmployeeDetail, 
    EmployeePayDetail,
    CustomerShippingDetail,
    CustomerBillingDetail,
    CustomerMarketingDetail,
)

from .forms import(
    UserChangeForm,
    UserCreationForm,
    EmployeeDetailForm,
    EmployeePayDetailForm,
    CustomerShippingForm,
    CustomerBillingForm,
    CustomerMarketingForm,
)

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display=  ('email', 'last_login', 'is_active', "is_superuser", "is_manager", "is_staff", "is_customer", )
    list_filter =  ('is_active', "is_superuser", "is_manager", "is_staff", "is_customer")
    fieldsets = (
        (None, {"fields": ('email', 'password',)}),
        ('Accreditations',{'fields': ("is_superuser", "is_manager", "is_staff", "is_customer",)}),
        ('Permissions', {'fields': ('groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('created_by','email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email' ,)
    ordering = ('email',)

admin.site.register(User, UserAdmin)

class EmployeeDetailAdmin(admin.ModelAdmin):
    form = EmployeeDetailForm
    list_display = ('lname', 'fname', 'email', )

admin.site.register(EmployeeDetail, EmployeeDetailAdmin)

class EmployeePayDetailAdmin(admin.ModelAdmin):
    form = EmployeePayDetailForm
    list_display = ( 'email', )

admin.site.register(EmployeePayDetail, EmployeePayDetailAdmin)

class CustomerShippingDetailAdmin(admin.ModelAdmin):
    form = CustomerShippingForm
    list_display = ('email',)

admin.site.register(CustomerShippingDetail, CustomerShippingDetailAdmin)

class CustomerBillingDetailAdmin(admin.ModelAdmin):
    form = CustomerBillingForm
    list_display = ('email',)

admin.site.register(CustomerBillingDetail, CustomerBillingDetailAdmin)

class CustomerMarketingDetailAdmin(admin.ModelAdmin):
    form = CustomerMarketingForm
    list_display = ('email', )

admin.site.register(CustomerMarketingDetail, CustomerMarketingDetailAdmin)