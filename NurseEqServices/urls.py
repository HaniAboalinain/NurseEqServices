from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns

from django.conf.urls.static import static
from NurseEqServices import settings
from django.views.i18n import set_language


urlpatterns = [
      path('i18n/setlang/', set_language, name='set_language'),
      path('i18n/', include('django.conf.urls.i18n')),
      path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('', include('main.urls')),
    path('', include('appointment.urls')),
    path('user/', include('user.urls')),
    path('equipment-res/', include('equipmentReservation.urls')),
    path('accounts/', include('allauth.urls')),
)
#Mohammad@079
