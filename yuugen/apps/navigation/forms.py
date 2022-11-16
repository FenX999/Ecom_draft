from django import forms
from django.utils.translation import gettext_lazy as _

from yuugen.apps.inventory.models import ProductDetail

from .models import(
    ThemeTag,
    CatalogTag,
    OperationTag,
    FlatPage,
    Product,
    ProductImage,
)




class FlatPageForm(forms.ModelForm):
    url = forms.URLField(label=_('URL'), widget=forms.URLInput)
    title = forms.CharField(label=_('Title'), widget=forms.TextInput(attrs={"id":"id_title_input"}))
    content = forms.CharField(label=_('Content'), widget=forms.Textarea(attrs={"id":"id_content_input"}))

    class Meta:
        model = FlatPage
        fields = '__all__'


class ThemeTagForm(forms.ModelForm):
    ttag = forms.CharField(label=_('Theme Tag'),widget=forms.TextInput(attrs={"id":"id_input_ttag"}), required=False)
    
    class Meta:
        model = ThemeTag
        fields = ('ttag',)

class CatalogTagForm(forms.ModelForm):
    ctag = forms.CharField(label=_('Catalog Tag'), widget=forms.TextInput(attrs={"id":"id_input_ctag"}), required=False)

    class Meta:
        model = CatalogTag
        fields = ('ctag',)


class OperationTagForm(forms.ModelForm):
    otag = forms.CharField(label=_('Opertion Tag'), widget=forms.TextInput(attrs={"id":"id_input_otag"}), required=False)
    
    class Meta:
        model = OperationTag
        fields = ("otag",)

class ProductForm(forms.ModelForm):
    designation = forms.CharField(label=_('Product designation'), widget=forms.TextInput(attrs={"id":"id_designation_input"}))
    description = forms.CharField(label=_('Description'), widget=forms.Textarea(attrs={"id":"id_description-input"}))
    ttag = forms.ModelChoiceField(
        queryset=ThemeTag.objects.filter(is_active = True),
        to_field_name='ttag',
        label=_('Theme Tag'),
        empty_label='------',
        widget=forms.Select(attrs={"id":"id_product_select_ttag"}))
    ctag = forms.ModelChoiceField(
        queryset=CatalogTag.objects.filter(is_active = True),
        to_field_name='ctag',
        label=_('Catalog Tag'),
        empty_label='------',
        widget=forms.Select(attrs={"id":"id_product_select_ctag"})
        )
    otag = forms.ModelChoiceField(
        queryset=OperationTag.objects.filter(is_active=True),
        to_field_name='otag',
        label=_('Operation Tag'),
        empty_label='------',
        widget=forms.Select(attrs={"id":"id_product_select_otag"})
        )
    class Meta:
        model = Product
        fields = ('ttag', 'ctag', 'otag', 'designation', 'description',)


class ProductImageForm(forms.ModelForm):
    img = forms.ImageField(
        label=_('Upload Image'), widget=forms.ClearableFileInput(attrs={"id":"id_image_input"}))
    
    class Meta:
        model = ProductImage
        fields = ('img',)