from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User
from events.models import Calendar
from events.models import Event
from events.models import Rule
import sys
import datetime


class Command(NoArgsCommand):
    help = "Load some sample data into the db"

    def handle_noargs(self, **options):

        print "Checking for users ..."
        users = User.objects.all()
        if not users:
            print "It doesn't look like you've added any users. To add at least one super user run, django-admin.py createsuperuser"
            sys.exit(1)

        print "Checking for existing data ..."
        try:
            cal = Calendar.objects.get(name="Example Calendar")
            print "It looks like you already have loaded this sample data, quitting."
            sys.exit(1)
        except Calendar.DoesNotExist:
            pass

        print "Creating Example Calendar ..."
        cal = Calendar(name="Example Calendar", slug="example")
        cal.save()

        try:
            rule = Rule.objects.get(name="Daily")
        except Rule.DoesNotExist:
            print "Adding the basic recurring rules ..."
            rule = Rule(frequency="YEARLY", name="Yearly", description="will recur once every Year")
            rule.save()
            print "Yearly recurrence created."
            rule = Rule(frequency="MONTHLY", name="Monthly", description="will recur once every Month")
            rule.save()
            print "Monthly recurrence created."
            rule = Rule(frequency="WEEKLY", name="Weekly", description="will recur once every Week")
            rule.save()
            print "Weekly recurrence created."
            rule = Rule(frequency="DAILY", name="Daily", description="will recur once every Day")
            rule.save()
            print "Daily recurrence created."

        print "Adding some example events ..."
        WEEKLY_RULE = Rule.objects.get(frequency="WEEKLY")
        MONTHLY_RULE = Rule.objects.get(frequency="MONTHLY")
        YEARLY_RULE = Rule.objects.get(frequency="YEARLY")

        Event.objects.create(**{
            'creator': users[0],
            'title': 'Exercise',
            'start': datetime.datetime(2008, 11, 3, 9, 0),
            'end': datetime.datetime(2008, 11, 3, 10, 0),
            'rule': WEEKLY_RULE,
            'calendar': cal
        })

        Event.objects.create(**{
            'creator': users[0],
            'title': 'Exercise',
            'start': datetime.datetime(2008, 11, 5, 15, 0),
            'end': datetime.datetime(2008, 11, 5, 16, 30),
            'rule': WEEKLY_RULE,
            'calendar': cal
        })

        Event.objects.create(**{
            'creator': users[0],
            'title': 'Exercise',
            'start': datetime.datetime(2008, 11, 7, 9, 0),
            'end': datetime.datetime(2008, 11, 7, 10, 0),
            'rule': WEEKLY_RULE,
            'calendar': cal
        })

        Event.objects.create(**{
                'creator': users[0],
                'title': 'Pay Mortgage',
                'start': datetime.datetime(2008, 11, 1, 14, 0),
                'end': datetime.datetime(2008, 11, 1, 14, 30),
                'rule': MONTHLY_RULE,
                'calendar': cal
        })

        Event.objects.create(**{
            'creator': users[0],
            'title': "Rock's Birthday Party",
            'start': datetime.datetime(2008, 12, 11, 19, 0),
            'end': datetime.datetime(2008, 12, 11, 23, 59),
            'rule': YEARLY_RULE,
            'calendar': cal
        })

        Event.objects.create(**{
            'creator': users[0],
            'title': 'Christmas Party',
            'start': datetime.datetime(2008, 12, 25, 19, 30),
            'end': datetime.datetime(2008, 12, 25, 23, 59),
            'rule': YEARLY_RULE,
            'calendar': cal
        })
