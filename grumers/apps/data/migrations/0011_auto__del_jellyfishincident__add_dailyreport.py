# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'JellyfishIncident'
        db.delete_table(u'data_jellyfishincident')

        # Adding model 'DailyReport'
        db.create_table(u'data_dailyreport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_observed', self.gf('django.db.models.fields.DateField')()),
            ('observation_station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.ObservationStation'], on_delete=models.PROTECT)),
            ('source', self.gf('django.db.models.fields.CharField')(default='W', max_length=2)),
            ('sting_incidents', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('total_incidents', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='created-incident', null=True, to=orm['auth.User'])),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='updated-incident', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'data', ['DailyReport'])


    def backwards(self, orm):
        # Adding model 'JellyfishIncident'
        db.create_table(u'data_jellyfishincident', (
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='updated-incident', null=True, to=orm['auth.User'], blank=True)),
            ('date_observed', self.gf('django.db.models.fields.DateField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('total_incidents', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sting_incidents', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('observation_station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.ObservationStation'], on_delete=models.PROTECT)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='created-incident', null=True, to=orm['auth.User'], blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(default='W', max_length=2)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'data', ['JellyfishIncident'])

        # Deleting model 'DailyReport'
        db.delete_table(u'data_dailyreport')


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
        u'data.dailyreport': {
            'Meta': {'ordering': "['-date_observed']", 'object_name': 'DailyReport'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'created-incident'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_observed': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observation_station': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.ObservationStation']", 'on_delete': 'models.PROTECT'}),
            'source': ('django.db.models.fields.CharField', [], {'default': "'W'", 'max_length': '2'}),
            'sting_incidents': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'total_incidents': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'updated-incident'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'data.flagchange': {
            'Meta': {'ordering': "['-date']", 'object_name': 'FlagChange'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'created-flag'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'flag_status': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jellyfish_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'observation_station': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.ObservationStation']", 'on_delete': 'models.PROTECT'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'updated-flag'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'data.jellyfishobservation': {
            'Meta': {'ordering': "['-date_observed']", 'object_name': 'JellyfishObservation'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'created-observation'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_observed': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jellyfish_specie': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.JellyfishSpecie']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'observation_station': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.ObservationStation']", 'on_delete': 'models.PROTECT'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'default': "'W'", 'max_length': '2'}),
            'sting_incidents': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'total_incidents': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'updated-observation'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'data.jellyfishspecie': {
            'Meta': {'ordering': "['order', 'name']", 'object_name': 'JellyfishSpecie'},
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'created-specie'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'default': "'jellyfish_species/no-img.jpg'", 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'updated-specie'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'data.observationroute': {
            'Meta': {'ordering': "['name']", 'object_name': 'ObservationRoute'},
            'code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'created-route'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'island': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'municipality': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'route_type': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '1'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'updated-route'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'use_incident_form': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'data.observationstation': {
            'Meta': {'ordering': "['observation_route', 'order']", 'object_name': 'ObservationStation'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'created-station'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'observation_route': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.ObservationRoute']", 'on_delete': 'models.PROTECT'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'position': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'station_type': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '1'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'updated-station'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['data']