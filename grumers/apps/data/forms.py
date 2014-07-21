 # coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, ButtonHolder
from crispy_forms.bootstrap import StrictButton
from bootstrap3_datetime.widgets import DateTimePicker
from grumers.utils.crispy import ExtendedLayout
from grumers.utils.widgets import BeachDateTimePicker

import models


class JellyfishObservationUpdateForm(forms.ModelForm):
    button_prefix = _("Update")

    class Meta:
        model = models.JellyfishObservation
        fields = [
            'date_observed',
            'observation_station',
            'quantity',
            'jellyfish_specie',
            'picture',
            'remarks',
            'sting_incidents',
            'total_incidents',
        ]

    def clean(self):
        cleaned_data = super(JellyfishObservationUpdateForm, self).clean()
        if cleaned_data['quantity'] > 0 and not cleaned_data['jellyfish_specie']:
            msg = _('Fill jellyfish specie or set quantity to none')
            self._errors["quantity"] = self.error_class([msg])
            self._errors["jellyfish_specie"] = self.error_class([msg])
            del cleaned_data["quantity"]
            del cleaned_data["jellyfish_specie"]

        elif cleaned_data['quantity'] == 0 and cleaned_data['jellyfish_specie']:
            msg = _('Fill quantity or set specie to none')
            self._errors["quantity"] = self.error_class([msg])
            self._errors["jellyfish_specie"] = self.error_class([msg])
            del cleaned_data["quantity"]
            del cleaned_data["jellyfish_specie"]

        if ['sting_incidents', 'total_incidents'] in cleaned_data.keys():
            if cleaned_data['sting_incidents'] > cleaned_data['total_incidents']:
                msg = _('Sting incidents can not be greater than total incidents')
                self._errors["sting_incidents"] = self.error_class([msg])
                self._errors["jellyfish_specie"] = self.error_class([msg])
                del cleaned_data["total_incidents"]
                del cleaned_data["total_incidents"]
        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-5'
        submit_button = StrictButton(
            '<span class="glyphicon glyphicon-save"></span> ' +
            _('%s observation') % self.button_prefix,
            css_class='btn btn-primary',
            name='observation',
            value='submit_observation',
            type='submit')
        next_station_button = StrictButton(
            _('%s Create observation and continue with next station') %
            '<span class="glyphicon glyphicon-arrow-right"></span>',
            css_class='btn btn-primary',
            name='next_station',
            value='submit_next_station',
            type='submit')
        cancel_button = StrictButton(
            _('Cancel'),
            css_class='btn',
            name='cancel',
            value='cancel',
            type='submit')

        if not isinstance(self, JellyfishObservationCreateForm):
            next_station_button = None

        self.helper.add_layout(
            ExtendedLayout(
                Fieldset(
                    _('When / Where'),
                    'date_observed',
                    'observation_station',
                ),
                Fieldset(
                    _('Jellyfish observation'),
                    'quantity',
                    'jellyfish_specie',
                    'picture',
                    'remarks',
                ),
                Fieldset(
                    _('Incidents during the day'),
                    'sting_incidents',
                    'total_incidents',
                    css_class='incidents'
                ),
                ButtonHolder(
                    next_station_button,
                    submit_button,
                    cancel_button,
                ),
            )
        )

        station = kwargs.pop('station', None)
        route = kwargs.pop('route', None)
        super(JellyfishObservationUpdateForm, self).__init__(*args, **kwargs)
        self.fields['remarks'].widget.attrs['rows'] = 4
        self.fields['jellyfish_specie'].widget.attrs['class'] = 'ignore-select2'
        self.fields['jellyfish_specie'].empty_label = _('None')
        if station:
            self.fields['observation_station'].initial = station

        station_queryset = self.fields['observation_station'].queryset
        if route:
            station_queryset = station_queryset.filter(observation_route=route)
        station_queryset = station_queryset.filter(disabled=False)
        self.fields['observation_station'].queryset = station_queryset

        self.fields['quantity'].widget = forms.Select(
            choices=models.JellyfishObservation.QUANTITY_CHOICES)

        # Remove incidents if route is not of a beach
        if not route or route.route_type != 'B':
            self.fields.pop('sting_incidents')
            self.fields.pop('total_incidents')
            self.helper.layout.remove_by_fieldname('sting_incidents')
            self.helper.layout.remove_by_fieldname('total_incidents')
            self.fields['date_observed'].widget = DateTimePicker(
                options={"format": "YYYY-MM-DD HH:mm",
                         "pickSeconds": False})
        else:
            self.fields['date_observed'].widget = BeachDateTimePicker(
                options={"format": "YYYY-MM-DD HH:mm",
                         "pickSeconds": False})


class JellyfishObservationCreateForm(JellyfishObservationUpdateForm):

    button_prefix = _("Create")

    def __init__(self, *args, **kwargs):
        super(JellyfishObservationCreateForm, self).__init__(*args, **kwargs)


class JellyfishObservationBulkCreateForm(forms.Form):
    observation_date = forms.DateField(label=_('observation date'), required=True)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-5'
        submit_button = StrictButton(
            '<span class="glyphicon glyphicon-save"></span> ' +
            unicode(_('Create bulk no-observations')),
            css_class='btn btn-primary',
            name='observation',
            value='submit_observation',
            type='submit')
        cancel_button = StrictButton(
            _('Cancel'),
            css_class='btn',
            name='cancel',
            value='cancel',
            type='submit')

        self.helper.add_layout(
            ExtendedLayout(
                'observation_date',
                ButtonHolder(
                    submit_button,
                    cancel_button,
                ),
            )
        )
        super(JellyfishObservationBulkCreateForm, self).__init__(*args, **kwargs)
        self.fields['observation_date'].widget.format = '%d/%m/%Y'
        self.fields['observation_date'].input_formats = ['%d/%m/%Y']

        for key in self.fields:
            self.fields[key].label = self.fields[key].label.capitalize()


class JellyfishObservationFilterForm(forms.Form):

    jellyfish_specie = forms.ModelChoiceField(
        models.JellyfishSpecie.objects.filter(disabled=False),
        label=_('specie'),
        empty_label=_('Specie: all'),
        required=False)
    created_by = forms.ModelChoiceField(
        User.objects.all(),
        label=_('created by'),
        empty_label=_('User: all'),
        required=False)
    route = forms.ModelChoiceField(
        models.ObservationRoute.objects.filter(disabled=False),
        label=_('observation route'),
        empty_label=_('Route: all'),
        required=False)
    station = forms.ModelChoiceField(
        models.ObservationStation.objects.filter(disabled=False),
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
        export_button = Submit(
            'export',
            css_class='btn btn-info',
            value=_('Export'),
            type='submit')
        self.helper.add_input(export_button)

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
            self.fields['station'].queryset = qs.filter(observation_route=route)
            self.fields['route'].widget.attrs['readonly'] = True

        if not user.is_superuser:
            self.fields['route'].queryset = models.ObservationRoute.objects.filter(
                groups__in=user.groups.all())

        for key in self.fields:
            self.fields[key].label = self.fields[key].label.capitalize()
