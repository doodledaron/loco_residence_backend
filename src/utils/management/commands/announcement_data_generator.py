from datetime import timedelta
import random
from announcements.models import Announcement
from django.utils import timezone

class AnnouncementDataGenerator:
    def __init__(self, stdout, style):
        self.stdout = stdout
        self.style = style
        self.announcement_titles = [
            "Community Event Announcement",
            "Important Facility Update",
            "Resident Survey Reminder",
            "Parking Lot Closure Notice",
            "Recycling Program Changes",
            "Holiday Decorating Contest",
            "Pest Control Treatment Schedule",
            "Fitness Center Renovation",
            "Neighborhood Watch Meeting",
            "Snow Removal Procedures"
        ]
        self.announcement_contents = [
            "Join us for a fun community event this Saturday at the clubhouse!",
            "The fitness center will be closed for renovations next week. We apologize for the inconvenience.",
            "Please take a few minutes to complete our resident survey. Your feedback is important.",
            "The parking lot will be closed for resurfacing from June 1st to June 5th. Plan for alternative parking during this time.",
            "We are making some changes to our recycling program. Check the community bulletin board for more details.",
            "It's time for our annual holiday decorating contest! Prizes will be awarded for the best-decorated homes.",
            "Pest control treatments will be performed in all units on the first Tuesday of every month. Please make sure to clear any items from under sinks.",
            "The fitness center is currently undergoing a complete renovation. We anticipate the work to be completed by the end of the month.",
            "There will be a neighborhood watch meeting next Saturday at 7 PM in the community center. All residents are encouraged to attend.",
            "Please review the updated snow removal procedures for the community. Residents are responsible for clearing snow from their assigned parking spots."
        ]

    def generate_announcements(self, residents):
        for resident in residents:
            for title, content in zip(self.announcement_titles, self.announcement_contents):
                announcement = Announcement.objects.create(
                    title=title,
                    content=content,
                    created_at=timezone.now() - timedelta(days=random.randint(1, 30)),
                    updated_at=timezone.now()
                )
                self.stdout.write(self.style.SUCCESS(f'Created announcement: {announcement.title} for resident: {resident}'))