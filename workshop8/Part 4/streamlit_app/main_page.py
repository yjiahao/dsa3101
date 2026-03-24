import streamlit as st
import pandas as pd
import requests


st.set_page_config(page_title="Wing Data Entry", layout="wide")

# Main page content
st.markdown("""
            Welcome to DSDS Enrichment Day! As you conduct your helicopter 
            experiments, please upload your data in the table below. Once you 
            click Submit, your data will be sent to the database. Before you click Submit,
            please ensure that you have clicked out of the table once. There should not be any red-outlined 
            cells when you click Submit.

            You can then view your data on the **Data Preview** page.
           """)

st.markdown("""
Here is a description of the columns:
            
- **wing_width**: The width of the wing in cm. (numeric)
- **wing_length**: The length of the wing in cm. (numeric)
- **sequence_id**: The iteration number for this particular helicopter.  (integer)
- **time_sec**: The time taken for the bottom of the helicopter to touch the ground, in seconds. (numeric)
- **heli_id**: An integer label id for this particular helicopter. (integer)
- **group_id**: The ID of the group conducting the experiment. (string, e.g. "tmnt")
""")


# Function to submit data to the database
with st.form("data_entry_form"):
    n_rows = 5     

    df = pd.DataFrame({
        "wing_width": [0.0]*n_rows,
        "wing_length": [0.0]*n_rows,
        "sequence_id": [1,2,3,4,5],
        "time_sec": [0.0]*n_rows,
        "heli_id": [0]*n_rows, 
        "group_id": [""]*n_rows,
    })

    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    submitted = st.form_submit_button("Submit")

if submitted:
    # submit to db
    json_data = edited_df.to_json(orient="records")
    res = requests.post("http://backend:5000/add_data",
                        json={"data": json_data})
    if res.status_code == 200:
        st.success(f"{edited_df.shape[0]} row(s) of data uploaded successfully.")