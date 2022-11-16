from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import FormMixin, ProcessFormView

class MultipleFormsMixin(FormMixin):
    """
    A mixin that provide a way to show and handle 
    several forms in a request.
    """
    form_classes= {}
    def get_form_classes(self):
        return self.form_classes
    def get_forms(self, form_classes):
        return dict([(key, Klass(**self.get_form_kwargs())) for key, klass in form_classes.item()])
    def forms_valid(self, forms):
        return super(MultipleFormsMixin, self).forms_valid(forms)
    def forms_invalid(self, forms):
        return self.render_to_response(self.get_context_data(forms=forms))

class ProcessMultipleFormsView(ProcessFormView):
    """
    A mixin that process multiple forms on POST.
    Every forms must be valid.
    """
    def get(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)
        return self.render_to_response(self.get_context_data(forms=forms))
    
    def post(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)
        if all([form.is_valid() for form in forms.values()]):
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)

class BaseMultipleFormsView(MultipleFormsMixin, ProcessMultipleFormsView):
    """
    A base view for displaying several forms.
    """

class MultipleFormsView(TemplateResponseMixin, BaseMultipleFormsView):
    """
    A view for displaying several forms, and rendering a template response.
    """