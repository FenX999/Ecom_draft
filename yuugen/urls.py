from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('yuugen.apps.shop.urls')),
    path('crm/', include('yuugen.apps.crm.urls')),
    path('ems/', include('yuugen.apps.ems.urls')),
    path('cms/', include('yuugen.apps.cms.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
