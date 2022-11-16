from django.utils.translation import gettext_lazy as _
from django.db import models

from yuugen.apps.users.models import UserCreation
from yuugen.apps.inventory.models import ProductDetail


class Supplier(models.Model):
    name = models.CharField(_('Supplier'), max_length=255, unique=True)
    created_by = models.ForeignKey(UserCreation, verbose_name=_("Created by"), on_delete=models.PROTECT, related_name='supplier_creator')
    modified_by = models.ForeignKey(UserCreation, on_delete=models.DO_NOTHING, related_name='supplier_editor', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta():
        verbose_name = _('Supplier')
        verbose_name_plural = _('Suppliers')

    def __str__(self):
        return self.name

class SupplierCatalogDetail(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='supplier_catalog')
    product = models.ForeignKey(ProductDetail, on_delete=models.CASCADE, related_name='supplier_product')
    created_by = models.ForeignKey(UserCreation, verbose_name=_("Created by"), on_delete=models.PROTECT, related_name='supplier_catalog_creator')
    modified_by = models.ForeignKey(UserCreation, on_delete=models.DO_NOTHING, related_name='supplier_catalog_editor', null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Supplier's Catalog"
        verbose_name_plural = "Suppliers's Catalog"

class SupplierOfficeDetail(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='supplier_office')
    address_1 = models.CharField(_("Address line 1"), max_length=255, blank=False, null= False, help_text="Adress of the warehouse")
    address_2 = models.CharField(_("Address line 2"),max_length=255, blank=True, help_text="Complement info if needed")
    city = models.CharField(_("City"), max_length=255, blank=False, null=False, help_text="City of the warehouse")
    zip_code = models.CharField(_("Zip Code"), max_length=100, blank=False, null=False, help_text="Zip code")
    states = models.CharField(_("States"), max_length=100, blank=False , null=False, help_text="States or Region of the Warehouse")
    country = models.CharField(_("Country"), max_length=100, blank=False , null=False, help_text="Country")
    created_by = models.ForeignKey(UserCreation, verbose_name=_("Created by"), on_delete=models.PROTECT, related_name='supplier_office_creator')
    modified_by = models.ForeignKey(UserCreation, on_delete=models.DO_NOTHING, related_name='supplier_office_editor', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Supplier Office'
        verbose_name_plural = 'Suppliers Office'

class SupplierOfficeContact(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    first_name = models.CharField(_("First Name"), max_length=45, blank=False, null=False, help_text="First  Name of the contact")
    last_name = models.CharField(_("Last Name"), max_length=45, blank=False, null=False, help_text= "Last name of the contact")
    phone = models.CharField(_("Phone Number"),max_length=45, blank=False, null=False, help_text="Please add the country calling code")
    mail = models.EmailField(blank=False, null=False)
    post = models.CharField(max_length=45, blank=False, null=False)
    social_media = models.CharField(_("Social Media"), max_length=100, null=True, help_text="Wechat, Linkedin etc")
    created_by = models.ForeignKey(UserCreation, verbose_name=_("Created by"), on_delete=models.PROTECT, related_name='supplier_contact_creator')
    modified_by = models.ForeignKey(UserCreation, on_delete=models.DO_NOTHING, related_name='supplier_contact_editor', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Supplier Contact'
        verbose_name_plural = 'Suppliers Contact'

class SupplierBankDetail(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='supplier_bank_detail')
    name = models.CharField(_("Bank Name"),max_length=45, blank=True, null=True,  help_text="Bank Name")
    country = models.CharField(_("Country"), max_length=45, blank=True, null=True, help_text="residency of the bank")
    IBAN = models.CharField(_("IBAN"),  max_length=100,  blank=True, null=True,  help_text="IBAN number of the bank if exist seperate by white spaces after four digits") 
    SWIFT = models.CharField(_("SWIFT"),  max_length=100, blank=True, null=True,  help_text="SWIFT number of the bank if exist seperate by white spaces after four digits")
    BIC = models.CharField(_("BIC"),  max_length=100,  blank=True, null=True,  help_text="BIC of the bank seperate by white spaces after four digits") 
    protocol = models.CharField(_("Blockchain Protocol"), max_length=45,  blank=True, null=True, help_text="Blockchain Protocol If used")
    wallet_address = models.CharField(_("Wallet adress"), max_length=45,  blank=True, null=True, help_text="Wallet address  If used")
    created_by = models.ForeignKey(UserCreation, verbose_name=_("Created by"), on_delete=models.PROTECT, related_name='supplier_billing_creator')
    modified_by = models.ForeignKey(UserCreation, on_delete=models.DO_NOTHING, related_name='supplier_billing_editor', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Supplier Bank Detail'
        verbose_name_plural = 'Suppliers Bank Details'

class SupplierWarehouseDetail(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='warehouse_detail')
    building_name =  models.CharField(_("Building name"), max_length=45,  blank=True, null=True, help_text="Name on the Building if different from supplier")
    address_1 = models.CharField(_("Address line 1"), max_length=45, blank=False, null= False, help_text="Adress of the warehouse")
    address_2 = models.CharField(_("Address line 2"),max_length=45, blank=True, null=True, help_text="Complement info if needed")
    city = models.CharField(_("City"), max_length=45, blank=False, null=False, help_text="City of the warehouse")
    zip_code = models.CharField(_("Zip Code"), max_length=45, blank=False, null=False, help_text="Zip code")
    states = models.CharField(_("States"), max_length=45, null=False, help_text="States or Region of the Warehouse")
    country = models.CharField(_("Country"), max_length=45, null=False, help_text="Country")
    created_by = models.ForeignKey(UserCreation, verbose_name=_("Created by"), on_delete=models.PROTECT, related_name='warehouse_creator')
    modified_by = models.ForeignKey(UserCreation, on_delete=models.DO_NOTHING, related_name='warehouse_editor', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Warehouse Detail'
        verbose_name_plural = 'Warehouses Detail'

class SupplierWarehouseContact(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='warehouse_contact')
    first_name = models.CharField(_("First Name"), max_length=45, null=False, help_text="First  Name of the contact")
    last_name = models.CharField(_("Last Name"), max_length=45, null=False, help_text= "Last name of the contact")
    phone = models.CharField(_("Phone Number"),max_length=45, null=False, help_text="Please add the country calling code")
    mail = models.EmailField()
    post = models.CharField(max_length=100, blank=False, null=False)
    created_by = models.ForeignKey(UserCreation, verbose_name=_("Created by"), on_delete=models.PROTECT, related_name='warehouse_contact_creator')
    modified_by = models.ForeignKey(UserCreation, on_delete=models.DO_NOTHING, related_name='warehouse_contact_editor', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class SupplierDetail(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    catalog = models.ForeignKey(SupplierCatalogDetail, on_delete=models.CASCADE)
    office_detail = models.ForeignKey(SupplierOfficeDetail, on_delete=models.CASCADE)
    office_contact = models.ForeignKey(SupplierOfficeContact, on_delete=models.CASCADE)
    bank_detail = models.ForeignKey(SupplierBankDetail, on_delete=models.CASCADE)
    warehouse_detail = models.ForeignKey(SupplierWarehouseDetail, on_delete=models.CASCADE)
    warehouse_contact = models.ForeignKey(SupplierWarehouseContact, on_delete=models.CASCADE)
    updated_at = models.DateField(auto_now=True)
    created_by = models.ForeignKey(UserCreation, verbose_name=_("Created by"), on_delete=models.PROTECT, related_name='supploer_detail_creator')
    modified_by = models.ForeignKey(UserCreation, on_delete=models.DO_NOTHING, related_name='supploer_detail_creator', null=True)