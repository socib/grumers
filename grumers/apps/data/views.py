# coding: utf-8
from grumers.apps.web.views import BasePageView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import BaseListView
from django_tables2.views import SingleTableView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson as json
from django.contrib import messages
from django.db.models import Sum, Max
from django.core.exceptions import PermissionDenied
from datetime import datetime
from grumers.utils import exporter
import models
import forms
import tables


class JellyfishObservationMixin(BasePageView):
    """
    Shared code for create or update a Jellyfish Observation
    """

    model = models.JellyfishObservation

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.station = request.GET.get('station', None)
        pk_route = kwargs.get('pk_route', None)
        if pk_route:
            self.route = models.ObservationRoute.objects.get(pk=pk_route)
            # Check if user is member of a group in route groups (if it has any)
            if not request.user.is_superuser and self.route.groups and\
               not (request.user.groups.all() & self.route.groups.all()):
                raise PermissionDenied()
        else:
            self.route = None

        self.date = request.GET.get('date', None)
        if self.date:
            self.date = datetime.strptime(self.date, '%Y%m%d%H%M')
        self.next_station = None
        self.station_list = models.ObservationStation.objects.all()
        if self.route:
            self.station_list = self.station_list.filter(observation_route=self.route)
        return super(JellyfishObservationMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(JellyfishObservationMixin, self).get_context_data(**kwargs)
        context['station_list'] = self.station_list
        context['route'] = self.route
        return context

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        return super(JellyfishObservationMixin, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(JellyfishObservationMixin, self).get_form_kwargs()
        kwargs['station'] = self.station
        if self.route:
            kwargs['route'] = self.route
        return kwargs

    def get_success_url(self):
        if self.next_station:
            if self.route:
                return "{url}?station={next_station}&date={date:%Y%m%d%H%M}".format(
                    url=reverse('data_route_observation_create',
                                args=[self.route.pk]),
                    next_station=self.next_station,
                    date=self.object.date_observed)
            return "{url}?station={next_station}&date={date:%Y%m%d%H%M}".format(
                url=reverse('data_observation_create'),
                next_station=self.next_station,
                date=self.object.date_observed)
        if self.route:
            return reverse('data_route_observation_list', args=[self.route.pk])
        return reverse('data_observation_list')


class JellyfishObservationCreate(JellyfishObservationMixin, CreateView):
    """
    Create a new Jellyfish Observation
    """

    template_name_suffix = '_create'
    form_class = forms.JellyfishObservationCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.source = models.JellyfishObservation.WEBFORM
        self.object.save(user=self.request.user)
        # Notify that in messages area
        messages.add_message(self.request, messages.SUCCESS, _('Observation created'))
        if 'next_station' in form.data:
            # calculate next station
            station = models.ObservationStation.objects.filter(
                observation_route=self.object.observation_station.observation_route,
                order__gte=self.object.observation_station.order)\
                .exclude(pk__in=[self.object.observation_station.pk])\
                .order_by('order')
            if station:
                self.next_station = station[0].pk

        return super(JellyfishObservationCreate, self).form_valid(form)

    def get_initial(self):
        initial = super(JellyfishObservationCreate, self).get_initial()
        initial = initial.copy()
        if self.date:
            initial['date_observed'] = self.date
        else:
            initial['date_observed'] = datetime.now()
        if len(self.station_list) == 1:
            initial['observation_station'] = self.station_list[0]
        return initial


class JellyfishObservationUpdate(JellyfishObservationMixin, UpdateView):
    """
    Update Jellyfish Observation
    """

    template_name_suffix = '_update'
    form_class = forms.JellyfishObservationUpdateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save(user=self.request.user)
        # Notify that in messages area
        messages.add_message(self.request, messages.SUCCESS, _('Observation updated'))
        return super(JellyfishObservationUpdate, self).form_valid(form)


class JellyfishObservationDelete(JellyfishObservationMixin, DeleteView):
    """
    Delete an observation
    """

    template_name_suffix = '_delete'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('data.delete_jellyfishobservation'):
            raise PermissionDenied()
        return super(JellyfishObservationDelete, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Override delete method to add message
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        messages.add_message(self.request, messages.SUCCESS, _('Observation deleted'))
        self.object.delete()
        return HttpResponseRedirect(success_url)


class JellyfishObservationList(BasePageView, SingleTableView):
    """List observations
    """

    table_class = tables.JellyfishObservationTable
    model = models.JellyfishObservation
    table_pagination = {"per_page": 50}
    export_format = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('data.can_list_jellyfishobservations'):
            raise PermissionDenied()
        pk_route = kwargs.get('pk_route', None)
        if pk_route:
            self.route = models.ObservationRoute.objects.get(pk=pk_route)
            # Check if user is member of a group in route groups (if it has any)
            if not request.user.is_superuser and self.route.groups and\
               not (request.user.groups.all() & self.route.groups.all()):
                raise PermissionDenied()
        else:
            self.route = None
        self.form = forms.JellyfishObservationFilterForm(self.request.GET,
                                                         user=request.user,
                                                         route=self.route)
        # Get export_type
        if "export" in request.POST or "export" in request.GET:
            self.export_format = 'xlsx'
            self.table_class = tables.JellyfishObservationExportTable

        return super(JellyfishObservationList, self).dispatch(request, *args, **kwargs)

    def get_table(self, **kwargs):
        if self.route:
            kwargs['route'] = self.route.pk
        return super(JellyfishObservationList, self).get_table(**kwargs)

    def get_table_data(self):
        data = models.JellyfishObservation.objects.all()
        user = self.request.user

        # Filter observations
        if not user.is_superuser and not user.is_staff:
            data = data.filter(created_by=user)
        if self.route:
            data = data.filter(
                observation_station__observation_route=self.route)

        if self.form.is_valid():
            if self.form.cleaned_data['jellyfish_specie']:
                data = data.filter(
                    jellyfish_specie=self.form.cleaned_data['jellyfish_specie'])
            if self.form.cleaned_data['route']:
                data = data.filter(
                    observation_station__observation_route=
                    self.form.cleaned_data['route'])
            if self.form.cleaned_data['station']:
                data = data.filter(
                    observation_station=self.form.cleaned_data['station'])
            if self.form.cleaned_data.get('created_by'):
                data = data.filter(
                    created_by=self.form.cleaned_data['created_by'])
            if self.form.cleaned_data.get('source'):
                data = data.filter(
                    source__in=self.form.cleaned_data['source'])
            if self.form.cleaned_data.get('from_date'):
                data = data.filter(
                    date_observed__gte=self.form.cleaned_data['from_date'])
        data = data.order_by('-date_observed')
        return data

    def get_context_data(self, **kwargs):
        context = super(JellyfishObservationList, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['route'] = self.route
        return context

    def export_data(self):
        table = self.get_table()
        return exporter.export_table(table, format=self.export_format)

    def render_to_response(self, context, **response_kwargs):
        if self.export_format is not None:
            return self.export_data()
        return super(
            JellyfishObservationList,
            self).render_to_response(context, **response_kwargs)


class JellyfishObservationMap(JellyfishObservationList):
    """Show observations in a map, with filter.
    """
    template_name = 'data/jellyfishobservation_map.html'
    table_class = tables.JellyfishObservationAggregatedTable

    def get_table_data(self):
        data = super(JellyfishObservationMap, self).get_table_data()
        if self.export_format is not None:
            return data
        data = data.values('observation_station__position').annotate(
            sum_quantity=Sum('quantity'),
            route_name=Max('observation_station__observation_route__name'),
            station_name=Max('observation_station__name')).order_by('-sum_quantity')
        return data


class JellyfishObservationHeatmap(JellyfishObservationMap):
    """Show observations in a heatmap, with filter.
    """
    template_name = 'data/jellyfishobservation_heatmap.html'


class ObservationRouteList(BasePageView, SingleTableView):
    """List routes
    """

    table_class = tables.ObservationRouteTable
    model = models.ObservationRoute
    table_pagination = {"per_page": 50}

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ObservationRouteList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        routes = models.ObservationRoute.objects.exclude(
            route_type='B')
        if not self.request.user.is_superuser:
            routes = routes.filter(
                groups__in=self.request.user.groups.all())
        return routes


class ObservationBeachList(ObservationRouteList):
    table_class = tables.ObservationBeachTable
    template_name = 'data/observationbeach_list.html'

    def get_queryset(self):
        routes = models.ObservationRoute.objects.filter(
            route_type='B')
        if not self.request.user.is_superuser:
            routes = routes.filter(
                groups__in=self.request.user.groups.all())
        return routes


class JSONJellyfishSpecieList(BaseListView):

    def get_queryset(self):
        return models.JellyfishSpecie.objects.all()

    def render_to_response(self, context):
        "Returns a JSON response"
        species = [specie.basic_dict for specie in self.get_queryset()]
        return self.get_json_response(json.dumps(species))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return HttpResponse(content,
                            content_type='application/json',
                            **httpresponse_kwargs)
