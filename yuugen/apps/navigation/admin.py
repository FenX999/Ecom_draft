from django.contrib import admin
from .models import (
    Product,
    ProductDetail,
    ProductImage,
    ThemeTag,
    CatalogTag,
    OperationTag,
)

class ThemeTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"tslug": ("ttag",)}

admin.site.register(ThemeTag, ThemeTagAdmin)

class CatalogTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"cslug": ("ctag",)}

admin.site.register(CatalogTag, CatalogTagAdmin)

class OperationTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"oslug": ("otag",)}

admin.site.register(OperationTag, OperationTagAdmin)

class ProductImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(ProductImage, ProductImageAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('designation', 'ttag', 'ctag', 'otag', 'is_active')
    prepopulated_fields = {"slug": ("designation",)}
    
admin.site.register(Product, ProductAdmin)