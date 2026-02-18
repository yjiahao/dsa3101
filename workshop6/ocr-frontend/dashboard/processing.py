import pandas as pd
import numpy as np

def preprocess(df):
    # Convert 'collectionTime' to datetime and extract date
    df['collectionTime'] = pd.to_datetime(df['collectionTime'], errors='coerce')
    df['Date'] = df['collectionTime'].dt.strftime('%d/%m/%Y')
    df['Time'] = df['selectedSession']

    # Get the reference weights for each date and session
    reference_weights = df[df['selectedReportingType'] == 'Reference'][[
        'Date', 'selectedSession', 'extractedWeight'
    ]]
    df = df[df['binCenterName'] != 'NUS - Use for Reference Weight']

    # Merge the reference weights back into the original dataframe based on date and session
    df = pd.merge(df,
                  reference_weights,
                  on=['Date', 'selectedSession'],
                  suffixes=('', '_ref'),
                  how='left')

    # Rename the merged column to 'referenceWeight'
    df.rename(columns={'extractedWeight_ref': 'referenceWeight'}, inplace=True)

    # Use manualWeight to calculate recordedWeight if manualWeight is not empty, else use extractedWeight
    df['recordedWeight'] = np.where(~pd.isna(df['manualWeight']),
                                    df['manualWeight'], df['extractedWeight'])

    df['recordedWeight'] = df['recordedWeight'] - df['referenceWeight']

    df['originalManualWeight'] = df['manualWeight'].copy()

    df['Image'] = "Click Here"
    
    # Add a column for discrepancy reason
    df['discrepancy_reason'] = np.nan

    # Detect same weight for the same date
    same_weight_mask = df.groupby('Date')['rfidWeight'].transform('nunique') == 1
    df.loc[same_weight_mask, 'discrepancy_reason'] = 'RFID Duplicates'
    

    # Detect missing weight records
    missing_weights_mask = df['rfidWeight'].isna()
    df.loc[missing_weights_mask, 'discrepancy_reason'] = 'Missing RFID'

    # Initialize the 'is_error' column
    df['is_error'] = False

    # Flag rows where manual weight is provided
    df.loc[~df['manualWeight'].isna(), 'is_error'] = True

    # Flag rows where extracted weight is below a certain threshold
    df.loc[df['extractedWeight'] < 160, 'is_error'] = True

    # Calculate IQR for anomaly detection
    Q1 = df['extractedWeight'].quantile(0.25)
    Q3 = df['extractedWeight'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Flag anomalies based on IQR
    df.loc[(df['extractedWeight'] < lower_bound) | (df['extractedWeight'] > upper_bound) | (df['recordedWeight'] <= 0), 'is_error'] = True

    # Reorder columns
    df = df[[
        'binCenterName', 'Date', 'Time', 'extractedWeight', 'referenceWeight',
        'manualWeight', 'rfidWeight', 'recordedWeight','image', 'Image', 'discrepancy_reason', 'is_error' 
    ]]
    df['is_abnormal'] = df['discrepancy_reason'].notna()

    df['is_edited'] = ~pd.isna(df['manualWeight'])

    df.reset_index(drop=True, inplace=True)

    return df



def preprocess_v2(df):

    # Use manualWeight to calculate recordedWeight if manualWeight is not empty, else use extractedWeight
    df['recordedWeight'] = np.where(~pd.isna(df['manualWeight']),
                                    df['manualWeight'], df['extractedWeight'])

    df['recordedWeight'] = df['recordedWeight'] - df['referenceWeight']

    df['originalManualWeight'] = df['manualWeight'].copy()

    df['Image'] = "Click Here"
    
    # Add a column for discrepancy reason
    df['discrepancy_reason'] = np.nan

    # Detect same weight for the same date
    same_weight_mask = df.groupby('Date')['rfidWeight'].transform('nunique') == 1
    df.loc[same_weight_mask, 'discrepancy_reason'] = 'RFID Duplicates'
    

    # Detect missing weight records
    missing_weights_mask = df['rfidWeight'].isna()
    df.loc[missing_weights_mask, 'discrepancy_reason'] = 'Missing RFID'

    # Initialize the 'is_error' column
    df['is_error'] = False

    # Flag rows where manual weight is provided
    df.loc[~df['manualWeight'].isna(), 'is_error'] = True

    # Flag rows where extracted weight is below a certain threshold
    df.loc[df['extractedWeight'] < 160, 'is_error'] = True

    # Calculate IQR for anomaly detection
    Q1 = df['extractedWeight'].quantile(0.25)
    Q3 = df['extractedWeight'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Flag anomalies based on IQR
    df.loc[(df['extractedWeight'] < lower_bound) | (df['extractedWeight'] > upper_bound) | (df['recordedWeight'] <= 0), 'is_error'] = True

    # Reorder columns
    df = df[[
        'binCenterName', 'Date', 'Time', 'extractedWeight', 'referenceWeight',
        'manualWeight', 'rfidWeight', 'recordedWeight','image', 'Image', 'discrepancy_reason', 'is_error' 
    ]]
    df['is_abnormal'] = df['discrepancy_reason'].notna()

    df['is_edited'] = ~pd.isna(df['manualWeight'])

    df.reset_index(drop=True, inplace=True)

    return df

def create_analytics_df(df):
    # Perform your existing preprocessing
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['is_abnormal'] = df['discrepancy_reason'].notna()
    df['is_edited'] = ~pd.isna(df['manualWeight'])
    
    # Create a new column to distinguish between performance errors and potential errors
    df['error_type'] = df.apply(
        lambda x: 'OCR Error' if x['is_edited'] else ('Potential Error' if x['is_error'] else 'No Error'), axis=1
    )
    
    # Group data by Date to count total readings
    total_readings_by_date = df.groupby(df['Date'].dt.date).size()
    
    # Group data by Date and error_type to count occurrences
    error_counts = df.groupby([df['Date'].dt.date, 'error_type']).size().unstack(fill_value=0)
    
    # Calculate the proportion of each error type out of the total readings per day
    error_proportions = error_counts.divide(total_readings_by_date, axis=0)*100
    
    # Reset index to turn 'Date' into a column and fill NA values with 0
    error_proportions.reset_index(inplace=True)
    error_proportions.fillna(0, inplace=True)
    
    # Include total readings in the DataFrame
    error_proportions['Total Readings'] = total_readings_by_date.values
    
    # Rename columns to reflect that they are proportions
    error_proportions.columns = ['Date', 'No Error Proportion', 'OCR Error', 'Potential Error', 'Total Readings']

    # Group data by Bin Center and error_type to count occurrences
    error_count_by_bin = df.groupby(['binCenterName', 'error_type']).size().unstack(fill_value=0).reset_index()

    # Filter RFID-related discrepancies and count them by Date and discrepancy_reason
    # Group data by Date and discrepancy_reason to count occurrences of each RFID error type
    rfid_issues_by_date = df[df['discrepancy_reason'].str.contains('RFID', na=False)]
    rfid_issues_by_date = rfid_issues_by_date.groupby([rfid_issues_by_date['Date'].dt.date, 'discrepancy_reason']).size().unstack(fill_value=0).reset_index()
    
    # Group data by Bin Center and discrepancy_reason to count occurrences of each RFID error type
    rfid_issues_by_bin = df[df['discrepancy_reason'].str.contains('RFID', na=False)]
    rfid_issues_by_bin = rfid_issues_by_bin.groupby(['binCenterName', 'discrepancy_reason']).size().unstack(fill_value=0).reset_index()


        # Return the processed DataFrame and the analytics DataFrames
    return error_proportions, error_count_by_bin, rfid_issues_by_date, rfid_issues_by_bin
