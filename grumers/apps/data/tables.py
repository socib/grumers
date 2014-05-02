import django_tables2 as tables
from django.template import Context
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.geos import GEOSGeometry
from django.utils import simplejson
import models


class JellyfishObservationTable(tables.Table):
    # LinkColum does not work with localeurl
    # date_observed = tables.LinkColumn('data_observation_update', args=[A('pk')])
    date_observed = tables.TemplateColumn(
        """<a href="{% url 'data_observation_update' record.pk %}">
            {{ record.date_observed|date:'d/m/Y H:i'}}
            </a>
        """)
    observation_station = tables.Column()
    jellyfish_specie = tables.Column()
    quantity = tables.Column()
    source = tables.Column()
    created_by = tables.Column()
    route = None

    def __init__(self, *args, **kwargs):
        self.route = kwargs.pop('route', None)
        super(JellyfishObservationTable, self).__init__(*args, **kwargs)
        if self.route:
            self.context = Context({'route': self.route})
            self.base_columns['date_observed'].template_code = """
            <a href="{% url 'data_route_observation_update' route.pk record.pk %}">
            {{ record.date_observed|date:'d/m/Y H:i'}}
            </a>
            """

    class Meta:
        model = models.JellyfishObservation
        attrs = {"class": "table table-striped"}
        sequence = fields = (
            'date_observed',
            'observation_station',
            'jellyfish_specie',
            'quantity',
            'created_by',
            'source',
        )

    @property
    def verbose_name(self):
        if getattr(self, 'display_name', None):
            return self.display_name
        return self.Meta.model._meta.verbose_name_plural.title()


class JellyfishObservationExportTable(JellyfishObservationTable):
    date_observed = tables.Column()

    def __init__(self, *args, **kwargs):
        self.route = kwargs.pop('route', None)
        super(JellyfishObservationExportTable, self).__init__(*args, **kwargs)


class JellyfishObservationAggregatedTable(tables.Table):
    x = tables.Column(empty_values=())
    y = tables.Column(empty_values=())
    sum_quantity = tables.Column()

    def render_x(self, record):
        return "{:.6f}".format(GEOSGeometry(record['observation_station__position']).x)

    def render_y(self, record):
        return "{:.6f}".format(GEOSGeometry(record['observation_station__position']).y)

    @property
    def json(self):
        data = []
        for record in self.rows:
            data.append({
                'lat': float(record['y']),
                'lng': float(record['x']),
                'count': record['sum_quantity']})
        return simplejson.dumps(data)

    def __init__(self, *args, **kwargs):
        self.route = kwargs.pop('route', None)
        super(JellyfishObservationAggregatedTable, self).__init__(*args, **kwargs)

    class Meta:
        attrs = {"class": "table table-striped"}


class ObservationRouteTable(tables.Table):
    name = tables.TemplateColumn(
        """<a href="{% url 'data_route_observation_list' record.pk %}">
            {{ record.name }}
            </a>
        """)
    description = tables.TemplateColumn(
        '{{ record.description|truncatewords_html:20|safe }}')
    create_observation = tables.TemplateColumn(
        """{% load i18n %}
           <a class="btn btn-primary"
            href="{% url 'data_route_observation_create' record.pk %}">
            <i class="glyphicon glyphicon-plus"></i>
            {% trans 'Add' %} {% trans 'observation' %}
            </a>""",
        verbose_name=_('create observation'))

    class Meta:
        model = models.ObservationRoute
        attrs = {"class": "table table-striped"}
        fields = (
            'name',
            'description',
        )
        sequence = (
            'name',
            'description',
            'create_observation',
        )
