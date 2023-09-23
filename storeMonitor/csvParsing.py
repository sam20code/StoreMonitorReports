import csv
from .models import PollData, BusinessHours, Timezone

# Define the paths to your CSV files
poll_data_csv_path = "storeStatus.csv"
business_hours_csv_path = "MenuHours.csv"
timezone_csv_path = "TimeZones.csv"

# Load data for YourModel
with open(poll_data_csv_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        PollData.objects.create(
            store_id=row['store_id'],
            timestamp_utc=row['timestamp_utc'],
            status=row['status']
        )

# Load data for BusinessHours
with open(business_hours_csv_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        BusinessHours.objects.create(
            store_id=row['store_id'],
            day_of_week=row['dayOfWeek'],
            start_time_local=row['start_time_local'],
            end_time_local=row['end_time_local']
        )

# Load data for Timezone
with open(timezone_csv_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        Timezone.objects.create(
            store_id=row['store_id'],
            timezone_str=row['timezone_str']
        )
