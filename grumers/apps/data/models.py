from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.html import strip_tags
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
    common_name = models.CharField(_('common name'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    description = models.TextField(_('description'))
    picture = models.ImageField(_('picture'),
                                upload_to=generate_image_path('jellyfish_species/'),
                                default='jellyfish_species/no-img.jpg')
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


class ObservationRoute(models.Model):
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'))
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

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.updated_by = user
        if not self.id:
            self.created_by = user
        return super(ObservationRoute, self).save(*args, **kwargs)


class ObservationStation(models.Model):
    name = models.CharField(_('name'), max_length=100)
    observation_route = models.ForeignKey(ObservationRoute, on_delete=models.PROTECT,
                                          verbose_name=_('observation route'))
    order = models.IntegerField(_('order in route'))
    position = models.PointField(srid=4326, verbose_name=_('position'))
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

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.updated_by = user
        if not self.id:
            self.created_by = user
        return super(ObservationStation, self).save(*args, **kwargs)


class JellyfishObservation(models.Model):
    WEBFORM, API, BULK = ('W', 'A', 'B')
    SOURCE_CHOICES = (
        (WEBFORM, _('Web Form')),
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

    date_observed = models.DateTimeField(_('date observed'))
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
