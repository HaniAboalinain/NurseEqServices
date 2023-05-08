from django.urls import path

from main.views import MainTemplate, AboutUsTemplateView, DepartmentsTemplateView, ContactTemplateView, ServicesTemplateView
from django.conf.urls.static import static
from NurseEqServices import settings
urlpatterns = [
    path('', MainTemplate.as_view(), name='home'),
    path('about_us', AboutUsTemplateView.as_view(), name='about-us'),
    path('services/', ServicesTemplateView.as_view(), name='services'),
    path('departments/', DepartmentsTemplateView.as_view(), name='departments'),
    path('contact_us/', ContactTemplateView.as_view(), name='contact-us'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
