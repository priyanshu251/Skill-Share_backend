from datetime import datetime, timedelta
import pytz

# Get the current time in UTC
now = datetime.now()

# Add one day to get tomorrow's date
tomorrow = now + timedelta(days=1)

# Print the timestamp
print(tomorrow)
