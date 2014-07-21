from django.contrib.gis import admin
from django import forms
from django.db.models import TextField
from ckeditor.widgets import CKEditorWidget

import models
import widgets


class AuditModelAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by', 'updated_by',)
    formfield_overrides = {TextField: {'widget': CKEditorWidget(
        config_name='default')}, }

    def save_model(self, request, obj, form, change):
        obj.save(user=request.user)


class JellyfishSpeciesAdmin(AuditModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'common_name', 'active',)


class ObservationRouteAdmin(AuditModelAdmin):
    list_display = ('name', 'group_list', 'active',)
    filter_horizontal = ('groups',)

    def save_model(self, request, obj, form, change):
        if form.cleaned_data['route_type'] == 'B' and not form.cleaned_data['groups']:
            route = form.save(commit=False)
            form.cleaned_data['groups'] = models.get_default_beach_groups(route)

        super(ObservationRouteAdmin, self).save_model(request, obj, form, change)


class ObservationStationAdmin(AuditModelAdmin):
    list_display = ('observation_route', 'name', 'position_coordinates',
                    'order', 'active',)
    list_filter = ['observation_route']
    # openlayers_url = 'js/open_layers/OpenLayers.js'

    def get_form(self, request, obj=None, **kwargs):
        # Change position widget
        form = super(ObservationStationAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['position'].widget = widgets.GrumersOSMWidget(
            attrs={'map_width': 800,
                   'map_height': 500})
        return form


class JellyfishObservationAdmin(AuditModelAdmin):
    list_display = ('date_observed', 'jellyfish_specie', 'quantity', 'source',
                    'created_by')
    list_filter = ['observation_station', 'jellyfish_specie', 'created_by',
                   'date_observed']

    def get_form(self, request, obj=None, **kwargs):
        # Change quantity widget
        form = super(JellyfishObservationAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['quantity'].widget = forms.Select(
            choices=models.JellyfishObservation.QUANTITY_CHOICES)
        return form

admin.site.register(models.JellyfishSpecie, JellyfishSpeciesAdmin)
admin.site.register(models.ObservationRoute, ObservationRouteAdmin)
admin.site.register(models.ObservationStation, ObservationStationAdmin)
admin.site.register(models.JellyfishObservation, JellyfishObservationAdmin)
