from django.db import models
from django.utils.translation import gettext_lazy as _ 
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
)

class CustomAccountManager(BaseUserManager):
    '''
    Custom User Manager to add more accreditations.
    '''
    def create_superuser(self, email, password, **extra_fields,):
        '''
        Custom superuser creator with a set of extra fields
        for permission, only superuser should delete data
        '''
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault('is_manager', True)
        extra_fields.setdefault('is_staff', True )
        extra_fields.setdefault("is_customer", True)
        extra_fields.setdefault("is_active", True)
        if not email:
            raise ValueError(f"You must provide an email")
        return self.create_user(email, password,  **extra_fields)

    def create_manager_user(self, email, password, **extra_fields):
        '''
        Custom Manager user to help deal precisly with permissions
        manager can: add, change, view, and set is_active to false. 

        '''
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault('is_manager', True)
        extra_fields.setdefault('is_staff', True )
        extra_fields.setdefault("is_customer", True)
        extra_fields.setdefault("is_active", True)
        if not email:
            raise ValueError(f"You must provide an email")
        return self.create_manager_user(email, password, **extra_fields)

    def create_staff_user(self, email, password, **extra_fields):
        '''
        Custom staff user to help deal precisly with permissions
        staff can only: add, and view data the ability to change should be 
        restricted to the minima. 

        '''
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault('is_manager', False)
        extra_fields.setdefault('is_staff', True )
        extra_fields.setdefault("is_customer", True)
        extra_fields.setdefault("is_active", True)
        if not email:
            raise ValueError(f"You must provide an email")
        return self.create_staff_user(email, user_name, password, **extra_fields)

    def create_user(self, email, password, **extra_fields):
        '''
        Classic user for Customer can only
        add change and view their own information
        '''
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault('is_manager', False)
        extra_fields.setdefault('is_staff', False )
        extra_fields.setdefault("is_customer", True)
        extra_fields.setdefault("is_active", True)
        if not email:
            raise ValueError(f"You must provide an email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email"), max_length=254, unique=True)
    groups = models.ManyToManyField(Group, verbose_name=_("Accreditation"))
    url_creation = models.CharField(max_length=20, blank=True)
    is_superuser = models.BooleanField(_('Super User Accreditation'), default=False)
    is_manager = models.BooleanField(_('Manager Accreditation'), default=False)
    is_staff = models.BooleanField(_('Staff Accreditation'), default=False)
    is_customer = models.BooleanField(_('Customer Accreditation'), default=True)
    is_active = models.BooleanField(_('Active Status'), default=True)
    created_by = models.ForeignKey('self', on_delete=models.PROTECT, related_name='user_creator')
    # created_by = models.CharField(max_length=1, default=1)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class EmployeeDetail(models.Model):
    '''
    model that deal with Personnal information on employees
    '''
    email = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_created_email')
    peronnal_email = models.EmailField(max_length=254, blank=True, null=True)
    entry_date = models.DateField(blank=False)
    departure_date = models.DateField(blank=True, null=True)
    fname = models.CharField(_("First Name"), max_length=150, unique=False, blank=False, help_text="First Name of the employee")
    lname = models.CharField(_("Last Name"), max_length=150, unique=False, blank=False, help_text="Last Name o the employee")
    address_1 = models.CharField(_("Address Line 1"), max_length=150,blank=True,  help_text="employee address information")
    address_2 = models.CharField(_("Address Line 2 "), max_length=150, blank=True,  help_text="for complementary info if needed")
    zip_code = models.CharField(_("Zip code"), max_length=150, blank=True,  help_text=" Employee Zip code")
    city = models.CharField(_("City Name"), max_length=150, blank=True,  help_text="Employee City name")
    states = models.CharField(_("States"), max_length=150, blank=True, help_text="Employee States or Region")
    country = models.CharField(_("Country"), max_length=150, blank=True,  help_text="Employee Country")
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, related_name='employee_creator')
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    class Meta:
        verbose_name = 'Employee Details'
        verbose_name_plural = 'Employees Details'
        ordering = ('-created_at',)
    def __str__(self):
        return self.lname

class EmployeePayDetail(models.Model):
    '''
    Model that deal with financial info on Employees 
    adding the capacity to store Blockchain Wallet and protocole
    '''
    email= models.ForeignKey(User, on_delete=models.CASCADE, related_name='employe_bank_detail')
    bank= models.CharField(_('Bank'), max_length=45, blank=True, null=True)
    BIC= models.CharField(_('BIC'), max_length=45, blank=True, null=True)
    IBAN= models.CharField(_('IBAN'), max_length=45, blank=True, null=True)
    SWIFT= models.CharField(_('SWFIT'), max_length=45, blank=True, null=True)
    protocol= models.CharField(_('Blockchain Protocol'), max_length=45, blank=True, null=True)
    wallet_address= models.CharField(_('Wallet Address'), max_length=45,  blank=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created by"), on_delete=models.PROTECT, related_name='employee_pay_creator')
    created_by = models.CharField(max_length=1, null = True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Employee Bank Details'
        verbose_name_plural = 'Employees Bank Details'
        ordering = ('-created_at',)
    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("Employee pay details")
        verbose_name_plural = _("Employess pay details")

class CustomerBillingDetail(models.Model):
    '''
    model that fetch personnal info about the buyer and help with 
    payement fraud  
    '''
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(_("First Name"), max_length=150, unique=False, null=False, help_text="First Name")
    lname = models.CharField(_("Last Name"), max_length=150, unique=False, null=False,  help_text="Last Name")
    address_1 = models.CharField(_("Address Line 1"), max_length=150, null=False, help_text="Your address information here")
    address_2 = models.CharField(_("Address Line 2 "), max_length=150, null=True, help_text="for complementary info if needed")
    zip_code = models.CharField(_("Zip code"), max_length=150, unique=False, help_text="Zip code")
    city = models.CharField(_("City Name"), max_length=150, unique=False, help_text="City name")
    states = models.CharField(_("States"), max_length=150, unique=False, help_text="States or Region")
    country = models.CharField(_("Country"), max_length=150, unique=False, help_text="Country")
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Customer Billing Details'
        verbose_name_plural = 'Customers Billing Details'

    def __str__(self):
        return self.lname

class CustomerShippingDetail(models.Model):
    '''
    Model that store shipping information in case buyer needs different 
    detail eg purchase sent as a gift to a third party
    '''
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    same_as_billing = models.BooleanField(default=False)
    fname = models.CharField(_("First Name"), max_length=150, unique=False, blank=True, help_text="First Name")
    lname = models.CharField(_("Last Name"), max_length=150, unique=False, blank=True, help_text="Last Name")
    address_1 = models.CharField(_("Address Line 1"), max_length=150,blank=True,  help_text="Your address information here")
    address_2 = models.CharField(_("Address Line 2 "), max_length=150, blank=True,  help_text="for complementary info if needed")
    zip_code = models.CharField(_("Zip code"), max_length=150, blank=True,  help_text="Zip code")
    city = models.CharField(_("City Name"), max_length=150, blank=True,  help_text="City name")
    states = models.CharField(_("States"), max_length=150, blank=True, help_text="States or Region")
    country = models.CharField(_("Country"), max_length=150, blank=True,  help_text="Country")
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Customer Shipping Details'
        verbose_name_plural = 'Customers Shipping Details'

    def __str__(self):
        return self.lname


class CustomerMarketingDetail(models.Model):
    '''
    model that store marketing option, buyer as control over.
    '''
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    news_letter = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Customer Marketing'
        verbose_name_plural = 'Customers Marketting'

