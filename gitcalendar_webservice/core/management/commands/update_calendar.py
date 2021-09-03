from django.core.management.base import BaseCommand, CommandError

from core.calendar_generator import generator
from core.models import CalendarConfiguration


class Command(BaseCommand):
    help = 'Updates all calendars'

    #  def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        for config in CalendarConfiguration.objects.all():
            print(config.config_name)
            try:
                generator(config)
            except Exception:
                self.stdout.write(self.style.ERROR('Calendar Configuration "%s" failed' % config.config_name))

            self.stdout.write(self.style.SUCCESS('Successfully updated "%s"' % config.config_name))
