from django.template.response import TemplateResponse


# Create your views here.

def ems_index(request):
    return TemplateResponse(request, 'ems/navigation/ems-home.html')

def create_staff_views(request):
    template = "ems/navigation/create-staff.html"
    return TemplateResponse(request, template)