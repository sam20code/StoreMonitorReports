import pandas as pd
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
import datetime
import random
import string


def calculate_uptime_downtime(store_id, store_data, business_hours, timezone, report_id):
    # Sort store_data by timestamp_utc
    store_data.sort_values(by='timestamp_utc', inplace=True)

    uptime_last_hour = 0
    uptime_last_day = 0
    uptime_last_week = 0
    downtime_last_hour = 0
    downtime_last_day = 0
    downtime_last_week = 0

    for index, row in store_data.iterrows():
        row['timestamp_utc'] = row['timestamp_utc'].tz_convert(timezone)

        # Use weekday() to get the day of the week (0 for Monday, 1 for Tuesday, etc.)
        day_of_week = row['timestamp_utc'].weekday()

        if day_of_week in business_hours:
            if business_hours[day_of_week]['open'] <= row['timestamp_utc'].time() <= business_hours[day_of_week]['close']:
                if index > 0:
                    time_diff = (row['timestamp_utc'] - store_data.loc[index - 1, 'timestamp_utc']).total_seconds() / 60
                    if row['status'] == 'active':
                        uptime_last_hour += time_diff
                        uptime_last_day += time_diff
                        uptime_last_week += time_diff
                    else:
                        downtime_last_hour += time_diff
                        downtime_last_day += time_diff
                        downtime_last_week += time_diff

    uptime_last_hour = round(uptime_last_hour / 60, 2)
    uptime_last_day = round(uptime_last_day / 60, 2)
    uptime_last_week = round(uptime_last_week / 60, 2)
    downtime_last_hour = round(downtime_last_hour / 60, 2)
    downtime_last_day = round(downtime_last_day / 60, 2)
    downtime_last_week = round(downtime_last_week / 60, 2)

    return store_id, uptime_last_hour, uptime_last_day, uptime_last_week, downtime_last_hour, downtime_last_day, downtime_last_week, report_id

def get_report(request,report_id):

    store_status_data = pd.read_csv('storeStatus.csv')
    business_hours_data = pd.read_csv('MenuHours.csv')
    timezone_data = pd.read_csv('Timezones.csv')

    store_data = pd.merge(store_status_data, business_hours_data, on='store_id', how='left')

    # Then merge the result with timezone_data
    store_data = pd.merge(store_data, timezone_data, on='store_id', how='left')
    print(store_data.columns)

    business_hours = {}
    for _, row in store_data.iterrows():
        day_of_week = row['day']
        open_time = pd.Timestamp(row['start_time_local'])
        close_time = pd.Timestamp(row['end_time_local'])
        if not pd.isna(open_time) and not pd.isna(close_time):
            business_hours[day_of_week] = {'open': open_time.time(), 'close': close_time.time()}
        else:
            continue

    report_data = []

    for store_id, group in store_data.groupby('store_id'):
        store_data_group = store_data[store_data['store_id'] == store_id].copy()
        store_data_group['status'] = store_data_group['status'].apply(lambda x: 'active' if x == 'active' else 'inactive')
        if 'timezone_str' in store_data_group.columns and not store_data_group['timezone_str'].isnull().all():
            timezone = store_data_group['timezone_str'].values[0]
        else:
            timezone = 'America/Chicago'

        store_data_group['timestamp_utc'] = pd.to_datetime(store_data_group['timestamp_utc'])
        store_data_group['timestamp_utc'] = store_data_group['timestamp_utc'].dt.tz_localize('UTC').dt.tz_convert(timezone)
    
        result = calculate_uptime_downtime(store_id, store_data_group, business_hours, timezone, report_id)
        report_data.append(result)

    # Create a DataFrame from the report data
    report_df = pd.DataFrame(report_data, columns=['store_id', 'uptime_last_hour', 'uptime_last_day', 'uptime_last_week', 'downtime_last_hour', 'downtime_last_day', 'downtime_last_week', 'report_id'])

    # Save the report as a CSV
    report_csv = report_df.to_csv(index=False)
    
    # Return the CSV as a response
    response = HttpResponse(report_csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="store_report.csv"'
    return response

def generate_report_id(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def trigger_report(request):
    report_id = generate_report_id()
    response_data = {
        'report_id': report_id,
        'message': 'Report generation initiated. Use the report_id for status polling.',
    }
    return JsonResponse(response_data)