# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Page.title_en'
        db.add_column(u'web_page', 'title_en',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.title_ca'
        db.add_column(u'web_page', 'title_ca',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.title_es'
        db.add_column(u'web_page', 'title_es',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.content_en'
        db.add_column(u'web_page', 'content_en',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.content_ca'
        db.add_column(u'web_page', 'content_ca',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.content_es'
        db.add_column(u'web_page', 'content_es',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.title_menu_en'
        db.add_column(u'web_page', 'title_menu_en',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.title_menu_ca'
        db.add_column(u'web_page', 'title_menu_ca',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.title_menu_es'
        db.add_column(u'web_page', 'title_menu_es',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.introduction_en'
        db.add_column(u'web_page', 'introduction_en',
                      self.gf('django.db.models.fields.CharField')(max_length=900, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.introduction_ca'
        db.add_column(u'web_page', 'introduction_ca',
                      self.gf('django.db.models.fields.CharField')(max_length=900, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.introduction_es'
        db.add_column(u'web_page', 'introduction_es',
                      self.gf('django.db.models.fields.CharField')(max_length=900, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Page.title_en'
        db.delete_column(u'web_page', 'title_en')

        # Deleting field 'Page.title_ca'
        db.delete_column(u'web_page', 'title_ca')

        # Deleting field 'Page.title_es'
        db.delete_column(u'web_page', 'title_es')

        # Deleting field 'Page.content_en'
        db.delete_column(u'web_page', 'content_en')

        # Deleting field 'Page.content_ca'
        db.delete_column(u'web_page', 'content_ca')

        # Deleting field 'Page.content_es'
        db.delete_column(u'web_page', 'content_es')

        # Deleting field 'Page.title_menu_en'
        db.delete_column(u'web_page', 'title_menu_en')

        # Deleting field 'Page.title_menu_ca'
        db.delete_column(u'web_page', 'title_menu_ca')

        # Deleting field 'Page.title_menu_es'
        db.delete_column(u'web_page', 'title_menu_es')

        # Deleting field 'Page.introduction_en'
        db.delete_column(u'web_page', 'introduction_en')

        # Deleting field 'Page.introduction_ca'
        db.delete_column(u'web_page', 'introduction_ca')

        # Deleting field 'Page.introduction_es'
        db.delete_column(u'web_page', 'introduction_es')


    models = {
        u'flatpages.flatpage': {
            'Meta': {'ordering': "(u'url',)", 'object_name': 'FlatPage', 'db_table': "u'django_flatpage'"},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'web.page': {
            'Meta': {'object_name': 'Page', '_ormbases': [u'flatpages.FlatPage']},
            'content_ca': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'flatpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['flatpages.FlatPage']", 'unique': 'True', 'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.CharField', [], {'max_length': '900', 'null': 'True', 'blank': 'True'}),
            'introduction_ca': ('django.db.models.fields.CharField', [], {'max_length': '900', 'null': 'True', 'blank': 'True'}),
            'introduction_en': ('django.db.models.fields.CharField', [], {'max_length': '900', 'null': 'True', 'blank': 'True'}),
            'introduction_es': ('django.db.models.fields.CharField', [], {'max_length': '900', 'null': 'True', 'blank': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['web.Page']"}),
            'related': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_rel_+'", 'null': 'True', 'to': u"orm['web.Page']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'title_ca': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_menu': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title_menu_ca': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title_menu_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title_menu_es': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['web']