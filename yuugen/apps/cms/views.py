import json

from django.template.response import TemplateResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpRequest, HttpResponseForbidden, JsonResponse
from django.core import serializers
from django.utils.text import slugify
from django.db.models import Q
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from yuugen.apps.users.models import User

from yuugen.apps.inventory.models import (
    ProductDetail,
    Finition,
    FinitionIndex,
    SizeIndex,
    Size,
    PublicPrice,
)

from yuugen.apps.navigation.models import (
    ThemeTag,
    CatalogTag,
    OperationTag,
    Product,
    ProductImage,
)

from yuugen.apps.navigation.forms import(
    ProductForm, 
    FlatPageForm,
    ProductImageForm, 
    ThemeTagForm,
    CatalogTagForm,
    OperationTagForm,
)
from yuugen.apps.inventory.forms import (
    ListFinitionForm,
    FinitionForm,
    ListSizeForm,
    SizeForm,
    ProductPublicPriceForm,
)
from yuugen.apps.navigation.models import FlatPage, Product, ProductImage


### custom class to prevent to bif of a boiler plate for global search function

class CmsSearchContext():
    '''
    custom class that will filter product, details and page based on query sent by a staff user with ajax call.
    manager can also sent a query based on an another user to retrieve all objects that user as created
    this will help globalize the search option on all the application and limit the code writen to achive that goal.
    this class does not deal with ajax , only deal with filtering the database related to the CMS app.
    '''
    def get_manager_context(self, fetched_query):
        context = dict()
        try:
            staff = User.objects.get(email__icontains=fetched_query)
        except ObjectDoesNotExist:
            staff = None
        if staff:
            context['staff_products'] = serializers.serialize('json',Product.objects.filter(Q(created_by=staff)))
            context['staff_details'] = serializers.serialize('json', ProductDetail.objects.filter(Q(created_by=staff)))
            context['staff_pages'] = serializers.serialize('json', FlatPage.objects.filter(Q(created_by=staff)))
            # print(f"staff context return:\n{context}")
        return context if len(context) > 0 else None
    def get_staff_context(self, fetched_query):
        context = dict()
        products = serializers.serialize('json',Product.objects.filter(Q(designation__icontains=fetched_query) |
                                                Q(slug__icontains=fetched_query)))
        # print(f'staff results at products:\n{products}')
        details = serializers.serialize('json',ProductDetail.objects.filter(Q(SKU__icontains=fetched_query)))
        # print(f'staff results at details:\n{details}')
        pages = serializers.serialize('json',FlatPage.objects.filter(Q(title__icontains=fetched_query)))
        # print(f'manager results at pages:\n{pages}')
        #populate context with value.
        if products != '[]':
            context['products'] = products
        if details != '[]':
            context['details'] = details
        if pages != '[]':
            context['pages'] = pages
        # print(f"context at search view return:\n{context}")
        return context if len(context)> 0 else None


def cms_home(request):
    '''
    Home view redirect to login if user is anonymous
    '''
    template = 'cms/navigation/cms-home.html'
    
    #instantiate custom class to retrieve search context
    call = CmsSearchContext()

    #send anonymous user to login 
    if not request.user.is_authenticated:
        return redirect('cms:login')

    #deal with ajax POST from the front end search item
    if request.POST.get('action') == "submit_search":
        query = request.POST.get('query')
        # print(f"query return:\n{query}")
        if request.user.is_manager:
            manager_data = call.get_manager_context(query)
            # print(f"manager_data return:\n{manager_data}")
        if request.user.is_staff or request.user.is_manager:
            staff_data = call.get_staff_context(query)
            # print(f"staff data return:\n{staff_data}")
            if not manager_data and not staff_data:
                messages.error(request, "No result found, try something else or double check your query.")
                return HttpResponseRedirect(redirect_to='cms/')
            if manager_data:
                data = manager_data
            if staff_data:
                data = staff_data
            # print(f"data at cms_home return:\n{data}")
        return JsonResponse(data)

    return TemplateResponse(request, template)

def product_list(request):
    if not request.user.is_authenticated:
        return redirect('cms:login')
    template = 'cms/product/list.html'
    context = {}
    context['products'] = Product.objects.all()
    return TemplateResponse(request, template, context)

def product_creator(request):
    '''
    view that create:
    1 a product 
    2 its attributes
    3 the navigation path that demonstrate the product in the store
    '''
    if not request.user.is_authenticated:
        return redirect('cms:login')
    template = 'cms/product/creator.html'
    creator = User.objects.get(email = request.user)
    context = {}
    context['product'] = ProductForm()
    context['ttag'] = ThemeTagForm()
    context['ctag'] = CatalogTagForm()
    context['otag'] = OperationTagForm()
    context['finition'] = FinitionForm()
    context['size'] = SizeForm()
    context['image'] = ProductImageForm()
    context['price'] = ProductPublicPriceForm()

    context['finition_list'] = Finition.objects.all()
    context['size_list'] = Size.objects.all()
    
    #Tag creation
    if request.POST.get('ajax_post') == 'create_ttag':
        ThemeTag.objects.create(
            created_by = creator,
            ttag = request.POST.get('sent_ttag'),
            tslug = slugify(request.POST.get('sent_ttag')),
        )
        context['product']['ttag'].queryset = ThemeTag.objects.all()


    if request.POST.get('ajax_post') == 'create_ctag':
        CatalogTag.objects.create(
            created_by = creator,
            ctag = request.POST.get('sent_ctag'),
            cslug = slugify(request.POST.get('sent_ctag')),
        )
        context['product']['ctag'].queryset = CatalogTag.objects.all()

    if request.POST.get('ajax_post') == 'create_otag':
        OperationTag.objects.create(
            created_by = creator,
            otag = request.POST.get('sent_otag'),
            oslug = slugify(request.POST.get('sent_otag')),
        )
        context['product']['otag'].queryset = OperationTag.objects.all()


    #logic for product creation
    if request.POST.get('ajax_post') == ('create_product'):
        # for key, value in request.POST.items():
        #     print(key, value)
        fetched_name = request.POST.get('designation')
        compiled_sku = 'sku_'+fetched_name.lower()
        fetched_ttag = request.POST.get('selected_ttag')
        fetched_ctag = request.POST.get('selected_ctag')
        fetched_otag = request.POST.get('selected_otag')
        if fetched_name:
        #As tag are extremely important check for empty value and send message to front end
            if fetched_ttag and fetched_ctag and fetched_otag :
                try:
                    detail = ProductDetail.objects.get(SKU = compiled_sku, created_by = creator)
                    if detail :
                        msg = {'submit_failure': f'SKU already created check your entry'}
                        return JsonResponse(msg)
                except ObjectDoesNotExist:
                    ProductDetail.objects.create(SKU = compiled_sku, created_by = creator)
                try :
                    product = Product.objects.get(
                        designation= fetched_name,
                        slug = slugify(fetched_name),
                        description = request.POST.get('description'),
                        SKU = ProductDetail.objects.get(SKU = compiled_sku),
                        created_by = creator,
                        ttag = ThemeTag.objects.get(ttag = fetched_ttag),
                        ctag = CatalogTag.objects.get(ctag = fetched_ctag),
                        otag = OperationTag.objects.get(otag = fetched_otag ),
                    )
                    if product:
                        msg = {'submit_failure':'Product name already exist, choose something else.'}
                        return JsonResponse(msg)
                except ObjectDoesNotExist:
                    product = Product.objects.create(
                        designation= fetched_name,
                        slug = slugify(fetched_name),
                        description = request.POST.get('description'),
                        SKU = ProductDetail.objects.get(SKU = compiled_sku),
                        created_by = creator,
                        ttag = ThemeTag.objects.get(ttag = fetched_ttag),
                        ctag = CatalogTag.objects.get(ctag = fetched_ctag),
                        otag = OperationTag.objects.get(otag = fetched_otag ),
                    )
                attr = json.loads(request.POST.get('attr'))
                for row in attr:
                    print(row)
                    fetched_finition =  row['finition'].lower()
                    if fetched_finition:
                        compiled_finition_sku = str('sku_'+fetched_name.lower()+'_'+fetched_finition)
                        try: 
                            fdetail = ProductDetail.objects.get(SKU = compiled_finition_sku, created_by = creator)
                        except ObjectDoesNotExist:
                            ProductDetail.objects.create(SKU = compiled_finition_sku, created_by = creator)
                            fdetail = ProductDetail.objects.get(SKU = compiled_finition_sku, created_by = creator)
                        try:
                            created_finition = Finition.objects.get(value = fetched_finition)
                        except ObjectDoesNotExist:
                            Finition.objects.create(value = fetched_finition)
                            created_finition = Finition.objects.get(value = fetched_finition)
                        try:
                            finition_index = FinitionIndex.objects.get(SKU = fdetail , created_by = creator,)
                        except ObjectDoesNotExist:
                            FinitionIndex.objects.create(SKU = fdetail ,created_by = creator)
                            finition_index = FinitionIndex.objects.get(SKU = fdetail , created_by = creator,)
                        finition_index.finition.add(created_finition)
                        ProductImage.objects.get_or_create(img = row['img'], created_by= creator, SKU = fdetail)

                    #size
                    fetched_size = row['size'].lower()
                    if fetched_size:
                        compiled_size_sku = str('sku_'+fetched_name.lower()+'_'+fetched_size)

                        try:
                            sdetail = ProductDetail.objects.get(SKU = compiled_size_sku, created_by = creator)
                        except ObjectDoesNotExist:
                            ProductDetail.objects.create(SKU = compiled_size_sku, created_by = creator)
                            sdetail = ProductDetail.objects.get(SKU = compiled_size_sku, created_by = creator)
                        try:
                            created_size = Size.objects.get(value = fetched_size)
                        except ObjectDoesNotExist:
                            Size.objects.create(value = fetched_size)
                            created_size = Size.objects.get(value = fetched_size)
                        try:
                            size_index = SizeIndex.objects.get(SKU = sdetail, created_by= creator)
                        except ObjectDoesNotExist:
                            SizeIndex.objects.create(SKU = sdetail, created_by= creator)
                            size_index = SizeIndex.objects.get(SKU = sdetail, created_by= creator)
                        size_index.size.add(created_size)
                    #price 
                    fetched_price = row['price']
                    if fetched_price and fetched_finition and fetched_size:
                        compiled_price_sku = str('sku_'+fetched_name.lower()+'_'+fetched_finition+'_'+fetched_size)
                        ProductDetail.objects.create(SKU = compiled_price_sku, created_by= creator)
                        PublicPrice.objects.create(public_price = fetched_price, SKU = ProductDetail.objects.get(SKU = compiled_price_sku), created_by = creator)

                    elif fetched_price and fetched_finition and not fetched_size:
                        PublicPrice.objects.create(public_price= fetched_price, SKU = ProductDetail.obects.get(SKU = compiled_finition_sku), created_by= creator)

                    elif fetched_price and fetched_size and not fetched_finition:
                        PublicPrice.objects.create(public_price= fetched_price, SKU = ProductDetail.objects.get(SKU = compiled_size_sku), created_by= creator)

                    elif fetched_price and not fetched_finition and not fetched_size:
                        PublicPrice.objects.create(public_price= fetched_price, SKU = ProductDetail.objects.get(SKU = compiled_sku), created_by= creator)
                        ProductImage.objects.create(img = row['img'], created_by = creator, SKU = ProductDetail.objects.get(SKU= compiled_sku))

                    else :
                        msg =  {'submit_failure':"price missing check your entry"}
                        return JsonResponse(msg)
            else:
                msg = {'submit_failure':  'Tag Error: Tags cannot be left empty!'}
                print(msg)
                return JsonResponse(msg)
        else:
            msg = {'submit_failure':'Name error: Name missing please check your entry'}
            print(msg)
        return JsonResponse(msg) 
    return TemplateResponse(request, template, context)

def view_product_form(request, pslug):
    #setting variable for function and logic
    template = 'cms/product/info.html'
    context = {}
    attr = []
    #setting context to be demonstrate
    context['ttag'] = ThemeTag.objects.all()
    context['ctag'] = CatalogTag.objects.all()
    context['otag'] = OperationTag.objects.all()
    context['finitions'] = Finition.objects.all()
    context['sizes'] = Size.objects.all()
    #setting fetched context
    context['product'] = Product.objects.get(slug = pslug)
    context['prices'] = PublicPrice.objects.filter(SKU__SKU__icontains = context['product'].SKU)
    for i in context['prices']:
        finition =  str(i.SKU).split('_')[2]
        size =  str(i.SKU).split('_')[3]
        price =  i.public_price
        image = ProductImage.objects.get(SKU__SKU__icontains= str(context['product'].SKU)+'_'+finition)
        output = {
            'id': i.id,
            'finition': finition,
            'size': size,
            'price': str(price),
            'image': image.img,
        }
        attr.append(output)
    context['attributes'] = attr
    
    #dealing with ajax call for new entry plus editing existing
    if request.POST.get('ajax_post') == 'create_ttag':
        ThemeTag.objects.create(
            created_by = creator,
            ttag = request.POST.get('sent_ttag'),
            tslug = slugify(request.POST.get('sent_ttag')),
        )
    context['ttag'] = ThemeTag.objects.all()


    if request.POST.get('ajax_post') == 'create_ctag':
        CatalogTag.objects.create(
            created_by = creator,
            ctag = request.POST.get('sent_ctag'),
            cslug = slugify(request.POST.get('sent_ctag')),
        )
        context['ctag'] = CatalogTag.objects.all()

    if request.POST.get('ajax_post') == 'create_otag':
        OperationTag.objects.create(
            created_by = creator,
            otag = request.POST.get('sent_otag'),
            oslug = slugify(request.POST.get('sent_otag')),
        )
        context['otag'] = OperationTag.objects.all()
    return TemplateResponse(request, template, context)

def del_product(request, pslug):
    '''
    View that deal with product edition based on the following rules:
    staff cannot change:
        designation of the product 
        slug of the product
        SKU of the product 
    staff can change :
        description of the product 
        tags of the product 
        prices of the product 
    staff can create :
        new tags 
        new finition & size
        new price 
        new SKU
    manager have permissions for all the details named above plus erase function
    '''
    if not request.user.is_authenticated:
        return redirect('cms:login')
    template = 'cms/product/editor.html'
    pass

def del_product(request):
    pass

def flatpage_list(request):
    if not request.user.is_authenticated:
        return redirect('cms:login')
    template = 'cms/navigation/page-list.html'
    context = {}
    context['pages'] = FlatPage.objects.all()
   

    return TemplateResponse(request, template, context)

def flatpage_creator(request):
    if not request.user.is_authenticated:
        return redirect('cms:login')

    template = 'cms/navigation/page-creator.html'
    context={}
    context['page'] = FlatPageForm()
    if request.POST.get('action') == 'create_page':
        print('hitted')
        fetched_title = request.POST.get("title")
        fetched_url = slugify(fetched_title)
        fetched_content = request.POST.get('content')
        print(fetched_title, fetched_url)
        FlatPage.objects.create(
            url = fetched_url,
            title = fetched_title,
            content = fetched_content,
            created_by= User.objects.get(email=request.user)
        )


    return TemplateResponse(request, template, context)

