from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Page(MPTTModel, FlatPage):
    title_menu = models.CharField(_('Short title for menu'), max_length=50)
    introduction = models.CharField(_('Introduction'), max_length=900,
                                    blank=True, null=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    related = models.ManyToManyField('self', verbose_name=_('related pages'),
                                     blank=True, null=True)
