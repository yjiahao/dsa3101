import pandas as pd 
import streamlit as st
import MySQLdb

st.markdown("##  Data Preview")

st.sidebar.markdown("Input your pair id to see your data.")

group_id = st.sidebar.text_input("Group ID", "")

db_config = st.secrets["mysql"]

conn = MySQLdb.connect(
     host=db_config["host"],
     user=db_config["username"],
     passwd=db_config["password"],
     port=db_config["port"],
     db=db_config["database"]
     )

if group_id:
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT * FROM measurements WHERE group_id = '{group_id}';
                    """)
    # Get column names from cursor
    columns = [desc[0] for desc in cursor.description]
    # Fetch all results
    results = cursor.fetchall()
    # Create DataFrame
    df = pd.DataFrame(results, columns=columns)
    cursor.close()
    conn.close()
    
    if not df.empty:
        st.dataframe(df)
    else:
        st.write("No data found for the given group ID.")

