import datetime
from crispy_forms.helper import FormHelper
from django import forms
from crispy_forms.layout import Layout, Div, ButtonHolder, Submit
from django.utils.translation import ugettext_lazy as _

from appointment.models import Appointment, WORKING_HOURS
from user.models import Staff


class DateInput(forms.DateInput):
    input_type = 'date'


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['major', 'date', 'city', 'session_time', 'message']
        widgets = {
            'date': DateInput(),
            'message': forms.widgets.Textarea(attrs={'placeholder': _('Write your notes here (optional)')}),
        }

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            # Div(
            Div("city", css_class="col-md-6 input-block"),
            Div("major", css_class="col-md-6 input-block"),
            Div("date", css_class="col-md-6 input-block"),
            Div("session_time", css_class="col-md-6 input-block"),
            Div("message", css_class="col-md-12"),
            Div(ButtonHolder(Submit('submit', _('Submit'), css_class='mt-2 w-25'),
                             css_class='d-flex justify-content-center'), )
        )

    def clean(self):
        clean = super(AppointmentForm, self).clean()
        clean['date'] = self.cleaned_data['date']
        if clean['date'] < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")

        clean['session_time'] = self.cleaned_data['session_time']
        if Appointment.objects.filter(date=clean['date'], session_time=clean['session_time'],
                                      status='PENDING' or 'APPROVED' or 'UNAVAILABLE').exists():
            raise forms.ValidationError("This time is not available, please Choose another time!")

        return clean


# ---------------------------------------

class EmergencyAppointmentForm(forms.ModelForm):
    user = forms.CharField()
    phone = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = Appointment
        fields = ['city', 'date', 'message']
        widgets = {
            'message': forms.widgets.Textarea(attrs={'placeholder': _('Write your note here (optional)')}),
        }

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            self.user = kwargs.pop('user', None)

        super(EmergencyAppointmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.fields['user'].widget.attrs['readonly'] = True
        self.fields['phone'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['date'].widget.attrs['readonly'] = True
        self.fields['date'].initial = datetime.date.today()
        self.fields['user'].initial = self.user
        self.fields['phone'].initial = self.user.phone
        self.fields['email'].initial = self.user.email
        self.helper.layout = Layout(
            # Div(
            Div("user", css_class="col-md-4 input-block"),
            Div("phone", css_class="col-md-4 input-block"),
            Div("email", css_class="col-md-4 input-block"),
            Div("date", css_class="col-md-6 input-block"),
            Div("city", css_class="col-md-6 input-block"),
            Div("message", css_class="col-md-12"),
            Div(ButtonHolder(Submit('submit', _('Submit'), css_class='mt-2 w-25'),
                             css_class='d-flex justify-content-center'), )
        )
