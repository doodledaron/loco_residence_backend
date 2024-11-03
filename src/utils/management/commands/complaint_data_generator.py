from datetime import datetime
from complaints.models import Complaint
import random

class ComplaintDataGenerator:
    def __init__(self, stdout, style):
        self.stdout = stdout
        self.style = style
        self.complaint_data = [
            {
                "title": "Noisy Neighbors",
                "description": "The upstairs neighbors have been playing loud music late into the night, making it difficult to sleep.",
                "category": "Services"
            },
            {
                "title": "Broken Appliance",
                "description": "My refrigerator has been making strange noises and is not cooling properly. It needs to be repaired or replaced.",
                "category": "Facility"
            },
            {
                "title": "Pest Infestation",
                "description": "I've noticed an increase in the number of ants and cockroaches in my apartment. This needs to be addressed as soon as possible.",
                "category": "Facility"
            },
            {
                "title": "Parking Violation",
                "description": "Someone has been parking in my assigned parking spot without authorization. This is an ongoing issue that needs to be resolved.",
                "category": "Facility"
            },
            {
                "title": "Maintenance Issue",
                "description": "The kitchen faucet is leaking, and there is a problem with the toilet in the bathroom that needs to be fixed.",
                "category": "Facility"
            },
            {
                "title": "Unauthorized Modification",
                "description": "I noticed that my neighbor has made an unauthorized addition to their patio without permission from the HOA.",
                "category": "Other"
            },
            {
                "title": "Unsafe Playground Equipment",
                "description": "One of the swings in the community playground is broken and poses a safety hazard, especially for young children.",
                "category": "Facility"
            },
            {
                "title": "Garbage Collection Dispute",
                "description": "The garbage collection schedule has been inconsistent, and my trash has not been picked up for the last two weeks.",
                "category": "Services"
            },
            {
                "title": "Unresponsive Property Manager",
                "description": "I've been trying to reach the property manager for the past week regarding a maintenance issue, but they have not responded to my calls or emails.",
                "category": "Services"
            },
            {
                "title": "Unfair Rental Increase",
                "description": "I recently received a notification about a rental increase that I believe is unreasonable and not in line with the current market rates.",
                "category": "Payment"
            }
        ]

        # Adding more complaints for variety, especially for Payment and Bookings categories
        self.complaint_data.extend([
            {
                "title": "Late Payment Processing",
                "description": "My rental payment was submitted on time but wasn't processed until several days later, resulting in a late fee.",
                "category": "Payment"
            },
            {
                "title": "Incorrect Booking Time",
                "description": "My facility booking for the tennis court was recorded for the wrong time slot.",
                "category": "Bookings"
            },
            {
                "title": "Double Charged Facility Fee",
                "description": "I was charged twice for my last month's facility usage fee.",
                "category": "Payment"
            },
            {
                "title": "Facility Booking System Down",
                "description": "Unable to book common facilities due to persistent system errors.",
                "category": "Bookings"
            },
            {
                "title": "Cleaning Service Quality",
                "description": "The cleaning service provided for common areas has been subpar for the past month.",
                "category": "Services"
            }
        ])

    def generate_complaints(self, residents):
        statuses = ['Received', 'In Progress', 'Resolved', 'Rejected']
        
        # Keep track of used complaints for each resident
        resident_complaints = {}
        
        for resident in residents:
            # Initialize empty set for this resident if not exists
            if resident.id not in resident_complaints:
                resident_complaints[resident.id] = set()
            
            # Determine how many complaints to generate
            num_complaints = min(
                random.randint(1, 5),  # Desired number of complaints
                len(self.complaint_data) - len(resident_complaints[resident.id])  # Available unique complaints
            )
            
            # Get available complaints (those not used by this resident)
            available_complaints = [
                complaint for i, complaint in enumerate(self.complaint_data)
                if i not in resident_complaints[resident.id]
            ]
            
            # Generate unique complaints
            for _ in range(num_complaints):
                # Randomly select a complaint from available ones
                complaint_data = random.choice(available_complaints)
                
                # Create the complaint
                complaint = Complaint.objects.create(
                    resident=resident,
                    title=complaint_data["title"],
                    description=complaint_data["description"],
                    category=complaint_data["category"],  # Added category
                    status=random.choice(statuses),
                    date=datetime.now().date()
                )
                
                # Mark this complaint as used for this resident
                resident_complaints[resident.id].add(
                    self.complaint_data.index(complaint_data)
                )
                
                # Remove this complaint from available ones
                available_complaints.remove(complaint_data)
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created complaint: {complaint.title} ({complaint.category}) for resident: {resident}'
                    )
                )