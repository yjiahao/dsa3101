import streamlit as st
import numpy as np
import pandas as pd

import utils

st.header("What is data science?")
# nus_dsa_df = pd.read_csv('data/nus-dsa.csv')
# smu_df = pd.read_csv('data/smu.csv')
# ntu_df = pd.read_csv('data/ntu.csv')

# # Show the first few rows 
# st.subheader("Data preview")
# st.dataframe(nus_dsa_df.head(3))

# # Histogram for sentiment ratings of NUS modules
# st.subheader("Sentiment rating distribution")
# counts, bin_edges = np.histogram(nus_dsa_df["sentiment_rating"], bins=20)
# hist_df = pd.DataFrame({
#     "bin_left": np.round(bin_edges[:-1], 2),
#     "count": counts
# })
# st.bar_chart(hist_df.set_index("bin_left"))

# # Calculate the similartity between two modules 
# st.subheader("Calculating the similarity between two modules")

# # Helper function to switch to the corresponding dataset
# def switch(uni_name):
#     if uni_name.lower() == "nus":
#         return nus_dsa_df
#     elif uni_name.lower() == "ntu":
#         return ntu_df
#     else:
#         return smu_df

# # Helper function to calculate the similarity between mod1 from uni1 and mod2 from uni2
# def compute_sim_concepts(uni1, mod1, uni2, mod2):
#     uni1 = switch(uni1)
#     uni2 = switch(uni2)
#     k1 = uni1[uni1.module_code == mod1].key_concepts.iloc[0] 
#     k2 = uni2[uni2.module_code == mod2].key_concepts.iloc[0] 

#     sim_score = utils.jacc_sim(k1, k2)

#     return sim_score

# # Display the similarity between DSA2101 and DSA1101
# score = compute_sim_concepts("NUS", "DSA2101", "nus", "DSA1101")
# st.write(f'The similarity score between NUS DSA2101 and NUS DSA1101 is {score}.')

# # Get user's input, and then calculate the similarity
# with st.form('form_sim'):
#     uni1 = st.text_input("Enter the first university:")
#     mod1 = st.text_input("Enter the first module:")    
#     uni2 = st.text_input("Enter the second university:")
#     mod2 = st.text_input("Enter the second module:")
#     submitted_sim = st.form_submit_button("Submit")

# if submitted_sim:
#     score = compute_sim_concepts(uni1, mod1, uni2, mod2)
#     st.write(f'The similarity score between {uni1} {mod1} and {uni2} {mod2} is {score}.')