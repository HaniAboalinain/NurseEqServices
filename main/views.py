# Create your views here.
from django.views.generic import TemplateView
from user.models import CustomUser, Staff
from django.shortcuts import redirect


class MainTemplate(TemplateView):
    template_name = 'templates/home.html'

    def get(self, request, *args, **kwargs):
        if Staff.objects.filter(user_id=request.user.id).exists():
            return redirect('staff-dashboard')
        else:
            return super().get(request, args, kwargs)

    def get_template_names(self):
        if self.request.user.id is None:
            return 'home.html'
        return super(MainTemplate, self).get_template_names()


class AboutUsTemplateView(TemplateView):
    template_name = 'templates/partials/about.html'


class ServicesTemplateView(TemplateView):
    template_name = 'templates/partials/services.html'


class DepartmentsTemplateView(TemplateView):
    template_name = 'templates/partials/departments.html'


class ContactTemplateView(TemplateView):
    template_name = 'templates/partials/contact.html'
