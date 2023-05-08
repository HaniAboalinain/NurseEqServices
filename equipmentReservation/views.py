from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, TemplateView, DeleteView
from equipmentReservation.forms import EquipmentReservationForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from equipmentReservation.models import EquipmentReservation
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages


# Create your views here.

@method_decorator(login_required, name="dispatch")
class EquipmentReservationCreateView(CreateView):
    model = EquipmentReservation
    template_name = 'templates/partials/eq_reservation/create_eq_reservation.html'
    form_class = EquipmentReservationForm
    success_url = reverse_lazy('thanks-page')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # form.instance.status = 'BOOKED'

        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class EquipmentReservationUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'templates/partials/eq_reservation/create_eq_reservation.html'
    model = EquipmentReservation
    form_class = EquipmentReservationForm
    success_message = _('Your Equipment reservation updated successfully.')
    success_url = reverse_lazy('list-user-appointment')


@method_decorator(login_required, name="dispatch")
class ThanksPage(TemplateView):
    model = EquipmentReservation
    template_name = 'templates/partials/appointment/thanks_page.html'


@method_decorator(login_required, name="dispatch")
class EquipmentReservationDeleteView(SuccessMessageMixin, DeleteView):
    template_name = 'partials/delete_page.html'
    model = EquipmentReservation
    success_message = _('Your Equipment reservation have been delete successfully.')
    success_url = reverse_lazy('list-user-appointment')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EquipmentReservationDeleteView, self).delete(request, *args, **kwargs)
