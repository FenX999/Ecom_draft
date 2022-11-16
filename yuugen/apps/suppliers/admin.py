from django.contrib import admin
from .models import (
    Supplier,
    SupplierOfficeContact,
    SupplierOfficeDetail,
    SupplierWarehouseContact,
    SupplierWarehouseDetail,
    SupplierBankDetail,
)


@admin.register(
    Supplier,
    SupplierOfficeContact,
    SupplierOfficeDetail,
    SupplierWarehouseContact,
    SupplierWarehouseDetail,
    SupplierBankDetail,   
)


class SupplierOfficeDetailAdmin(admin.ModelAdmin):
    pass

class SupplierOfficeContactAdmin(admin.ModelAdmin):
    pass

class SupplierBankDetailAdmin(admin.ModelAdmin):
    pass

class SupplierWarehouseDetailAdmin(admin.ModelAdmin):
    pass

class SupplierWarehouseContactAdmin(admin.ModelAdmin):
    pass

class SupplierAdmin(admin.ModelAdmin):
    pass
