from django.template.response import TemplateResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from yuugen.apps.users.models import (
    User,
    CustomerBillingDetail,
    CustomerShippingDetail,
    CustomerMarketingDetail,
    )

from yuugen.apps.users.forms import (
    UserCreationForm,
    UserChangeForm,   
    CustomerBillingForm,
    CustomerShippingForm,
    CustomerMarketingForm,
    UserChangePassword,
)
from yuugen.apps.navigation.models import (
   ThemeTag,
   CatalogTag,
   OperationTag,
   Product,
   ProductImage,
)
from yuugen.apps.inventory.models import (
   ProductDetail,
   PublicPrice,
   Finition,
   Size,
)

from yuugen.apps.core.profile import get_or_create_store_proxy_user

#store's navigations

def shop_home_view(request):
    data = ThemeTag.objects.all()
    # print(f"home page data : {data}")
    # print(f"home page : {data.query}")
    context = {'data':data,}
    return TemplateResponse(request, 'store/navigation/home.html', context)

def catalog_list_view(request, tslug=None):
    tslug = request.get_full_path().strip('/')
   #  print(f'catalog view => {tslug}')
    data = Product.objects.filter(Q(is_active=True) & Q(theme_tag_id__tslug=tslug)).distinct('catalog_tag_id')
    #print(data)
    #print(f"catalog page :\n {data.query}")
    context={'data': data,}
    return TemplateResponse(request, 'store/navigation/catalog-list.html', context)

def product_list_view(request, tslug=None, cslug=None):
    tslug = request.META['HTTP_REFERER'].split('/')[-2]
    # print(f'product-list tslug => {tslug}')
    cslug = request.get_full_path().split('/')[-2]
    # print(f'product-list cslug => {cslug}')
    objects = Product.objects.filter(
        Q(is_active=True) & 
        Q(theme_tag_id__tslug=tslug) & 
        Q(catalog_tag_id__cslug=cslug)).defer('created_at', 'updated_at')
    # print(f"product list query objects :\n {objects.query}")
    # print(f'product-list value objects:\n {objects.values()}')
    # sku = list(objects.values_list('SKU_id', flat=True))
    # print(f"product list sku :{sku}")
    detail = PublicPrice.objects.all().defer('created_at', 'updated_at')
    # print(f"product-list detail query :\n {detail.query}")
    # print(f'product-list detail values:\n {detail.values()}')
    # print(f'product-list detail: {dir(detail)}')
    context={'objects':objects, 'detail':detail}
    # print(f'product -list context :\n {context}')
    return TemplateResponse(request, 'store/navigation/product-list.html', context)


@require_http_methods(["GET", "POST"])
def product_detail_view( request, slug=None):
   obj = get_object_or_404(Product, slug = request.get_full_path().split('/')[-2])
   img = get_object_or_404(ProductImage, product_id = obj.id )
   detail = get_list_or_404(ProductDetail, SKU__startswith=obj.SKU)
   
   try:
         finition= Finition.objects.filter(Q(SKU_detail_id__in=detail)).distinct('finition')
   except:
          return finition
   try:
      size = Size.objects.filter(Q(SKU_detail_id__in=detail)).distinct('value')
   except :
      return size
   listed_price = get_list_or_404(PublicPrice, SKU_detail_id__in=detail)

   context = {
      'obj': obj,
      'img': img,
      'finition': finition,
      'size': size, 
      'price': listed_price,
   }
   # def get_finition(self, *args, **kwats):
   #    if request.is_ajax and request.method == 'POST':
   #       fetched_finition = request.POST.get("finition")
   #       return str(fetched_finition)
   # def get_size(self, *args, **kwargs):
   #    if request.is_ajax and request.method == 'POST':
   #       fetched_size = request.POST.get('size')
   #       return str(fetched_size)
   def select_price(self, *args, **kwarg):
      if request.method == "POST" and request.is_ajax():
         detail = request.POST.get('detail')
         print(detail)
         instance = (detail if detail in listed_price else listed_price)
         sr_instance = serializers.serialize('json', [ instance, ])
         print(f"for size not finition:{sr_instance}")
         return JsonResponse({'instance': sr_instance}, status=200)
   return TemplateResponse(request, 'store/product/product-detail.html', context)


@login_required(login_url='/login/')
def customer_profile(request):
    context= {}
    try:
        context["detail"] = User.objects.get(email= request.user)
        context["shipping"] = CustomerShippingDetail.objects.get(email_id=request.user.id)
        context["billing"] = CustomerBillingDetail.objects.get(email_id=request.user.id)
        context["marketing"] = CustomerMarketingDetail.objects.get(email_id=request.user.id)
    except :
        pass
    return TemplateResponse(request, 'store/users/profile.html', context)

@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = UserChangePassword(request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('shop:customer-profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserChangePassword(request.POST)
    return TemplateResponse(request, 'store/users/change-password.html', {'form': form})

def update_billing_detail(request):
    userid = request.user.id
    user_email = request.user
    if request.method == 'POST':
        form = CustomerBillingForm(request.POST, request.user)
        if form.is_valid():
            print(f"print after form valid method{form.fields}")
            fs = form.save(commit=False)
            fs.email = User.objects.get(id=userid)
            fs.save()
            return redirect('shop:customer-profile')
    else :
        form = CustomerBillingForm()
    return TemplateResponse(request, 'store/users/customer-billing.html', {'form': form})

def update_shipping_detail(request):
    userid = request.user.id
    if request.method == 'POST':
        form = CustomerShippingForm(request.POST, request.user)
        if form.is_valid():
            print(f"print after form valid method{form.fields}")
            fs = form.save(commit=False)
            fs.email = User.objects.get(id=userid)
            fs.save()
            return redirect('shop:customer-profile')
    else :
        form = CustomerShippingForm()
    return TemplateResponse(request, 'store/users/customer-shipping.html', {'form': form})

def update_marketing_detail(request):
    userid = request.user.id
    if request.method == 'POST':
        form = CustomerMarketingForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.email = User.objects.get(id=userid)
            fs.save()
            return redirect('shop:customer-profile')
    else:
        form = CustomerMarketingForm()
    return TemplateResponse(request, 'store/users/marketing-detail.html', {'form': form})