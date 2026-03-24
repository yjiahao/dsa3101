import streamlit as st

# Define the pages
main_page = st.Page("st_example.py", title="Introduction to Streamlit")
page_2 = st.Page("datascience.py", title="An Example")

# Set up navigation
pg = st.navigation([main_page, page_2])

# Run the selected page
pg.run()