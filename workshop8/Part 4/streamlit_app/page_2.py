import pandas as pd 
import streamlit as st
import requests

st.markdown("##  Data Preview")

st.sidebar.markdown("Input your pair id to see your data.")
group_id = st.sidebar.text_input("Group ID", "")

if group_id:
    res = requests.get("http://backend:5000/get_data", 
                       params={"group_id": group_id})
    if res.status_code == 200:
        data = res.json()
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.write("No data found for the given group ID.")
else:           
    res = requests.get("http://backend:5000/get_alldata")
    data = res.json()
    df = pd.DataFrame(data)
    st.dataframe(df)