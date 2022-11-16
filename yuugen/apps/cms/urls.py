from django.urls import path
from . import views


from yuugen.apps.users.views import login_view, logout_view, register_view

app_name='cms'

urlpatterns = [
    #home url of the cms app 
    path('', views.cms_home, name='home' ),
    #global login logout urls.
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    #product CRUD
    path('product_creator/', views.product_creator, name='product-creation'),
    path('product_editor/', views.edit_product, name='product-editor'),
    path('products_list',views.product_list, name ='product-list'),
    path('products_info/<str:product_id',views.view_product_form, name ='product-info'),
    #pages CRUD
    path('page_creator/', views.flatpage_creator, name='page-creator'),
    path('page_editor/', views.flatpage_list, name='page-editor'),
    path('pages/', views.flatpage_list, name="page-list"),
]