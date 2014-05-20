from django.contrib.auth.models import Group
from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager


class Page(MPTTModel, FlatPage):
    title_menu = models.CharField(_('Short title for menu'), max_length=50)
    order = models.IntegerField(_('order'), default=0)
    introduction = models.CharField(_('Introduction'), max_length=900,
                                    blank=True, null=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    related = models.ManyToManyField('self', verbose_name=_('related pages'),
                                     blank=True, null=True)
    groups = models.ManyToManyField(Group, verbose_name=_('user groups allowed'),
                                    blank=True, null=True)
    is_container = models.BooleanField(_('page is just a container'), default=False)

    tree = TreeManager()

    class MPTTMeta:
        order_insertion_by = ['order']

    @property
    def group_list(self):
        return ', '.join([group.name for group in self.groups.all()])
