import django_tables2 as tables
from django_tables2.utils import A
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
        # self.base_columns['date_observed'].verbose_name = 'Test - proves'
        if self.route:
            self.base_columns['date_observed'].viewname = 'data_route_observation_update'
            self.base_columns['date_observed'].args = [int(self.route), A('pk')]

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
            </a>""")

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
