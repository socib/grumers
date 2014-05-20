from django.contrib import admin
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db.models import TextField
from ckeditor.widgets import CKEditorWidget
from mptt.admin import MPTTModelAdmin
from modeltranslation.admin import TranslationAdmin
import models


class PageForm(FlatpageForm):

    class Meta:
        model = models.Page


class PageAdmin(MPTTModelAdmin, TranslationAdmin, FlatPageAdmin):
    form = PageForm
    formfield_overrides = {TextField: {'widget': CKEditorWidget(config_name='default')}, }
    filter_horizontal = ('related', 'groups',)
    list_display = ('url', 'title', 'order', 'group_list')
    fieldsets = (
        (None, {
            'fields': ('parent', 'url', 'title', 'title_menu', 'order', 'introduction',
                       'content', 'sites')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('related', 'enable_comments', 'is_container',
                       'registration_required', 'groups', 'template_name')
        }),
    )
admin.site.unregister(FlatPage)
admin.site.register(models.Page, PageAdmin)
