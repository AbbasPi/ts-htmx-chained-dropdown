from django.urls import reverse
from .models import Manufacturer, Model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Button, Submit
from django import forms
from dynamic_forms import DynamicField, DynamicFormMixin


class ManufacturerForm(DynamicFormMixin, forms.Form):

    manufacturers = forms.ModelChoiceField(queryset=Manufacturer.objects.all(),
                                           required=False)

    model = DynamicField(
        forms.ModelChoiceField,
        queryset=lambda form: Model.objects.filter(manufacturer=form['manufacturers'].value()),
        required=False,
    )

    price = forms.IntegerField(
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('manufacturers', css_class='included',
                      **{'hx-get': reverse('index'), 'hx-target': '#form', 'hx-trigger': 'change',
                         'hx-swap': 'outerHTML'}),
                    ),
            Div(
                Field('model', css_class='form-control',
                      **{'hx-get': reverse('index'), 'hx-target': '#form',
                         'hx-swap': 'outerHTML', 'hx-include': '.included'},
                      ),
                css_class='form-group'
            ),
            Div(
                Field('price'),

            ),
            Div(
                Submit(
                    'submit', 'Submit', css_class='btn btn-primary', type='submit',
                    **{'hx-post': reverse('add'), 'hx-target': 'ul', 'hx-swap': 'beforeend'}

                )
            ))


