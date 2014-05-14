from django.core.management.base import NoArgsCommand, make_option
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.geos import Point
import re
import csv

from grumers.apps.data.models import ObservationRoute, ObservationStation


class Command(NoArgsCommand):

    help = "Import routes and stations in data/station_list.csv"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def process_beach_station(self, beach_el):
        print "Processing beach element", beach_el['NOM_PLATJA'],\
            " - ", beach_el['ELEMENT']
        route_code = "P-" + beach_el['CD_PLATJA']
        # search route
        try:
            route = ObservationRoute.objects.get(
                code__iexact=route_code)
        except ObjectDoesNotExist:
            route = ObservationRoute()
            route.route_type = 'B'
            route.code = route_code
            route.name = beach_el['NOM_PLATJA']
            route.island = beach_el['NOM_ILLA']
            route.municipality = beach_el['NOM_MUNI']
            route.save()

        # Check if station exists:
        if ObservationStation.objects.filter(name=beach_el['ELEMENT']).exists():
            return
        station = ObservationStation()
        station.observation_route = route
        # extract order from element (T-15001-01, digits after second -)
        s = re.split('-(\d+)', beach_el['ELEMENT'])
        if len(s) < 4:
            print "Beach element name is not as expected. Leave order 0"
            station.order = 0
        else:
            station.order = int(s[3])

        station.name = beach_el['ELEMENT']
        station.station_type = beach_el['TIPUS_PUNT']
        if station.station_type == 'N':
            station.order = station.order + 10
        elif station.station_type == 'O':
            station.order = station.order + 20
        x = float(beach_el['X'].replace(',', '.'))
        y = float(beach_el['Y'].replace(',', '.'))
        pnt = Point(x, y)
        pnt.set_srid(int(beach_el['SRID']))

        if pnt.srid != 4326:
            pnt.transform(4326)
        station.position = pnt
        station.save()

    def handle_noargs(self, **options):

        with open('data/beach_station_list.csv', 'rb') as infile:
            data = csv.DictReader(infile, delimiter=',')
            for line in data:
                self.process_beach_station(line)
