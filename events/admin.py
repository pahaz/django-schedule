from django.contrib import admin

from events.models import Calendar, Event, CalendarRelation, Rule


class CalendarAdminOptions(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']


class EventAdmin(admin.ModelAdmin):
    search_fields = ('title', )
    list_display = ('title', 'start', 'end', 'all_day', 'rule')
    list_filter = ('start', 'end', 'all_day', 'rule')
admin.site.register(Event, EventAdmin)


admin.site.register(Calendar, CalendarAdminOptions)
admin.site.register([Rule, CalendarRelation])
