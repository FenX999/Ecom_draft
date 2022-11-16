from django.urls import path

from yuugen.apps.users.views import login_view, logout_view, register_view

from .views import (
     shop_home_view,
     catalog_list_view,
     product_list_view,
     product_detail_view,
     customer_profile,
     update_shipping_detail,
     update_billing_detail,
     update_marketing_detail,
     change_password,
)


app_name = 'shop'


urlpatterns=[
     #flatpage for ecom
     #store's navigation
     path('', shop_home_view, name='home'),
     path('<slug:tslug>', catalog_list_view, name='catalog-list'),
     path('<slug:cslug>', product_list_view, name='product-list'),
     path('<slug:slug>', product_detail_view, name='product-detail'),
     #customer CRUD
     path('register/', register_view, name='customer-register'),
     path('login/', login_view, name='customer-login'),
     path('logout/', logout_view, name='customer-logout'),
     #customer's hub
     path('profile', customer_profile, name='customer-profile'),
     path('shipping-detail', update_shipping_detail, name='customer-shipping'),
     path('billing-detail', update_billing_detail, name='customer-billing'),
     path('change-password', change_password, name='customer-password'),
     path('marketing-detail', update_marketing_detail, name='customer-marketing'),
]