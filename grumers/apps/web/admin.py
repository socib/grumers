from django.contrib import admin
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db.models import TextField
from ckeditor.widgets import CKEditorWidget
from mptt.admin import MPTTModelAdmin
import models


class PageForm(FlatpageForm):

    class Meta:
        model = models.Page


class PageAdmin(MPTTModelAdmin, FlatPageAdmin):
    form = PageForm
    formfield_overrides = {TextField: {'widget': CKEditorWidget(config_name='default')}, }
    filter_horizontal = ('related',)
    fieldsets = (
        (None, {
            'fields': ('parent', 'url', 'title', 'title_menu', 'introduction', 'content', 'sites')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('related', 'enable_comments', 'registration_required', 'template_name')
        }),
    )
admin.site.unregister(FlatPage)
admin.site.register(models.Page, PageAdmin)
