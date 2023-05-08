import datetime
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from appointment.forms import AppointmentForm, EmergencyAppointmentForm
from appointment.models import Appointment
from equipmentReservation.models import EquipmentReservation
from user.models import Staff


@method_decorator(login_required, name="dispatch")
class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'partials/appointment/create_appointment.html'
    success_url = reverse_lazy('thanks-page')

    # success_message = _('Your request sent successfully.')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'BOOKED'
        form.instance.type = 'NORMAL'
        form.instance.doctor = Staff.objects.filter(city=self.request.POST['city']).order_by('?')[0]
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class UserAppointmentUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'partials/appointment/update_appointment.html'
    model = Appointment
    form_class = AppointmentForm
    success_message = _('Your appointment updated successfully.')
    success_url = reverse_lazy('list-user-appointment')


@method_decorator(login_required, name="dispatch")
class UserAppointment(ListView):
    model = Appointment
    template_name = 'partials/appointment/list_user_appointment.html'

    # paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserAppointment, self).get_context_data()
        context['appointment'] = self.model.objects.filter(user=self.request.user)
        context['eq_reservation'] = EquipmentReservation.objects.filter(user=self.request.user)
        return context


@method_decorator(login_required, name="dispatch")
class UserAppointmentDeleteView(SuccessMessageMixin, DeleteView):
    template_name = 'partials/delete_page.html'
    model = Appointment
    success_message = _('Your appointment have been delete successfully.')
    success_url = reverse_lazy('list-user-appointment')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(UserAppointmentDeleteView, self).delete(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class ThanksPage(TemplateView):
    model = Appointment
    template_name = 'templates/partials/appointment/thanks_page.html'


@method_decorator(login_required, name="dispatch")
class EmergencyAppointmentCreateView(SuccessMessageMixin, CreateView):
    model = Appointment
    form_class = EmergencyAppointmentForm
    template_name = 'partials/appointment/emergency_appointment.html'
    success_url = reverse_lazy('thanks-page')

    # success_message = _('Your request sent successfully.')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'APPROVED'
        form.instance.session_time = datetime.datetime.now().time()
        form.instance.doctor = Staff.objects.filter(city=self.request.POST['city']).order_by('?')[0]
        form.instance.type = 'EMERGENCY'
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(EmergencyAppointmentCreateView, self).get_form_kwargs()
        user = self.request.user

        if user:
            kwargs['user'] = user

        return kwargs
