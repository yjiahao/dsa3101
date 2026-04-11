import streamlit as st
import numpy as np
import pandas as pd
from flask import jsonify
import requests
import ast
from io import BytesIO


st.title("Workshop 8: Streamlit (Part II)")

st.header("What is data science?")

@st.cache_data
def load_module_data():
    files = {
        "NUS": "data/nus-dsa.csv",
        "NTU": "data/ntu.csv",
        "SMU": "data/smu.csv"
    }

    ### Get the module codes
    module_dict = {}
    for uni, path in files.items():
        df = pd.read_csv(path)
        module_codes = df.iloc[:, 0].dropna().astype(str).tolist()
        module_dict[uni] = module_codes

    return module_dict

@st.fragment
def checkpre():
    with st.form("pre"):
        mod_code = st.text_input("Enter the module you want to check prerequisite for (e.g. ST3131)")
        mod_past = st.text_input('Enter the module(s) you passed, separated by commas (e.g. ST1131:A, ST2131:D)')
        submitted1 = st.form_submit_button("Submit")
    if submitted1:
        mod_past_list = [mod.strip() for mod in mod_past.split(",")]
        url1 = f"http://backend:5000/prereq/{mod_code}"
        r1 = requests.post(url1, json=mod_past_list)
        if r1.json():
            st.success("Pre-req pass.")
        else:
            st.error("Pre-req fail.")
  
@st.fragment
def drawtree():
    mod_code = st.text_input("Enter the module (e.g., ST3236):")
    if mod_code:
        url1 = f"http://backend:5000/getgraph/{mod_code}" 
        r1 = requests.get(url1)
        if r1.status_code == 200:
            st.image(BytesIO(r1.content), caption=f"Prerequisite tree for {mod_code}")
        else:
            st.error(f"Request failed with code {r1.status_code}")

@st.fragment
def similarity3():
    with st.form("sim4"):
        col1, col2 = st.columns(2)
        with col1:
            uni1 = st.text_input("Enter the first University:")
            mod1 = st.text_input("Enter the first module:")
        with col2:
            uni2 = st.text_input("Enter the second University:")
            mod2 = st.text_input("Enter the second module:")
        submitted5 = st.form_submit_button("Submit")

    if submitted5:
        url1 = "http://backend:5000/similarity/concepts"
        params = {
            'uni1': uni1,
            'mod1': mod1,
            'uni2': uni2,
            'mod2': mod2
        }
        r1 = requests.get(url1, params=params)
        if r1.status_code == 200:
            st.write(f"""The similarity score between {uni1.upper()} {mod1.upper()}
            and {uni2.upper()} {mod2.upper()} is {r1.json():.2f}""")
        else:
            st.error(f"Request failed with code {r1.status_code}")


@st.fragment
def similarity():
    with st.form("sim"):
        col1, col2 = st.columns(2)
        with col1:
            uni1 = st.text_input("Enter the first University:")
        with col2:
            mod1 = st.text_input("Enter the first module:")
        submitted2 = st.form_submit_button("Save first pair")

    if submitted2:
        st.session_state["uni1"] = uni1
        st.session_state["mod1"] = mod1
        st.success("First university/module pair saved.")

    with st.form("sim2"):
        col1, col2 = st.columns(2)
        with col1:
            uni2 = st.text_input("Enter the second University:")
        with col2:
            mod2 = st.text_input("Enter the second module:")
        submitted3 = st.form_submit_button("Save second pair")
    
    if submitted3:
        st.session_state["uni2"] = uni2
        st.session_state["mod2"] = mod2
        st.success("Second university/module pair saved.")  

    if all(k in st.session_state for k in ["uni1", "mod1", "uni2", "mod2"]):
        if st.button("Calculate similarity"):
            url1 = "http://backend:5000/similarity/concepts"
            params = {
                "uni1": st.session_state["uni1"],
                "mod1": st.session_state["mod1"],
                "uni2": st.session_state["uni2"],
                "mod2": st.session_state["mod2"]
            }
            r1 = requests.get(url1, params=params)
            if r1.status_code == 200:
                st.write(
                    f"""The similarity score between
                    {st.session_state["uni1"].upper()} {st.session_state["mod1"].upper()}
                    and
                    {st.session_state["uni2"].upper()} {st.session_state["mod2"].upper()}
                    is {r1.json():.2f}"""
                )
            else:
                st.error(f"Request failed with code {r1.status_code}")

@st.fragment
def similarity2():
    module_dict = load_module_data()

    st.subheader("First pair")
    col1, col2 = st.columns(2)
    with col1:
        uni1 = st.selectbox(
            "Enter the first university",
            ["NUS", "NTU", "SMU"],
            key="uni1_select"
        )
    with col2:
        mod1 = st.selectbox(
            "Enter the first module",
            module_dict[uni1],
            key="mod1_select"
        )

    st.subheader("Second pair")
    col3, col4 = st.columns(2)
    with col3:
        uni2 = st.selectbox(
            "Enter the second university",
            ["NUS", "NTU", "SMU"],
            key="uni2_select"
        )
    with col4:
        mod2 = st.selectbox(
            "Enter the second module",
            module_dict[uni2],
            key="mod2_select"
        )  

    if st.button("Calculate similarity"):
        url1 = "http://backend:5000/similarity/concepts"
        params = {
            "uni1": uni1,
            "mod1": mod1,
            "uni2": uni2,
            "mod2": mod2
        }
        r1 = requests.get(url1, params=params)
        if r1.status_code == 200:
            st.write(
                f"""The similarity score between
                {uni1.upper()} {mod1.upper()}
                and
                {uni2.upper()} {mod2.upper()}
                is {r1.json():.2f}"""
            )
        else:
            st.error(f"Request failed with code {r1.status_code}")
    
st.subheader("Check prerequisite")
checkpre()

st.subheader("Plot prerequisite tree")
drawtree()

st.header("Original Form")
st.subheader("Calculate the similarity between two modules")
similarity3()

st.header("Task 1")
st.subheader("Calculate the similarity between two modules")
similarity()

st.header("Task 2")
st.subheader("Calculate the similarity between two modules")
similarity2()
