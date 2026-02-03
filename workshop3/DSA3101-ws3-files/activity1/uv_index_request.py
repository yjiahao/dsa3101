import requests
import csv
import os

# Get from environment variable, or use default
datetime_str = os.environ.get('DATETIME_STR', '2025-08-03T19:00:00')
print(f"Using datetime: {datetime_str}")

params = {'date': datetime_str}

url = 'https://api-open.data.gov.sg/v2/real-time/api/uv'

response = requests.get(url, params=params)
data = response.json()

# Extract the relevant data from the API response
records = data.get('data', {}).get('records', [])
csv_rows = []

# Add timezone info, as in the returned data
target_datetime = datetime_str + '+08:00'

for record in records:
    for uv in record.get('index', []):
        hour = uv.get('hour')
        value = uv.get('value')
        if hour == target_datetime:
            print(f"Timestamp: {hour}, UV Index: {value}")
            csv_rows.append([hour, value])

# Create a dynamic CSV file name based on the date/time
csv_file = f'uv_index_{datetime_str.replace(":", "-")}.csv'

if csv_rows:
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'uv_index'])
        writer.writerows(csv_rows)
    print(f"\nUV index data written to {csv_file}")
else:
    print("No UV index data found for the specified time.")