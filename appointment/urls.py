from django.urls import path

from appointment.views import AppointmentCreateView, UserAppointment, UserAppointmentUpdateView, ThanksPage, \
    EmergencyAppointmentCreateView, UserAppointmentDeleteView

urlpatterns = [
    path('create/appointment', AppointmentCreateView.as_view(), name='create-appointment'),
    path('user/update/appointment/<int:pk>', UserAppointmentUpdateView.as_view(), name='user-update-appointment'),
    path('list/user/appointemt', UserAppointment.as_view(), name='list-user-appointment'),
    path('delete/page/<int:pk>', UserAppointmentDeleteView.as_view(), name='delete-page'),
    path('thank-you', ThanksPage.as_view(), name='thanks-page'),

    path('create/emergency/appointment', EmergencyAppointmentCreateView.as_view(), name='create-emergency-appointment'),
]
