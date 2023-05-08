import datetime
from crispy_forms.helper import FormHelper
from django import forms
from crispy_forms.layout import Layout, Div, ButtonHolder, Submit
from django.forms import ModelChoiceField
from django.utils.translation import ugettext_lazy as _

from equipmentReservation.models import EquipmentReservation
from equipment.models import Equipment


class EquipmentChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.name}  ------------- price: {obj.price}'


class DateInput(forms.DateInput):
    input_type = 'date'


class EquipmentReservationForm(forms.ModelForm):
    # eq_name = forms.ModelChoiceField(queryset=Equipment.objects, empty_label=_("--- Please Choose Equipment ---"))
    eq_name = EquipmentChoiceField(queryset=Equipment.objects, empty_label=_("--- Please Choose Equipment ---"))

    class Meta:
        model = EquipmentReservation
        fields = ['eq_name', 'eq_count', 'duration_from', 'duration_to', 'price', 'id_photo',
                  'delivery_way', 'city', 'address', 'privacy_policy']
        widgets = {
            'duration_from': DateInput(),
            'duration_to': DateInput(),
            # 'message': forms.widgets.Textarea(attrs={'placeholder': _('Write your note here (optional)')}),
        }

    def __init__(self, *args, **kwargs):
        super(EquipmentReservationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.fields['price'].widget.attrs['readonly'] = True
        self.fields['eq_count'].initial = 1
        self.helper.layout = Layout(
            # Div(
            Div("eq_name", css_class="eq_name col-md-6 input-block"),
            Div("eq_count", css_class="count col-md-6 input-block"),
            Div("city", css_class="col-md-6 input-block"),
            Div("address", css_class="col-md-6 input-block"),
            Div("duration_from", css_class="col-md-4 input-block"),
            Div("duration_to", css_class="col-md-4 input-block"),
            Div("delivery_way", css_class="col-md-4 input-block"),
            Div("id_photo", css_class="col-md-4 input-block"),
            Div("price", css_class=" price col-md-6 input-block"),
            Div("privacy_policy", css_class="col-md-6 input-block"),

            Div(ButtonHolder(Submit('submit', _('Submit'), css_class='mt-2 w-25'),
                             css_class='d-flex justify-content-center'), )
        )

    def clean(self):
        clean = super(EquipmentReservationForm, self).clean()
        """
        clean['date'] = self.cleaned_data['date']
        if clean['date'] < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")

        clean['session_time'] = self.cleaned_data['session_time']
        if Appointment.objects.filter(date=clean['date'], session_time=clean['session_time'],
                                      status='PENDING' or 'APPROVED' or 'UNAVAILABLE').exists():
            raise forms.ValidationError("This time is not available, please Choose another time!")
        """
        return clean
