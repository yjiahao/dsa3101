import streamlit as st

# Define the pages
main_page = st.Page("main_page.py", title="Data Entry")
page_2 = st.Page("page_2.py", title="Data Preview")
#page_3 = st.Page("page_3.py", title="Data Visualisation")

# Set up navigation
pg = st.navigation([main_page, page_2])

# Run the selected page
pg.run()
