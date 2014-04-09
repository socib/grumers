# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'JellyfishSpecie'
        db.create_table(u'data_jellyfishspecie', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('common_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='created-specie', null=True, to=orm['auth.User'])),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='updated-specie', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'data', ['JellyfishSpecie'])

        # Adding model 'ObservationRoute'
        db.create_table(u'data_observationroute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='created-route', null=True, to=orm['auth.User'])),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='updated-route', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'data', ['ObservationRoute'])

        # Adding model 'ObservationStation'
        db.create_table(u'data_observationstation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('observation_route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.ObservationRoute'], on_delete=models.PROTECT)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('position', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='created-station', null=True, to=orm['auth.User'])),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='updated-station', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'data', ['ObservationStation'])

        # Adding model 'JellyfishObservation'
        db.create_table(u'data_jellyfishobservation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_observed', self.gf('django.db.models.fields.DateTimeField')()),
            ('observation_station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.ObservationStation'], on_delete=models.PROTECT)),
            ('jellyfish_specie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.JellyfishSpecie'], null=True, on_delete=models.PROTECT, blank=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(default='W', max_length=2)),
            ('remarks', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='created-observation', null=True, to=orm['auth.User'])),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='updated-observation', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'data', ['JellyfishObservation'])


    def backwards(self, orm):
        # Deleting model 'JellyfishSpecie'
        db.delete_table(u'data_jellyfishspecie')

        # Deleting model 'ObservationRoute'
        db.delete_table(u'data_observationroute')

        # Deleting model 'ObservationStation'
        db.delete_table(u'data_observationstation')

        # Deleting model 'JellyfishObservation'
        db.delete_table(u'data_jellyfishobservation')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'data.jellyfishobservation': {
            'Meta': {'object_name': 'JellyfishObservation'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'created-observation'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_observed': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jellyfish_specie': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.JellyfishSpecie']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'observation_station': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.ObservationStation']", 'on_delete': 'models.PROTECT'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'default': "'W'", 'max_length': '2'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'updated-observation'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'data.jellyfishspecie': {
            'Meta': {'object_name': 'JellyfishSpecie'},
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'created-specie'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'updated-specie'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'data.observationroute': {
            'Meta': {'object_name': 'ObservationRoute'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'created-route'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'updated-route'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'data.observationstation': {
            'Meta': {'object_name': 'ObservationStation'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'created-station'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'observation_route': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.ObservationRoute']", 'on_delete': 'models.PROTECT'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'position': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'updated-station'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['data']