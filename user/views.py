# Create your views here.
from django.views.generic import UpdateView, DetailView, TemplateView, ListView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from user.forms import UserUpdateForm, NurseRequestForm
from user.models import CustomUser, Staff, NurseRequest
from appointment.models import Appointment
from django.contrib import messages


@method_decorator(login_required, name="dispatch")
class StaffDashboardView(TemplateView):
    template_name = 'staff/home.html'

    def get_object(self, queryset=None):
        queryset = self.model.objects.filter(id=self.request.user.id)
        return super(StaffDashboardView, self).get_object(queryset)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StaffDashboardView, self).get_context_data()
        context['nurse_reservations'] = Appointment.objects.filter(doctor__user_id=self.request.user.id)
        return context


class StaffListView(ListView):
    template_name = 'staff/doctors_list.html'
    model = Staff


@method_decorator(login_required, name="dispatch")
class UserDetailView(DetailView):
    template_name = 'user/user_information.html'
    model = CustomUser

    def get_object(self, queryset=None):
        queryset = self.model.objects.filter(id=self.request.user.id)
        return super(UserDetailView, self).get_object(queryset)


@method_decorator(login_required, name="dispatch")
class UserUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'user/user_edit_info.html'
    model = CustomUser
    form_class = UserUpdateForm
    success_message = 'Your information updated successfully.'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        queryset = self.model.objects.filter(id=self.request.user.id)
        return super(UserUpdateView, self).get_object(queryset)


@method_decorator(login_required, name="dispatch")
class NurseRequestCreateView(SuccessMessageMixin, CreateView):
    template_name = 'staff/nurse_request.html'
    model = NurseRequest
    form_class = NurseRequestForm
    success_message = 'Thanks you, We will review your request and get back to you as soon as possible.'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if not self.model.objects.filter(user=self.request.user).exists():
            super(NurseRequestCreateView, self).form_valid(form)
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'You already have a pending nurse request, please wait until we get back to you!',
                       extra_tags='danger')
        return response


class DoctorDetailView(DetailView):
    template_name = 'staff/doctor_info.html'
    model = Staff

