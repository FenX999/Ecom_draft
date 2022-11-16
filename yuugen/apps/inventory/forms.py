from django import forms
from django.utils.translation import gettext_lazy as _ 
from .models import(
    ProductDetail,
    FinitionIndex,
    SizeIndex,
    Finition,
    Size,
    Stock,
    DetailWeight,
    DetailVolume,
    RetailPrice,
    PublicPrice,
)




class ListFinitionForm(forms.ModelForm):
    finition = forms.ModelMultipleChoiceField(
        label=_('Finition Options'),
        widget=forms.SelectMultiple(attrs={"id":"id_finition_select"}),
        queryset= Finition.objects.all()
        )
    class Meta:
        model = FinitionIndex
        fields = ('finition', )


class ListSizeForm(forms.ModelForm):
    size = forms.ModelMultipleChoiceField(
        label=_('Size Options'),
        widget=forms.SelectMultiple(attrs={"id":"id_size_select"}),
        queryset = Size.objects.all(),
        )
    class Meta:
        model = SizeIndex
        fields = ('size',)

class SizeForm(forms.ModelForm):
    value = forms.CharField(
        label=_('Size'),
        widget=forms.TextInput(attrs={"id":"id_size_input"}), 
        help_text=_('Add a Size if not available in the list.'),
        )
    class Meta:
        model = Size
        fields = ('value',)


class FinitionForm(forms.ModelForm):
    value = forms.CharField(
        label=_('Finition'),
        widget=forms.TextInput(attrs={"id":"id_finition_input"}),
        help_text=_('Select all characteristics that your product will need or add yours below if not in the list.'),
        )
    class Meta:
        model = Finition
        fields = ('value',)

class ProductPublicPriceForm(forms.ModelForm):
    public_price = forms.DecimalField(
        label='Public Price',
        max_digits= 11,
        decimal_places= 2,
        widget=forms.TextInput(attrs={"id":"id_price_input"}),
    )

    class Meta:
        model = PublicPrice
        fields =('public_price',)


###need volume, stock, weight, prices