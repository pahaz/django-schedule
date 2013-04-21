# -*- coding: utf-8 -*-
import datetime
from south.db import db
from django.db import connection
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):

        # If the database has tables from when the app was named "schedule"
        # then rename the tables instead of create new tables
        if 'schedule_calendar' in connection.introspection.table_names():
            db.rename_table('schedule_calendar', 'events_calendar')
            db.rename_table('schedule_calendarrelation', 'events_calendarrelation')
            db.rename_table('schedule_rule', 'events_rule')
            db.rename_table('schedule_event', 'events_event')
            db.rename_table('schedule_eventrelation', 'events_eventrelation')
            db.rename_table('schedule_occurrence', 'events_occurrence')

            if not db.dry_run:
                orm['contenttypes.contenttype'].objects.filter(app_label='schedule', model='calendar').update(app_label='events')
                orm['contenttypes.contenttype'].objects.filter(app_label='schedule', model='calendarrelation').update(app_label='events')
                orm['contenttypes.contenttype'].objects.filter(app_label='schedule', model='rule').update(app_label='events')
                orm['contenttypes.contenttype'].objects.filter(app_label='schedule', model='event').update(app_label='events')
                orm['contenttypes.contenttype'].objects.filter(app_label='schedule', model='eventrelation').update(app_label='events')
                orm['contenttypes.contenttype'].objects.filter(app_label='schedule', model='occurrence').update(app_label='events')

        else:

            # Adding model 'Calendar'
            db.create_table('events_calendar', (
                ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
                ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
                ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200)),
            ))
            db.send_create_signal('events', ['Calendar'])

            # Adding model 'CalendarRelation'
            db.create_table('events_calendarrelation', (
                ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
                ('calendar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Calendar'])),
                ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
                ('object_id', self.gf('django.db.models.fields.IntegerField')()),
                ('distinction', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
                ('inheritable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ))
            db.send_create_signal('events', ['CalendarRelation'])

            # Adding model 'Rule'
            db.create_table('events_rule', (
                ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
                ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
                ('description', self.gf('django.db.models.fields.TextField')()),
                ('frequency', self.gf('django.db.models.fields.CharField')(max_length=10)),
                ('params', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ))
            db.send_create_signal('events', ['Rule'])

            # Adding model 'Event'
            db.create_table('events_event', (
                ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
                ('start', self.gf('django.db.models.fields.DateTimeField')()),
                ('end', self.gf('django.db.models.fields.DateTimeField')()),
                ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
                ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
                ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
                ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
                ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Rule'], null=True, blank=True)),
                ('end_recurring_period', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
                ('calendar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Calendar'], blank=True)),
            ))
            db.send_create_signal('events', ['Event'])

            # Adding model 'EventRelation'
            db.create_table('events_eventrelation', (
                ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
                ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
                ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
                ('object_id', self.gf('django.db.models.fields.IntegerField')()),
                ('distinction', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ))
            db.send_create_signal('events', ['EventRelation'])

            # Adding model 'Occurrence'
            db.create_table('events_occurrence', (
                ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
                ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
                ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
                ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
                ('start', self.gf('django.db.models.fields.DateTimeField')()),
                ('end', self.gf('django.db.models.fields.DateTimeField')()),
                ('cancelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
                ('original_start', self.gf('django.db.models.fields.DateTimeField')()),
                ('original_end', self.gf('django.db.models.fields.DateTimeField')()),
            ))
            db.send_create_signal('events', ['Occurrence'])

    def backwards(self, orm):
        # Deleting model 'Calendar'
        db.delete_table('events_calendar')

        # Deleting model 'CalendarRelation'
        db.delete_table('events_calendarrelation')

        # Deleting model 'Rule'
        db.delete_table('events_rule')

        # Deleting model 'Event'
        db.delete_table('events_event')

        # Deleting model 'EventRelation'
        db.delete_table('events_eventrelation')

        # Deleting model 'Occurrence'
        db.delete_table('events_occurrence')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'events.calendar': {
            'Meta': {'object_name': 'Calendar'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'})
        },
        'events.calendarrelation': {
            'Meta': {'object_name': 'CalendarRelation'},
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Calendar']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'distinction': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inheritable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Calendar']", 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'end_recurring_period': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Rule']", 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'events.eventrelation': {
            'Meta': {'object_name': 'EventRelation'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'distinction': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'events.occurrence': {
            'Meta': {'object_name': 'Occurrence'},
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_end': ('django.db.models.fields.DateTimeField', [], {}),
            'original_start': ('django.db.models.fields.DateTimeField', [], {}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'events.rule': {
            'Meta': {'object_name': 'Rule'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'params': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['events']
