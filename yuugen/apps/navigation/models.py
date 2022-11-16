import os
from io import BytesIO
from PIL import Image

from django.conf import settings
from django.core.files import File
from django.db import models
from django.utils.translation import gettext_lazy as _

from yuugen.apps.users.models import User
from yuugen.apps.inventory.models import ProductDetail

class ThemeTag(models.Model):
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, related_name='ttag_creator')
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='ttag_editor', null=True)
    ttag = models.CharField(
        _('Theme Tag'),
        max_length=254, 
        unique=True,
        blank=False, 
        )
    tslug = models.SlugField()
    
    def __str__(self):
        return self.ttag


class CatalogTag(models.Model):
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, related_name='ctag_creator')
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='ctag_editor',null=True)
    ctag = models.CharField(
        _('Catalog Tag'),
        max_length=254,
        unique=True,
        blank=False,
        )
    cimg = models.ImageField(_('Catalog Image'), upload_to='img', blank=True, unique=False, max_length=254)    
    cslug = models.SlugField()

    def __str__(self):
        return self.ctag


class OperationTag(models.Model):
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, related_name='otag_creator')
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='otag_editor',null=True)
    otag = models.CharField(
        _('Operation Tag'),
        max_length=254, 
        unique=True, 
        blank=False,
        )
    oimg = models.ImageField(_('Catalog Image'), upload_to='img', blank=True, unique=False, max_length=254) 
    oslug = models.SlugField()
    
    def __str__(self):
        return self.otag

class Product(models.Model):
    '''
    Model that provide Table for Product Detail
    '''
    designation = models.CharField(_("name"), max_length=100, unique=True, blank=False)
    slug = models.SlugField(_("slug"), max_length=50, unique=True, blank=False)
    description = models.TextField(_("description"), blank=True)
    ctag = models.ForeignKey(CatalogTag, on_delete=models.PROTECT, related_name='product_catalog_tag')
    ttag = models.ForeignKey(ThemeTag, on_delete=models.PROTECT, related_name='product_theme_tag')
    otag = models.ForeignKey(OperationTag, on_delete=models.PROTECT, related_name='product_operation_tag')
    SKU = models.ForeignKey(ProductDetail, on_delete=models.PROTECT, blank=False, null=False, related_name="product_sku")
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, related_name='product_creator')
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='product_editor',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta():
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.designation


class ProductImage(models.Model):
    """
    Models that provide Table for Product Images
    """
    SKU = models.ForeignKey(ProductDetail, on_delete= models.CASCADE, related_name='image_sku')
    img = models.ImageField(_('image'), upload_to='img', blank=False, unique=False, max_length=254)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, related_name='image_creator')
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='image_editor',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def get_image(self):
        if self.image:
            return str(BASE_URL + self.image.url)
        return ""

class NewsLetter(models.Model):
    """
    add the capacity to grab email through a newsletter form navigation or markecting apps is yet to be define
    """
    email = models.EmailField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)


class FlatPage(models.Model):
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    title = models.CharField(_('title'), max_length=200, blank=False)
    content = models.TextField(_('content'), blank=False)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, related_name='page_creator')
    modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='page_editor', null=True)
    is_active = models.BooleanField(default=True)


    class Meta:
        verbose_name = _('Flat page')
        verbose_name_plural = _('Flat pages')
        ordering = ['url']

    def __str__(self):
        return "%s -- %s" % (self.url, self.title)
