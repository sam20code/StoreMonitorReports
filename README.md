** (while cloning make sure files come in following hierarchy as snippet in `applicatonFileHierarchy` depicts, along with it download storeStatus csv file)

# StoreMonitor
This Python Django-based application generates uptime and downtime reports for multiple stores based on their status data. The application takes into account the business hours of each store and provides insights into their operational performance over various time intervals.

## Situation
----
I was tasked with developing a Django-based web application for monitoring the uptime and downtime of various stores. This application needed to calculate uptime and downtime statistics for each store based on status data, business hours, and time zones. The status data, business hours, and time zone information were provided in CSV files.
## Interpolation Issue:
---
## `Handling Missing Data`:

- I noticed that the data provided might have missing or irregular timestamps, which could lead to inaccuracies in calculating uptime and downtime.
- To address this, I began by using the sort_values method to ensure that the data is sorted by the 'timestamp_utc' column. This step was crucial as it prepared the data for time-based calculations.
## `Iterating Through Data`:

- I used a for loop to iterate through the rows of the sorted data, ensuring that the data was processed sequentially in time order.
- Within the loop, I converted the 'timestamp_utc' column to the appropriate time zone using tz_convert. This step ensured that all timestamps were consistently in the local time zone of the store being analyzed.
## `Day of the Week`:

- To determine the day of the week for each timestamp, I used the weekday() method on the 'timestamp_utc' column. This provided a numerical representation of the day (0 for Monday, 1 for Tuesday, and so on).
## `Business Hours Check`:

- I checked whether the timestamp fell within the defined business hours for the day of the week. This check was critical for calculating uptime during business hours and downtime outside of business hours.
- The 'business_hours' dictionary, which I prepared earlier, contained the opening and closing times for each day of the week.
## `Time Difference Calculation`:

- To calculate the time difference between consecutive data points, I subtracted the timestamp of the current row from the timestamp of the previous row. This gave me the time elapsed in seconds.
- I converted this time difference to minutes by dividing it by 60.
## `Uptime and Downtime Accumulation`:
- Based on the status of the store ('active' or 'inactive') and whether it was within business hours, I accumulated the time into variables:
  - uptime_last_hour: Uptime in the last hour
  - uptime_last_day: Uptime in the last day
  - uptime_last_week: Uptime in the last week
  - downtime_last_hour: Downtime in the last hour
  - downtime_last_day: Downtime in the last day
  - downtime_last_week: Downtime in the last week
## `Rounding Time`:

- I rounded the accumulated times to two decimal places, which provided a more readable format for the report.
## Action:
---
### `Data Preparation`:

- I imported the necessary libraries, including pandas for data manipulation.
- I defined a function calculate_uptime_downtime to calculate uptime and downtime for a given store based on its status data, business hours, and time zone.
- I read the status data, business hours, and time zone CSV files into Pandas DataFrames.
### `Data Merging`:
- I merged the status data with business hours data using the 'store_id' as the common key.
- I then merged the result with time zone data using the same 'store_id' key.

### `Business Hours Dictionary`:

I created a dictionary business_hours to store the opening and closing times for each day of the week for each store. This dictionary is based on the merged data.
### `Report Generation`:

- I initialized an empty list report_data to store the calculated statistics for each store.
- I iterated over the unique store IDs and grouped the data by store ID.
- For each store group, I:
- Made a copy of the group.
- Standardized the 'status' column values to 'active' or 'inactive'.
- Determined the time zone for the store.
- Converted the 'timestamp_utc' column to the store's time zone.
- Called the calculate_uptime_downtime function to calculate uptime and downtime for that store.
- Appended the results to report_data.

### `CSV Report`:

- I created a Pandas DataFrame report_df from report_data, defining columns for 'store_id', 'uptime_last_hour', 'uptime_last_day', 'uptime_last_week', 'downtime_last_hour', 'downtime_last_day', 'downtime_last_week'.
- I saved the DataFrame as a CSV file report_csv.
### `Response`:
- I created an HTTP response containing the CSV data.
- I set the content type to 'text/csv'.
- I configured the response to prompt the user to download the CSV file with the name "store_report.csv".

### `Result`:
- The script successfully calculates and generates a CSV report for each store's uptime and downtime statistics based on the provided status data, business hours, and time zones.
- This report can be easily downloaded and used for further analysis.

