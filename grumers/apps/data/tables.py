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
        attrs = {"class": "table table-striped table-condensed"}
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
    observation_route = tables.Column(
        accessor='observation_station.observation_route.name')

    def __init__(self, *args, **kwargs):
        self.route = kwargs.pop('route', None)
        super(JellyfishObservationExportTable, self).__init__(*args, **kwargs)

    class Meta:
        model = models.JellyfishObservation
        fields = (
            'date_observed',
            'observation_station',
            'jellyfish_specie',
            'quantity',
            'created_by',
            'source',
            'sting_incidents',
            'total_incidents'
        )
        sequence = (
            'date_observed',
            'observation_route',
            'observation_station',
            'jellyfish_specie',
            'quantity',
            'created_by',
            'source',
        )


class JellyfishObservationAggregatedTable(tables.Table):
    x = tables.Column(empty_values=())
    y = tables.Column(empty_values=())
    sum_quantity = tables.Column()
    station_name = tables.Column()
    route_name = tables.Column()

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
                'station': record['station_name'],
                'route': record['route_name'],
                'count': record['sum_quantity']})
        return simplejson.dumps(data)

    def __init__(self, *args, **kwargs):
        self.route = kwargs.pop('route', None)
        super(JellyfishObservationAggregatedTable, self).__init__(*args, **kwargs)

    class Meta:
        attrs = {"class": "table table-striped table-condensed"}


class ObservationRouteTable(tables.Table):
    name = tables.TemplateColumn(
        """<a href="{% url 'data_route_observation_list' record.pk %}">
            {{ record.name }}
            </a>
        """)
    create_observation = tables.TemplateColumn(
        """{% load i18n %}
           <a class="btn btn-primary"
            href="{% url 'data_route_observation_create' record.pk %}">
            <i class="glyphicon glyphicon-plus"></i>
            {% trans 'Add' %} {% trans 'observation' %}
            </a>""",
        verbose_name=_('create observation'))
    create_bulk_observation = tables.TemplateColumn(
        """{% load i18n %}
           <a class="btn btn-warning"
            href="{% url 'data_route_observation_bulkcreate' record.pk %}">
            <i class="glyphicon glyphicon-plus"></i>
            {% trans 'Add bulk no-observations' %}
            </a>""",
        verbose_name=_('create bulk no-observations'))

    class Meta:
        model = models.ObservationRoute
        attrs = {"class": "table table-striped table-condensed"}
        fields = (
            'name',
        )


class ObservationBeachTable(tables.Table):
    name = tables.TemplateColumn(
        """{% load i18n %}{{ record.name }}
            {%if record.use_incident_form %}
            <a href="{% url 'data_route_dailyreport_list' record.pk %}" title="{% trans "Show observation list" %}">
            {% else %}
            <a href="{% url 'data_route_observation_list' record.pk %}" title="{% trans "Daily Report List" %}">
            {% endif %}
            <span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span>
            </a>
            <a href="{% url 'data_route_flagchange_list' record.pk %}" title="{% trans "Flag Change List" %}"><span class="glyphicon glyphicon-flag" aria-hidden="true"></span></a>
        """)
    island = tables.Column()
    municipality = tables.Column()
    create_observation = tables.TemplateColumn(
        """{% load i18n %}
           {%if record.use_incident_form %}
            <a class="btn btn-primary"
            href="{% url 'data_route_dailyreport_create' record.pk %}">
            <i class="glyphicon glyphicon-plus"></i>
            {% trans 'Add' %} {% trans 'daily report' %}
            </a>
           {% else %}<a class="btn btn-primary"
            href="{% url 'data_route_observation_create' record.pk %}">
            <i class="glyphicon glyphicon-plus"></i>
            {% trans 'Add' %} {% trans 'observation' %}
            </a>
            <a class="btn btn-warning"
            href="{% url 'data_route_observation_bulkcreate' record.pk %}">
            <i class="glyphicon glyphicon-plus"></i>
            {% trans 'Add bulk no-observations' %}
            </a>{% endif %}
            <a class="btn btn-info"
            href="{% url 'data_route_flagchange_create' record.pk %}">
            <i class="glyphicon glyphicon-plus"></i>
            {% trans 'Add' %} {% trans 'flag change' %}
            </a>

            """,
        verbose_name=_('actions'))

    class Meta:
        model = models.ObservationRoute
        attrs = {"class": "table table-striped table-condensed"}
        fields = (
            'name',
            'island',
            'municipality',
        )


class ObservationStationTable(tables.Table):
    name = tables.Column()
    observation_route = tables.Column()
    station_type = tables.Column()

    class Meta:
        model = models.ObservationStation
        attrs = {"class": "table table-striped table-condensed"}
        fields = (
            'name',
            'observation_route',
            'station_type'
        )


class ObservationStationGeoTable(tables.Table):
    x = tables.Column(empty_values=())
    y = tables.Column(empty_values=())
    name = tables.Column()
    observation_route = tables.Column()
    station_type = tables.Column()

    def render_x(self, record):
        return "{:.6f}".format(GEOSGeometry(record['position']).x)

    def render_y(self, record):
        return "{:.6f}".format(GEOSGeometry(record['position']).y)

    @property
    def json(self):
        data = []
        for record in self.rows:
            data.append({
                'lat': float(record['y']),
                'lng': float(record['x']),
                'station': record['name'],
                'route': record['observation_route']})
        return simplejson.dumps(data)

    def __init__(self, *args, **kwargs):
        self.route = kwargs.pop('route', None)
        super(ObservationStationGeoTable, self).__init__(*args, **kwargs)

    class Meta:
        model = models.ObservationStation
        attrs = {"class": "table table-striped table-condensed"}


class DailyReportTable(tables.Table):
    date_observed = tables.TemplateColumn(
        """<a href="{% url 'data_dailyreport_update' record.pk %}">
            {{ record.date_observed|date:'d/m/Y'}}
            </a>
        """)
    observation_station = tables.Column()
    sting_incidents = tables.Column()
    total_incidents = tables.Column()
    source = tables.Column()
    created_by = tables.Column()
    route = None

    def __init__(self, *args, **kwargs):
        self.route = kwargs.pop('route', None)
        super(DailyReportTable, self).__init__(*args, **kwargs)
        if self.route:
            self.context = Context({'route': self.route})
            self.base_columns['date_observed'].template_code = """
            <a href="{% url 'data_route_dailyreport_update' route.pk record.pk %}">
            {{ record.date_observed|date:'d/m/Y'}}
            </a>
            """

    class Meta:
        model = models.DailyReport
        attrs = {"class": "table table-striped table-condensed"}
        sequence = fields = (
            'date_observed',
            'observation_station',
            'sting_incidents',
            'total_incidents',
            'created_by',
            'source',
        )

    @property
    def verbose_name(self):
        if getattr(self, 'display_name', None):
            return self.display_name
        return self.Meta.model._meta.verbose_name_plural.title()


class DailyReportExportTable(DailyReportTable):
    date_observed = tables.Column()
    observation_route = tables.Column(
        accessor='observation_station.observation_route.name')

    def __init__(self, *args, **kwargs):
        self.route = kwargs.pop('route', None)
        super(DailyReportExportTable, self).__init__(*args, **kwargs)

    class Meta:
        model = models.DailyReport
        fields = (
            'date_observed',
            'observation_station',
            'created_by',
            'source',
            'sting_incidents',
            'total_incidents'
        )
        sequence = (
            'date_observed',
            'observation_route',
            'observation_station',
            'sting_incidents',
            'total_incidents',
            'created_by',
            'source',
        )


class FlagChangeTable(tables.Table):
    date = tables.TemplateColumn(
        """<a href="{% url 'data_flagchange_update' record.pk %}">
            {{ record.date|date:'d/m/Y H:i'}}
            </a>
        """)
    observation_station = tables.Column()
    flag_status = tables.Column()
    jellyfish_flag = tables.Column()
    created_by = tables.Column()
    route = None

    def __init__(self, *args, **kwargs):
        self.route = kwargs.pop('route', None)
        super(FlagChangeTable, self).__init__(*args, **kwargs)
        if self.route:
            self.context = Context({'route': self.route})
            self.base_columns['date'].template_code = """
            <a href="{% url 'data_route_flagchange_update' route.pk record.pk %}">
            {{ record.date|date:'d/m/Y H:i'}}
            </a>
            """

    class Meta:
        model = models.FlagChange
        attrs = {"class": "table table-striped table-condensed"}
        sequence = fields = (
            'date',
            'observation_station',
            'flag_status',
            'jellyfish_flag',
            'created_by',
        )

    @property
    def verbose_name(self):
        if getattr(self, 'display_name', None):
            return self.display_name
        return self.Meta.model._meta.verbose_name_plural.title()


class FlagChangeExportTable(FlagChangeTable):
    date = tables.Column()
    observation_route = tables.Column(
        accessor='observation_station.observation_route.name')

    def __init__(self, *args, **kwargs):
        self.route = kwargs.pop('route', None)
        super(FlagChangeExportTable, self).__init__(*args, **kwargs)
