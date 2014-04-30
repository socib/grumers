from django.core.management.base import NoArgsCommand, make_option
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.geos import Point
from fastkml import kml
import re

from grumers.apps.data.models import ObservationRoute, ObservationStation


class Command(NoArgsCommand):

    help = "Whatever you want to print here"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def process_feature(self, feature):
        print "Processing feature ", feature.name
        if isinstance(feature, kml.Placemark):
            # Search marker code
            s = re.split('_(\d+)', feature.name)
            if len(s) < 2:
                # print "Placemark name is not correct. Discard"
                return

            route = s[0]
            order = s[1]
            print 'Route=', route, 'Order=', order

            station = ObservationStation()
            try:
                station.observation_route = ObservationRoute.objects.get(
                    code__iexact=route)
            except ObjectDoesNotExist:
                print "Route code", route, " does no exist. Discard"
                return
            station.order = int(order)
            station.name = feature.name
            station.position = Point(feature.geometry.x, feature.geometry.y)
            station.save()

        if getattr(feature, 'features', None):
            for f in feature.features():
                self.process_feature(f)

    def handle_noargs(self, **options):

        f = file('data/rutes_neteja_me.kml')
        k = kml.KML()
        kml_doc = f.read()
        k.from_string(kml_doc)

        for feature in k.features():
            self.process_feature(feature)
