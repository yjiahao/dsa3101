import threading
import time
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, jsonify
import pandas as pd
from dashboard.app import create_dash_app
import mysql.connector
import os
import json 
from flask_cors import CORS,cross_origin
import random
import pandas as pd
import requests, io
import base64

df = pd.read_csv('./dashboard/extraction.csv')

app = Flask(__name__,  static_url_path='/static', static_folder='static')
CORS(app, supports_credentials=True)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_FOLDER'] = 'static/img'


def path_to_image_html(path):
    return '<img src="'+ path + '" width="200" height = "200">'

# Function to establish connection to MySQL database
def establish_sql_connection():
    db = mysql.connector.connect(
    host="mysql",
    user="counter1",
    password="counter1123",
    database="ocr"
    )
    return db

@app.route('/')
def index():
    db = establish_sql_connection()
    cursor = db.cursor()
    query = "SELECT binCenterID, binCenterName, binCenterLat, binCenterLon FROM bincenters"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    db.close()

    bin_centers = [{'binCenterID': row[0], 'binCenterName': row[1], 'binCenterLat': row[2], 'binCenterLon': row[3]} for row in result]

    return render_template('index.html', bin_centers=bin_centers)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' in request.files:
        image = request.files['image']
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        transformation_url = 'http://host.docker.internal:8000/number_extraction'

        # Read image data, encode it in base64, and send it in the POST request
        with open(os.path.join(app.config['UPLOAD_FOLDER'], image.filename), 'rb') as img_file:
            encoded_data = base64.b64encode(img_file.read()).decode()
        data = {'image_data': encoded_data}
        print(data)
        response = requests.post(transformation_url, json=data)
        response_json = response.json()
        return jsonify(response_json)
  
@app.route('/analytics', methods=['GET'])
def analytics():
    db = establish_sql_connection()
    cursor = db.cursor()

    query = "SELECT e.binCenterName, e.extractedWeight, e.manualWeight, e.collectionTime, e.latitude, e.longitude, e.selectedSession, e.selectedReportingType, i.image FROM extraction e LEFT JOIN images i ON e.collectionTime = i.collectionTime ORDER BY e.collectionTime DESC"
    cursor.execute(query)
    result = cursor.fetchall()

    processed_data = []

    for row in result:
        binCenterName, extractedWeight, manualWeight, collectionTime, latitude, longitude, selectedSession, selectedReportingType, image = row
        if image:  
            image_url = os.path.join(app.config['UPLOAD_FOLDER'], image)
        else:
            image_url = None  
        
        processed_data.append((binCenterName, extractedWeight, manualWeight, collectionTime, latitude, longitude, selectedSession, selectedReportingType, image_url))

    cursor.close()
    db.close()

    df = pd.DataFrame(processed_data, columns=['binCenterName', 'extractedWeight', 'manualWeight', 'collectionTime', 'latitude', 'longitude', 'selectedSession', 'selectedReportingType', 'image'])

    image_cols = ['image']
    format_dict = {}
    for image_col in image_cols:
        format_dict[image_col] = path_to_image_html

    return render_template('analytics.html', data=df.to_html(index=False, escape=False, formatters=format_dict))


@app.route('/results', methods=['POST'])
def submit_results():
  # Check if 'image' is in the request.files dictionary
  if 'image' in request.files:
    image = request.files['image']
    # Save the image and form data in the 'results' folder
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))

    # Retrieve other form fields
    extractedWeight = request.form.get('extractedWeight')
    extractedWeight = int(extractedWeight) if extractedWeight.lower() != 'null' else None
    selectedBinCenter = request.form.get('selectedBinCenter')
    timestamp = request.form.get('timestamp')
    manualWeight = request.form.get('manualWeightForm')
    manualWeight = int(manualWeight) if manualWeight.lower() != 'null' else None
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    selectedSession = request.form.get('selectedSession')
    selectedReportingType = request.form.get('selectedReportingType')

    # Create a dictionary to store the form data
    form_data = {
      'extractedWeight': extractedWeight,
      'selectedBinCenter': selectedBinCenter,
      'timestamp': timestamp,
      'manualWeight':manualWeight,
      'latitude': latitude,
      'longitude': longitude,
      'image': image.filename,
      'selectedSession': selectedSession,
      'selectedReportingType': selectedReportingType
    }

    # Serialize the form data to JSON and save it as a text file
    form_data_path = os.path.join(app.config['UPLOAD_FOLDER'], 'form_data.json')
    with open(form_data_path, 'w') as json_file:
        json.dump(form_data, json_file)

    db = establish_sql_connection()
    cursor = db.cursor()
    
    query = "INSERT INTO extraction (binCenterName, extractedWeight, manualWeight, collectionTime, latitude, longitude, selectedSession, selectedReportingType) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (selectedBinCenter, extractedWeight, manualWeight, timestamp, latitude, longitude, selectedSession, selectedReportingType))

    query2 = "INSERT INTO images (collectionTime, image) VALUES (%s, %s)"
    cursor.execute(query2, (timestamp, image.filename if image.filename else None))

    db.commit()
    cursor.close()
    db.close()

    # Return 200 to indicate success
    return "", 200
  else:
    return "Error"
  
def process_df():
    while True:
        # Path to the df.json file
        df_path = os.path.join("static", "df.json")
        # Check if df.json exists
        if os.path.exists(df_path):
            # Read the JSON file using with open
            with open(df_path, 'r') as f:
                json_data = f.read()
            api_endpoint = 'http://host.docker.internal:8000/data_transformation'

            # Send the JSON data in the request body
            response = requests.post(api_endpoint, json=json_data)

            # Check the response
            if response.status_code == 200:
                print('Data successfully sent for processing.')

                # Split the response into lines and process each line separately
                response_lines = response.text.strip().split('\n')
                
                # Assuming you want to save all lines to a single file
                df_cleaned_path = os.path.join("static", "df_cleaned.json")
                with open(df_cleaned_path, 'w') as output_file:
                    output_file.write("[")  # Add opening bracket before the first line
                    for line in response_lines:
                        try:
                            response_json = json.loads(line)
                            # Process the response_json as needed

                            # Write the entire line to the file
                            output_file.write(json.dumps(response_json, indent=4))
                            output_file.write(',\n')  # Add a comma and newline after each line

                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON: {e}")

                    output_file.write("]") 

            else:
                print('Error sending data. Status code:', response.status_code)

            break

            # Sleep for a while before checking again
        time.sleep(20)  # Adjust the interval as needed

create_dash_app(server=app,df=df)  # create Dash app instance

if __name__ == "__main__":
    process_thread = threading.Thread(target=process_df)
    process_thread.start()
    app.run(host='0.0.0.0', port="5000", debug=True)
