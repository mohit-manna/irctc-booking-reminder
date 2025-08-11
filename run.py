import icalendar
import requests
from datetime import datetime, timedelta
import uuid

# Replace with your actual HTTP URL
ics_url = "https://calendar.google.com/calendar/ical/en.indian%23holiday%40group.v.calendar.google.com/public/basic.ics"  # Update this URL
response = requests.get(ics_url)
response.raise_for_status()  # Raises an exception for bad status codes

calendar = icalendar.Calendar.from_ical(response.content)

# Create a new calendar for IRCTC booking reminders
irctc_calendar = icalendar.Calendar()
irctc_calendar.add('prodid', '-//IRCTC Booking Reminder//EN')
irctc_calendar.add('version', '2.0')
irctc_calendar.add('calscale', 'GREGORIAN')
irctc_calendar.add('method', 'PUBLISH')
# Add last modified timestamp
irctc_calendar.add('last-modified', datetime.now())
# Add custom property for last updated
irctc_calendar.add('x-wr-lastupdated', datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'))

# Process each event in the original calendar
for component in calendar.walk():
    if component.name == "VEVENT":
        original_event = component
        
        # Get the original event date
        original_date = original_event.get('DTSTART').dt
        if isinstance(original_date, datetime):
            # If it's a datetime, just use the date part
            original_date = original_date.date()
        
        # Calculate booking date (61 days in advance)
        booking_date = original_date - timedelta(days=61)
        
        # Get original summary
        original_summary = str(original_event.get('SUMMARY', 'Event'))
        
        # Format the original date as dd/mm/yyyy
        formatted_date = original_date.strftime('%d/%m/%Y')
        
        # Create single event with new naming format
        new_event = icalendar.Event()
        new_event.add('uid', str(uuid.uuid4()))
        
        # Set event to start at 7:30 AM on the booking date
        booking_datetime = datetime.combine(booking_date, datetime.min.time().replace(hour=7, minute=30))
        new_event.add('dtstart', booking_datetime)
        new_event.add('dtend', booking_datetime + timedelta(hours=1))  # 1 hour duration
        
        # Set the new summary format
        new_event.add('summary', f'Booking For {original_summary} {formatted_date}')
        new_event.add('description', f'Booking reminder for {original_summary} on {formatted_date}')
        new_event.add('dtstamp', datetime.now())
        
        # Add specific alarms as requested
        # Alarm 1: 10 minutes before
        alarm1 = icalendar.Alarm()
        alarm1.add('action', 'DISPLAY')
        alarm1.add('trigger', timedelta(minutes=-10))
        alarm1.add('description', 'This is an event reminder')
        new_event.add_component(alarm1)
        
        # Alarm 2: 1 day before
        alarm2 = icalendar.Alarm()
        alarm2.add('action', 'DISPLAY')
        alarm2.add('trigger', timedelta(days=-1))
        alarm2.add('description', 'This is an event reminder')
        new_event.add_component(alarm2)
        
        # Alarm 3: 2 days before
        alarm3 = icalendar.Alarm()
        alarm3.add('action', 'DISPLAY')
        alarm3.add('trigger', timedelta(days=-2))
        alarm3.add('description', 'This is an event reminder')
        new_event.add_component(alarm3)
        
        # Alarm 4: 3 days before
        alarm4 = icalendar.Alarm()
        alarm4.add('action', 'DISPLAY')
        alarm4.add('trigger', timedelta(days=-3))
        alarm4.add('description', 'This is an event reminder')
        new_event.add_component(alarm4)
        
        # Add the event to the IRCTC calendar
        irctc_calendar.add_component(new_event)

# Save the new calendar to file
with open('irctc-booking.ics', 'wb') as f:
    f.write(irctc_calendar.to_ical())

print(f"Created irctc-booking.ics with booking reminders")
print(f"Total events created: {len([c for c in irctc_calendar.walk() if c.name == 'VEVENT'])}")

# Optional: Print some sample events for verification
print("\nSample booking events:")
count = 10
li=[]
today = datetime.now()
# Filter and keep all events from today onwards in ascending order
events = []
for component in irctc_calendar.walk():
    if component.name == "VEVENT":
        event_start = component.get('DTSTART').dt
        if event_start.date() >= today.date():
            events.append((event_start, f"- {event_start}: {component.get('SUMMARY')}"))

# Sort events by start date/time
events.sort(key=lambda x: x[0])

# Print sorted events and count
for _, event_str in events:
    if count >= 1:
        print(event_str)
    count -= 1