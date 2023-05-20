from crispy_forms.helper import FormHelper
from django import forms
from crispy_forms.layout import Layout, Div, ButtonHolder, Submit, HTML
from django.forms import ModelChoiceField
from django.utils.translation import ugettext_lazy as _
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator

from equipmentReservation.models import EquipmentReservation, PAYMENT_METHOD
from equipment.models import Equipment


class EquipmentChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.name} \u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0 {obj.price} JD/DAY'


class DateInput(forms.DateInput):
    input_type = 'date'


class MonthYearWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.Select(attrs=attrs, choices=[(str(i), str(i)) for i in range(1, 13)]),  # Month
            forms.Select(attrs=attrs, choices=[(str(i), str(i)) for i in range(2023, 2030)])  # Year
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.month, value.year]
        return [None, None]

    def format_output(self, rendered_widgets):
        return ' / '.join(rendered_widgets)


class MonthYearField(forms.MultiValueField):
    widget = MonthYearWidget

    def __init__(self, *args, **kwargs):
        fields = [
            forms.IntegerField(),
            forms.IntegerField()
        ]
        super().__init__(fields, *args, **kwargs)

    def compress(self, values):
        if values:
            month, year = values
            if month and year:
                return date(year, month, 1)
        return None


class EquipmentReservationForm(forms.ModelForm):
    # eq_name = forms.ModelChoiceField(queryset=Equipment.objects, empty_label=_("--- Please Choose Equipment ---"))
    eq_name = EquipmentChoiceField(queryset=Equipment.objects, empty_label=_("--- Please Choose Equipment ---"))
    eq_count = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD, widget=forms.RadioSelect, initial='cash')
    visa_exp_date = MonthYearField()

    class Meta:
        model = EquipmentReservation
        fields = ['eq_name', 'eq_count', 'duration_from', 'duration_to', 'price', 'id_photo', 'delivery_way',
                  'city', 'address', 'privacy_policy', 'payment_method', 'card_number', 'visa_exp_date', 'cvv']
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
            Div(
                Div("eq_name", css_class="eq_name col-md-6 input-block"),
                Div("eq_count", css_class="count col-md-6 input-block"),
                Div("duration_from", css_class="col-md-6 input-block"),
                Div("duration_to", css_class="col-md-6 input-block"),
                Div("address", css_class="col-md-12 input-block"),
                Div("city", css_class="col-md-6 input-block"),
                Div("delivery_way", css_class="col-md-6 input-block"),
                Div("id_photo", css_class="col-md-6 input-block"),
                Div("price", css_class=" price col-md-6 input-block"),
                Div("privacy_policy", HTML(
                    '<ul><li> Policy 1 </li><li> Policy 2 </li><li> Policy 3 </li></ul>'),
                    css_class="col-md-6 input-block"),

                Div(ButtonHolder(Submit('submit', _('Submit'), css_class='mt-2 w-25'),
                                 css_class='d-flex justify-content-center'), ),
                css_class="row eq_name col-md-8"),

            Div(Div("payment_method", css_class="payment-method col-md-12 input-block"),
                Div(Div(HTML('<h3 class="text-primary">Card Info.</h3>'), "card_number",
                        css_class="col-md-12 input-block"),
                    Div("visa_exp_date", css_class="col-md-12 input-block"),
                    Div("cvv", css_class="col-md-12 input-block"),
                    css_class="visa-info col-md-12 input-block d-none", css_id="visa-info-section"),
                css_class="row eq_name col-md-4")

        )

    def clean(self):
        clean = super(EquipmentReservationForm, self).clean()
        clean['duration_from'] = self.cleaned_data['duration_from']
        clean['duration_to'] = self.cleaned_data['duration_to']

        if clean['duration_from'] > clean['duration_to']:
            raise forms.ValidationError("The duration from field can't be greater than duration to!")

        clean['eq_count'] = self.cleaned_data['eq_count']
        qty = Equipment.objects.get(id=self.data['eq_name']).quantity
        if clean['eq_count'] > qty:
            raise forms.ValidationError("The available quantity in the inventory is" + " " + str(qty))

        # clean['session_time'] = self.cleaned_data['session_time']
        # if Appointment.objects.filter(date=clean['date'], session_time=clean['session_time'],
        #                               status='PENDING' or 'APPROVED' or 'UNAVAILABLE').exists():
        #     raise forms.ValidationError("This time is not available, please Choose another time!")

        return clean

    def clean_privacy_policy(self):
        privacy_policy = self.cleaned_data.get('privacy_policy')
        if not privacy_policy:
            raise forms.ValidationError(_("Please, Agree the policy before you submit the request."))
        return privacy_policy
