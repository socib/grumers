from django.contrib.gis import admin
from django import forms
from django.db.models import TextField
from ckeditor.widgets import CKEditorWidget

import models


class AuditModelAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by', 'updated_by',)
    formfield_overrides = {TextField: {'widget': CKEditorWidget(config_name='default')}, }

    def save_model(self, request, obj, form, change):
        obj.save(user=request.user)


class JellyfishSpeciesAdmin(AuditModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'common_name',)


class ObservationRouteAdmin(AuditModelAdmin):
    list_display = ('name',)


class ObservationStationAdmin(AuditModelAdmin):
    list_display = ('name', 'observation_route', 'order')
    list_filter = ['observation_route']
    openlayers_url = 'js/open_layers/OpenLayers.js'
    default_lon = 2.58
    default_lat = 39.50
    default_zoom = 9


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
