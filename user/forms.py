from django import forms
from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import SignupForm as AbstractSignupForm

from user.models import CustomUser, Staff, NurseRequest
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, ButtonHolder, Submit, HTML


class DateInput(forms.DateInput):
    input_type = 'date'


class SignupForm(AbstractSignupForm):
    first_name = forms.CharField(max_length=10)
    last_name = forms.CharField(max_length=10)
    phone = forms.CharField(max_length=10, label='phone')
    birth_date = forms.DateField(widget=DateInput())
    insurance = forms.NullBooleanField()
    agreement = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-md-4 create-label'
        # self.helper.field_class = 'col-md-5'
        self.helper.layout = Layout(
            Div(
                Div("first_name", css_class="col-md-6"),
                Div("last_name", css_class="col-md-6"),
                Div("email", css_class="col-md-12"),
                Div("phone", css_class="col-md-6"),
                Div("birth_date", css_class="col-md-6"),
                Div("password1", css_class="col-md-6"),
                Div("password2", css_class="col-md-6"),
                Div("agreement", HTML(
                    '<small class=" text-muted">I read and agree all <a href="#">terms and condition</a> for the Home of speech website.</small>'),
                    css_class="col-md-12 mt-3 mb-3"),

                css_class="row d-flex"
            ))

    def clean(self):
        clean = super(SignupForm, self).clean()
        clean['phone'] = self.cleaned_data['phone']
        if CustomUser.objects.filter(phone=clean['phone']).exists():
            self.add_error('phone', 'This phone is already exist, please enter another phone number.')

        return clean

    def save(self, request):
        user = super(SignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.birth_date = self.cleaned_data['birth_date']
        user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'birth_date', 'agreement']
        widgets = {
            'birth_date': DateInput(),
        }


class NurseRequestForm(forms.ModelForm):
    class Meta:
        model = NurseRequest
        fields = ['bio', 'exp_year', 'city', 'certificate', 'major', 'photo']

    def __init__(self, *args, **kwargs):
        super(NurseRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.attrs['enctype'] = 'multipart/form-data'  # add this line
        self.helper.layout = Layout(
            Div(
                Div("major", css_class="col-md-4"),
                Div("exp_year", css_class="col-md-4"),
                Div("city", css_class="col-md-4"),
                Div("photo", css_class="col-md-6"),
                Div("certificate", css_class="col-md-6"),
                Div("bio", css_class="col-md-12"),
                Div(ButtonHolder(Submit('submit', _('Submit'), css_class='mt-2 w-25'),
                                 css_class='d-flex justify-content-center')),
                css_class="row d-flex"
            ))

    # def clean(self):
    #     clean = super(NurseRequestForm, self).clean()
    #     """
    #     clean['phone'] = self.cleaned_data['phone']
    #     if CustomUser.objects.filter(phone=clean['phone']).exists():
    #         self.add_error('phone', 'This phone is already exist, please enter another phone number.')
    #     """
    #     return clean
