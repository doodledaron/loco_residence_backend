from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

from bookings.models import TimeSlot

def get_time_slot_ids(time_list):
    time_slot_ids = []
    try:
        for time_str  in time_list:
            time_obj = datetime.strptime(time_str, '%H:%M:%S').time()
            
            # Query the TimeSlot object with this time
            time_slot = TimeSlot.objects.get(start_time=time_obj)
            
            # Append the TimeSlot ID to the list
            time_slot_ids.append(time_slot.id)

        return time_slot_ids
    except ValueError:
        return {"error": "Invalid time format. Use HH:MM."}
    except ObjectDoesNotExist:
        return {"error": "TimeSlot objects do not exist for the given times."}
