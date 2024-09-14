from django.core.management.base import BaseCommand

from utils.management.commands.finance_data__generator import FinanceDataGenerator
from .user_data_generator import UserDataGenerator
from .facility_data_generator import FacilityDataGenerator
from .booking_data_generator import BookingDataGenerator

class Command(BaseCommand):
    help = 'Generates all dummy data for testing'

    def add_arguments(self, parser):
        parser.add_argument('user_count', type=int, help='Number of users to create')
        parser.add_argument('--clear', action='store_true', help='Clear existing data before generating new data')

    def handle(self, *args, **options):
        user_count = options['user_count']
        
        if options['clear']:
            self.clear_all_data()

        self.stdout.write('Generating dummy data...')

        # Generate users
        user_generator = UserDataGenerator(self.stdout, self.style)
        users = user_generator.generate_users(user_count)

        # Generate facilities and time slots
        facility_generator = FacilityDataGenerator(self.stdout, self.style)
        facilities = facility_generator.generate_facilities()
        time_slots = facility_generator.generate_time_slots()

        # Generate bookings
        booking_generator = BookingDataGenerator(self.stdout, self.style)
        booking_generator.generate_bookings(users, facilities, time_slots)

        #Generate finances
        finance_generator = FinanceDataGenerator(self.stdout, self.style)
        finance_generator.generate_finance_data(users)

        self.stdout.write(self.style.SUCCESS('All dummy data generated successfully'))

    def clear_all_data(self):
        # Implementation of data clearing logic
        pass