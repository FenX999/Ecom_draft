from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist


from yuugen.apps.users.models import (
    User,
    CustomerBillingDetail,
    CustomerShippingDetail,
    CustomerMarketingDetail,

)

from yuugen.apps.navigation.models import (
    ThemeTag,
    CatalogTag,
    OperationTag,
    Product,
    ProductDetail,
    ProductImage,
)

from yuugen.apps.inventory.models import PublicPrice, ProductDetail

'''
Profile creator :
This module deal with profile and groups that will work, visit or use this website projects
and management systems permission have been looked as an option nevertheless they only are usefull
for the admin website and since each groups should have their own mangement system to work with they have been droped.

'''

def get_or_create_store_proxy_user():
    '''
    functiun that get or create a proxy profile that store's customer apply on upon creation 
    as created_by.
    Use at customer registration.
    '''
    try: 
        store_proxy = User.objects.get(email='store@email.com')
    except ObjectDoesNotExist:
        proxy = User.objects.create(
        email = 'store@email.com',
        password="testpass123",
        created_by=User.objects.get(email='admin@email.com')
        )
        store_proxy = UserCreation.objects.get(email='store@email.com')
    return store_proxy



def get_or_create_groups(group_name=None, obj=None):
    '''
    get or create groups based on list fectech with django.appse
    '''
    from django.apps import apps
    ilist = []
    ilist2 = []
    for item in apps.get_app_configs():
        ilist.append(str(item))
        for i in ilist:
            ni = i.split(':')[1].strip('>')
            ilist2.append(ni if ni not in ilist2 else '')
            for nti in ilist2:
                if nti =='':
                    ilist2.remove(nti)