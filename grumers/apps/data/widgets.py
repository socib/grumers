from django.contrib.gis.forms.widgets import OSMWidget


class GrumersOSMWidget(OSMWidget):
    """
    An OpenLayers/OpenStreetMap-based widget.
    """
    template_name = 'gis/openlayers-osm.html'
    default_lon = 2.58
    default_lat = 39.50

    class Media:
        extend = False
        js = (
            'js/open_layers/OpenLayers.js',
            'js/open_layers/OpenStreetMap.js',
            'gis/js/OLMapWidget.js',
        )

    def render(self, name, value, attrs=None):
        default_attrs = {
            'default_lon': self.default_lon,
            'default_lat': self.default_lat,
        }
        if attrs:
            default_attrs.update(attrs)
        return super(GrumersOSMWidget, self).render(name, value, default_attrs)
