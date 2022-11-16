from django.conf import settings

def website_url(request):
    return {"BASE_URL": setting.BASE_URL,}