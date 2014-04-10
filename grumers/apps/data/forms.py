from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from bootstrap3_datetime.widgets import DateTimePicker

from datetime import datetime
import models


class JellyfishObservationUpdateForm(forms.ModelForm):
    button_prefix = _("Update")

    class Meta:
        model = models.JellyfishObservation
        fields = [
            'date_observed',
            'observation_station',
            'jellyfish_specie',
            'quantity',
            'remarks',
        ]

    def clean(self):
        cleaned_data = super(JellyfishObservationUpdateForm, self).clean()
        if cleaned_data['quantity'] > 0 and not cleaned_data['jellyfish_specie']:
            msg = _('Fill jellyfish specie or set quantity to none')
            self._errors["quantity"] = self.error_class([msg])
            self._errors["jellyfish_specie"] = self.error_class([msg])
            del cleaned_data["quantity"]
            del cleaned_data["jellyfish_specie"]

        if cleaned_data['quantity'] == 0 and cleaned_data['jellyfish_specie']:
            msg = _('Fill quantity or set specie to none')
            self._errors["quantity"] = self.error_class([msg])
            self._errors["jellyfish_specie"] = self.error_class([msg])
            del cleaned_data["quantity"]
            del cleaned_data["jellyfish_specie"]
        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-5'
        submit_button = Submit(
            css_class='btn btn-primary',
            name='observation',
            value=_('%s observation') % self.button_prefix,
            type='submit')
        next_station_button = Submit(
            css_class='btn btn-primary',
            name='next_station',
            value=_('Create observation and continue with next station'),
            type='submit')
        cancel_button = Submit(
            css_class='btn',
            name='cancel',
            value=_('Cancel'),
            type='submit')

        if isinstance(self, JellyfishObservationCreateForm):
            self.helper.add_input(next_station_button)

        self.helper.add_input(submit_button)
        self.helper.add_input(cancel_button)

        station = kwargs.pop('station', None)
        route = kwargs.pop('route', None)
        super(JellyfishObservationUpdateForm, self).__init__(*args, **kwargs)
        self.fields['date_observed'].widget = DateTimePicker(
            options={"format": "YYYY-MM-DD HH:mm",
                     "pickSeconds": False})
        self.fields['date_observed'].initial = datetime.now()
        self.fields['remarks'].widget.attrs['rows'] = 4
        self.fields['jellyfish_specie'].empty_label = _('None')
        if station:
            self.fields['observation_station'].initial = station

        station_queryset = self.fields['observation_station'].queryset
        if route:
            station_queryset = station_queryset.filter(observation_route__id=route)
        self.fields['observation_station'].queryset = station_queryset

        self.fields['quantity'].widget = forms.Select(
            choices=models.JellyfishObservation.QUANTITY_CHOICES)


class JellyfishObservationCreateForm(JellyfishObservationUpdateForm):

    button_prefix = _("Create")

    def __init__(self, *args, **kwargs):
        super(JellyfishObservationCreateForm, self).__init__(*args, **kwargs)


class JellyfishObservationFilterForm(forms.Form):

    jellyfish_specie = forms.ModelChoiceField(
        models.JellyfishSpecie.objects.all(),
        label=_('specie'),
        empty_label=_('Specie: all'),
        required=False)
    created_by = forms.ModelChoiceField(
        User.objects.all(),
        label=_('created by'),
        empty_label=_('User: all'),
        required=False)
    route = forms.ModelChoiceField(
        models.ObservationRoute.objects.all(),
        label=_('observation route'),
        empty_label=_('Route: all'),
        required=False)
    station = forms.ModelChoiceField(
        models.ObservationStation.objects.all(),
        label=_('observation station'),
        empty_label=_('Station: all'),
        required=False)
    source = forms.MultipleChoiceField(
        models.JellyfishObservation.SOURCE_CHOICES, label=_('source'), required=False)
    from_date = forms.DateField(label=_('from date'), required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        filter_button = Submit(
            'filter',
            css_class='btn btn-default',
            value=_('Filter'),
            type='submit')
        self.helper.add_input(filter_button)

        user = kwargs.pop('user')
        route = kwargs.pop('route')
        super(JellyfishObservationFilterForm, self).__init__(*args, **kwargs)
        self.fields['from_date'].widget.format = '%d/%m/%Y'
        self.fields['from_date'].input_formats = ['%d/%m/%Y']
        if not user.has_perm('data.can_list_others_jellyfishobservations'):
            self.fields['created_by'].queryset = User.objects.filter(
                id__in=[user.id])
        if route:
            qs = self.fields['station'].queryset
            self.fields['station'].queryset = qs.filter(observation_route_id=route)

        for key in self.fields:
            self.fields[key].label = self.fields[key].label.capitalize()
