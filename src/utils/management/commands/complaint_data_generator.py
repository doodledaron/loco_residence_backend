from datetime import datetime
from complaints.models import Complaint
import random

class ComplaintDataGenerator:
    def __init__(self, stdout, style):
        self.stdout = stdout
        self.style = style
        self.complaint_titles = [
            "Noisy Neighbors",
            "Broken Appliance",
            "Pest Infestation",
            "Parking Violation",
            "Maintenance Issue",
            "Unauthorized Modification",
            "Unsafe Playground Equipment",
            "Garbage Collection Dispute",
            "Unresponsive Property Manager",
            "Unfair Rental Increase"
        ]
        self.complaint_descriptions = [
            "The upstairs neighbors have been playing loud music late into the night, making it difficult to sleep.",
            "My refrigerator has been making strange noises and is not cooling properly. It needs to be repaired or replaced.",
            "I've noticed an increase in the number of ants and cockroaches in my apartment. This needs to be addressed as soon as possible.",
            "Someone has been parking in my assigned parking spot without authorization. This is an ongoing issue that needs to be resolved.",
            "The kitchen faucet is leaking, and there is a problem with the toilet in the bathroom that needs to be fixed.",
            "I noticed that my neighbor has made an unauthorized addition to their patio without permission from the HOA.",
            "One of the swings in the community playground is broken and poses a safety hazard, especially for young children.",
            "The garbage collection schedule has been inconsistent, and my trash has not been picked up for the last two weeks.",
            "I've been trying to reach the property manager for the past week regarding a maintenance issue, but they have not responded to my calls or emails.",
            "I recently received a notification about a rental increase that I believe is unreasonable and not in line with the current market rates."
        ]

    def generate_complaints(self, residents):
        statuses = ['Received', 'In Progress', 'Resolved', 'Rejected']

        for resident in residents:
            for _ in range(random.randint(1, 5)):  # Each resident has 1 to 5 complaints
                title = random.choice(self.complaint_titles)
                description = random.choice(self.complaint_descriptions)
                complaint = Complaint.objects.create(
                    resident=resident,
                    title=title,
                    description=description,
                    status=random.choice(statuses),
                    date=datetime.now().date()
                )
                self.stdout.write(self.style.SUCCESS(f'Created complaint: {complaint.title} for resident: {resident}'))