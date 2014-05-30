# -*- coding:utf-8 -*-
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.utils.html import strip_tags
from django.conf import settings
from django.db.models.signals import post_save
from sorl.thumbnail import get_thumbnail
import os


def generate_image_path(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(instance.picture_name, ext)
        return os.path.join(path, filename)
    return wrapper


class JellyfishSpecie(models.Model):
    name = models.CharField(_('scientific name'), max_length=100)
    common_name = models.CharField(_('common name'), max_length=100,
                                   null=True, blank=True)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    description = models.TextField(_('description'), null=True, blank=True)
    picture = models.ImageField(_('picture'),
                                upload_to=generate_image_path('jellyfish_species/'),
                                default='jellyfish_species/no-img.jpg')
    order = models.IntegerField(_('display order'))
    # Audit
    created_on = models.DateTimeField(_('date added'), auto_now_add=True)
    created_by = models.ForeignKey(User, blank=True, null=True,
                                   editable=False, related_name='created-specie',
                                   verbose_name=_('created by'))
    updated_on = models.DateTimeField(_('date modified'), auto_now=True)
    updated_by = models.ForeignKey(User, blank=True, null=True,
                                   editable=False, related_name='updated-specie',
                                   verbose_name=_('update by'))

    class Meta:
        verbose_name = _('jellyfish specie')
        verbose_name_plural = _('jellyfish species')
        ordering = ['order', 'name']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.updated_by = user
        if not self.id:
            self.created_by = user
        return super(JellyfishSpecie, self).save(*args, **kwargs)

    @property
    def picture_name(self):
        return self.slug

    @property
    def basic_dict(self):
        """
        Export this model to a dict compatible with JSON representation
        """

        im = get_thumbnail(self.picture, '50x50', crop='center', quality=99)

        obj = {
            "id": self.pk,
            "name": self.name,
            "common_name": self.common_name,
            "description": strip_tags(self.description),
            "picture": self.picture.url,
            "thumbnail": im.url,
        }

        return obj

ISLAND_CHOICES = (
    ('Mallorca', _('Mallorca')),
    ('Menorca', _('Menorca')),
    ('Eivissa', _('Eivissa')),
    ('Formentera', _('Formentera')),
)


class ObservationRoute(models.Model):
    ROUTE_TYPE_CHOICES = (
        ('R', _('Marine reserve')),
        ('C', _('Cleaning route')),
        ('B', _('Beach watching')),
    )

    name = models.CharField(_('name'), max_length=100)
    code = models.CharField(_('code'), max_length=10, null=True, blank=True,
                            db_index=True)
    description = models.TextField(_('description'), null=True, blank=True)
    route_type = models.CharField(_('type'), max_length=1,
                                  choices=ROUTE_TYPE_CHOICES,
                                  default='C')
    island = models.CharField(_('island'), max_length=15,
                              choices=ISLAND_CHOICES,
                              blank=True, null=True)
    municipality = models.CharField(_('municipality'), max_length=50,
                                    null=True, blank=True)
    groups = models.ManyToManyField(Group, verbose_name=_('user groups allowed'),
                                    blank=True, null=True)
    # Audit
    created_on = models.DateTimeField(_('date added'), auto_now_add=True)
    created_by = models.ForeignKey(User, blank=True, null=True,
                                   editable=False, related_name='created-route',
                                   verbose_name=_('created by'))
    updated_on = models.DateTimeField(_('date modified'), auto_now=True)
    updated_by = models.ForeignKey(User, blank=True, null=True,
                                   editable=False, related_name='updated-route',
                                   verbose_name=_('update by'))

    class Meta:
        verbose_name = _('observation route')
        verbose_name_plural = _('observation routes')
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @property
    def group_list(self):
        return ', '.join([group.name for group in self.groups.all()])

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.updated_by = user
        if not self.id:
            self.created_by = user
        return super(ObservationRoute, self).save(*args, **kwargs)


class ObservationStation(models.Model):
    STATION_TYPE_CHOICES = (
        ('S', _('High sea')),
        ('O', _('Offshore - 200 m')),
        ('N', _('Nearshore - 100 m')),
        ('B', _('Beach shore')),
    )

    name = models.CharField(_('name'), max_length=100)
    observation_route = models.ForeignKey(ObservationRoute, on_delete=models.PROTECT,
                                          verbose_name=_('observation route'))
    order = models.IntegerField(_('order in route'))
    position = models.PointField(srid=4326, verbose_name=_('position'))
    station_type = models.CharField(_('type'), max_length=1,
                                    choices=STATION_TYPE_CHOICES,
                                    default='S')
    # Audit
    created_on = models.DateTimeField(_('date added'), auto_now_add=True)
    created_by = models.ForeignKey(User, blank=True, null=True,
                                   editable=False, related_name='created-station',
                                   verbose_name=_('created by'))
    updated_on = models.DateTimeField(_('date modified'), auto_now=True)
    updated_by = models.ForeignKey(User, blank=True, null=True,
                                   editable=False, related_name='updated-station',
                                   verbose_name=_('update by'))

    objects = models.GeoManager()

    class Meta:
        verbose_name = _('observation station')
        verbose_name_plural = _('observation stations')
        ordering = ['observation_route', 'order']

    def __unicode__(self):
        return self.name

    @property
    def position_coordinates(self):
        return ", ".join([str(self.position.x), str(self.position.y)])

    @property
    def longname(self):
        return " - ".join([self.observation_route.name, self.name])

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.updated_by = user
        if not self.id:
            self.created_by = user
        return super(ObservationStation, self).save(*args, **kwargs)


class JellyfishObservation(models.Model):
    WEBFORM, API, BULK, WEBBULK = ('W', 'A', 'B', 'WB')
    SOURCE_CHOICES = (
        (WEBFORM, _('Web Form')),
        (WEBBULK, _('Web Form (Bulk)')),
        (API, _('API')),
        (BULK, _('Bulk upload')),
    )

    QUANTITY_CHOICES = (
        (0, _('None')),
        (1, _('One')),
        (3, _('2 to 5')),
        (8, _('6 to 10')),
        (50, _('11 to 99')),
        (110, _('100 or more')),
    )

    date_observed = models.DateTimeField(_('observation date and time'))
    observation_station = models.ForeignKey(ObservationStation, on_delete=models.PROTECT,
                                            verbose_name=_('observation station'))
    jellyfish_specie = models.ForeignKey(JellyfishSpecie, on_delete=models.PROTECT,
                                         blank=True, null=True,
                                         verbose_name=_('jellyfish specie'))
    quantity = models.IntegerField(_('quantity observed'), blank=True)
    picture = models.ImageField(_('picture'),
                                upload_to=generate_image_path('jellyfish_observations/'),
                                null=True, blank=True)
    source = models.CharField(_('source'), max_length=2,
                              choices=SOURCE_CHOICES,
                              default=WEBFORM, blank=False)
    remarks = models.TextField(_('remarks'), blank=True, null=True)
    sting_incidents = models.IntegerField(
        _('total sting incidents'),
        default=0, blank=True)
    total_incidents = models.IntegerField(
        _('total incidents'),
        default=0, blank=True)
    # Audit
    created_on = models.DateTimeField(_('date added'), auto_now_add=True)
    created_by = models.ForeignKey(User, blank=True, null=True,
                                   editable=False, related_name='created-observation',
                                   verbose_name=_('created by'))
    updated_on = models.DateTimeField(_('date modified'), auto_now=True)
    updated_by = models.ForeignKey(User, blank=True, null=True,
                                   editable=False, related_name='updated-observation',
                                   verbose_name=_('update by'))

    class Meta:
        verbose_name = _('jellyfish observation')
        verbose_name_plural = _('jellyfish observations')
        permissions = (
            ("can_list_jellyfishobservations",
             "Can list jellyfish observations"),
            ("can_list_others_jellyfishobservations",
             "Can list jellyfish observations from others"),
        )
        ordering = ['-date_observed']

    def __unicode__(self):
        specie = _('None')
        if self.jellyfish_specie:
            specie = self.jellyfish_specie.name
        return "{specie} on {date:%d/%m/%Y}: {qty}".format(
            specie=specie,
            date=self.date_observed,
            qty=self.quantity)

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.updated_by = user
        if not self.id:
            self.created_by = user
        return super(JellyfishObservation, self).save(*args, **kwargs)

    @property
    def picture_name(self):
        specie = 'None'
        if self.jellyfish_specie:
            specie = self.jellyfish_specie.slug
        return "{date:%Y%m%d-%H%M}-{specie}-{qty}".format(
            specie=specie,
            date=self.date_observed,
            qty=self.quantity)


def assign_default_beach_groups(sender, instance, **kwargs):
    if instance.route_type != 'B' or instance.groups.count() > 0:
        return
    groups = get_default_beach_groups(instance)
    instance.groups.add(*groups)


def get_default_beach_groups(route):
    groups = []
    groups.append(get_group(settings.GRUMERS_GROUP_BEACH_GENERAL_ADMIN))
    if route.municipality:
        group_name = settings.GRUMERS_GROUP_BEACH_MUN_ADMIN_PREFIX.decode('utf-8') +\
            route.municipality.decode('utf-8')
        groups.append(get_group(group_name))
    try:
        group_name = settings.GRUMERS_GROUP_BEACH_ADMIN_PREFIX.decode('utf-8') +\
            route.name
    except:
        group_name = settings.GRUMERS_GROUP_BEACH_ADMIN_PREFIX.decode('utf-8') +\
            route.name.decode('utf-8')

    groups.append(get_group(group_name))
    return groups


def get_group(group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        group = Group()
        group.name = group_name
        group.save()
    return group

post_save.connect(
    assign_default_beach_groups,
    sender=ObservationRoute,
    dispatch_uid="assign_beach_groups")
