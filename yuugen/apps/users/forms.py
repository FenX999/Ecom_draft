from django import forms
from django.contrib.auth import authenticate, get_user, password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

from yuugen.apps.core.methods import get_current_user, get_current_user_email
from .models import(
    User,
    EmployeeDetail,
    EmployeePayDetail,
    CustomerShippingDetail,
    CustomerBillingDetail,
    CustomerMarketingDetail,
)


"""
Model forms for store's staff
"""

class UserCreationForm(forms.ModelForm):
    '''
    Form that handle Staff creation 
    '''
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput)
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'email',
            'password1',
            'password2',
            'created_by',
            'is_manager',
            'is_staff',
            'is_active',
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields ='__all__'

class UserChangePassword(forms.Form):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = {
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }
    old_password = forms.CharField(
        label=_("Current password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'password-confirmation'}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["Current password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

class EmployeeDetailForm(forms.ModelForm):
    personnal_email = forms.EmailField(label=_('Personnal Email'), widget=forms.EmailInput)
    entry_date = forms.DateField(label=_('Entry date'), widget=forms.DateInput)
    departure_date =  forms.DateField(label=_('Entry date'), widget=forms.DateInput)
    fname = forms.CharField(required=True, label=_("First Name"), widget=forms.TextInput)
    lname = forms.CharField(required=True, label=_("Last Name"), widget=forms.TextInput)
    address_1 = forms.CharField(required=True, label=_("Address info"), widget=forms.TextInput(attrs={"placeholder":'eg: number and street name'}))
    address_2 = forms.CharField(required=False, label=_("Complement Info"), widget=forms.TextInput(attrs={"placeholder": 'eg: residential or building name if needed'}))
    zip_code = forms.CharField(required=True, label=_("Zip code"), widget=forms.TextInput)
    city = forms.CharField(required=True, label=_('City Name'), widget=forms.TextInput)
    states = forms.CharField(required=True, label=_('State Name'), widget=forms.TextInput)
    country = forms.CharField(required=True, label=_('Country Name'), widget=forms.TextInput)

    class Meta:
        model = EmployeeDetail
        exclude = {
            'created_by',
            'created_at',
            'updated_at',
        }

class EmployeePayDetailForm(forms.ModelForm):

    bank = forms.CharField(label=_('Bank Name'), widget=forms.TextInput)
    BIC =  forms.CharField(label=_('BIC numbers'), widget=forms.TextInput)
    IBAN =  forms.CharField(label=_('IBAN numbers'), widget=forms.TextInput)
    SWIFT =  forms.CharField(label=_('SWIFT numbers'), widget=forms.TextInput)
    protocole =  forms.CharField(label=_('Bockchain Protocole'), widget=forms.TextInput)
    wallet_address = forms.CharField(label=_('Wallet Address'), widget=forms.TextInput)

    class Meta:
        model = EmployeePayDetail
        exclude = {
            'created_by',
            'created_at',
            'updated_at',
        }


"""
forms for Store's customer
"""



class CustomerBillingForm(forms.ModelForm):
    fname = forms.CharField(required=True, label=_("First Name"), widget=forms.TextInput)
    lname = forms.CharField(required=True, label=_("Last Name"), widget=forms.TextInput)
    address_1 = forms.CharField(required=True, label=_("Address info"), widget=forms.TextInput(attrs={"placeholder":'eg: number and street name'}))
    address_2 = forms.CharField(required=False, label=_("Complement Info"), widget=forms.TextInput(attrs={"placeholder": 'eg: residential or building name if needed'}))
    zip_code = forms.CharField(required=True, label=_("Zip code"), widget=forms.TextInput)
    city = forms.CharField(required=True, label=_('City Name'), widget=forms.TextInput)
    states = forms.CharField(required=True, label=_('State Name'), widget=forms.TextInput)
    country = forms.CharField(required=True, label=_('Country Name'), widget=forms.TextInput)
    class Meta:
        model = CustomerBillingDetail
        fields = [
            'fname',
            'lname',
            'address_1',
            'address_2',
            'zip_code',
            'city',
            'states',
            'country',
            ]


class CustomerShippingForm(forms.ModelForm):
    fname = forms.CharField(required=True, label=_("First Name"), widget=forms.TextInput)
    lname = forms.CharField(required=True, label=_("Last Name"), widget=forms.TextInput)
    address_1 = forms.CharField(required=True, label=_("Address info"), widget=forms.TextInput(attrs={"placeholder":'eg: number and street name'}))
    address_2 = forms.CharField(required=False, label=_("Complement Info"), widget=forms.TextInput(attrs={"placeholder": 'eg: residential or building name if needed'}))
    zip_code = forms.CharField(required=True, label=_("Zip code"), widget=forms.TextInput)
    city = forms.CharField(required=True, label=_('City Name'), widget=forms.TextInput)
    states = forms.CharField(required=True, label=_('State Name'), widget=forms.TextInput)
    country = forms.CharField(required=True, label=_('Country Name'), widget=forms.TextInput)
    class Meta:
        model = CustomerShippingDetail
        fields = [
            'fname',
            'lname',
            'address_1',
            'address_2',
            'zip_code',
            'city',
            'states',
            'country',
            ]




class CustomerMarketingForm(forms.ModelForm):
    news_letter = forms.BooleanField(required=False, label=_('Do you wish to receive News Letter and future promotion?'), widget=forms.CheckboxInput)
    class Meta:
        model = CustomerMarketingDetail
        fields = {'news_letter'}