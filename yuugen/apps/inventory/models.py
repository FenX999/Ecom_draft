from django.db import models
from django.utils.translation import gettext_lazy as _

from yuugen.apps.users.models import User

class ProductDetail(models.Model):
    is_active = models.BooleanField(default=True)
    SKU = models.CharField(_('Inventory Designation'),
        primary_key=True,
        max_length=255,
        unique=True,
        blank=False,
    )
    # UPC = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='detail_creator')
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='detail_editor', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.SKU


class Size(models.Model):
    value = models.CharField(_('Characteristics designation of a product'),max_length=24, unique=True, blank=False)

    def __str__(self):
        return self.value

class Finition(models.Model):
    value = models.CharField(_('Characteristics designation of a product'),max_length=24, unique=True, blank=False)

    def __str__(self):
        return self.value

class Stock(models.Model):
    SKU = models.ForeignKey(
        ProductDetail,
        on_delete=models.CASCADE,
        related_name='stock_sku',
    )
    unit = models.IntegerField(_('Units'),default=0, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='stock_creator')
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='stock_ediito', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    def __str__(self):
        return self.SKU_detail_id


class SizeIndex(models.Model):
    SKU = models.ForeignKey(ProductDetail, 
        on_delete=models.CASCADE,
        related_name='size_sku',
    )
    size = models.ManyToManyField(Size)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='size_creator')
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='size_editor', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.SKU_detail_id


class FinitionIndex(models.Model):
    SKU = models.ForeignKey(ProductDetail, 
        on_delete=models.CASCADE,
        related_name='finition_sku',
        )
    finition = models.ManyToManyField(Finition)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='finition_creator')
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='finition_editor' ,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.SKU_detail_id


class DetailWeight(models.Model):
    SKU = models.ForeignKey(ProductDetail, 
        on_delete=models.CASCADE,
        related_name='weight_sku',
        )
    weight_kg = models.DecimalField(_('Weight in Kilogramms'), max_digits=9, decimal_places=2, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='weight_creator')
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='weight_editor', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    def __str__(self):
        return self.SKU_detail_id


class DetailVolume(models.Model):
    SKU = models.ForeignKey(ProductDetail,
    on_delete=models.CASCADE,
    related_name='volume_sku',
    )
    volume_m3 = models.DecimalField(_('Volume of the delivered Parcel'),
        blank=False,
        max_digits=9,
        decimal_places=2,
        help_text='Volume in m3 of the parcel if needed upon Shipping rate'
    )
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='volume_creator')
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='volume_editor', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    def __str__(self):
        return self.SKU_detail_id


class RetailPrice(models.Model):
    SKU = models.ForeignKey(ProductDetail, 
    on_delete=models.CASCADE,
    related_name='retail_price_sku',
    )
    public_price = models.DecimalField(_('Retail Price'), max_digits=11, decimal_places=2, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='retail_price_creator')
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='retail_price_editor', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    def __str__(self):
        return self.SKU_detail_id


class PublicPrice(models.Model):
    SKU = models.ForeignKey(ProductDetail, 
    on_delete=models.CASCADE,
    related_name='public_price_sku',
    )
    public_price = models.DecimalField(_('Public Price'), max_digits=11, decimal_places=2, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='public_price_creator')
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='public_price_editor', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    def __str__(self):
        return self.SKU_id
