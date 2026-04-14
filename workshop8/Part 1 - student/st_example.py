import streamlit as st
import pandas as pd
import time

st.title("Workshop 8: Streamlit")
st.title("(Part I: Introduction to Streamlit)")

# Basic display
st.header("Display")

st.write("Hello world!")
"Hello World * 2!"

st.text("Hello World * 3!")

st.markdown("**Hello** *World* * 4!")

st.success("✅ Success!")
st.info("ℹ️ Information message")
st.warning("⚠️ Warning!")
st.error("❌ Error occurred")

st.latex(r"e^{i\pi}=-1")  # r is to tell Python don't treat backslashes (\): just interpret the string literally.
st.code(r'st.latex(r"e^{i\pi}=-1")')
st.json({"Course Name": "Data Science in Practice", "Course Code": "DSA3101"})

# Display interactive widgets
st.header("Display interactive widgets")

text = st.text_input("Enter some text:")
st.write(f"Your input: {text}")

num = st.number_input("Enter a number:")
st.write(f"The square of {num} is ", num ** 2)

num = st.number_input("Enter an integer between 0 and 10:",
                      min_value=0,
                      max_value=10,
                      value=1,
                      step=1)
st.write(f"The square of {num} is ", num ** 2)

num = st.slider("Select a number:", min_value=0.0, max_value=10.0, step=0.1)
st.write(f"The square root of {num} is ", num ** (1/2))

num = st.radio("Radio", [1,2,5])
st.write("You selected ", num)

color = st.selectbox("Pick a color", ["Red", "Yellow", "Blue"])
st.write("You picked ", color)

checked = st.checkbox("Check")
if checked:
    st.write("Hello World!")

clicked = st.button("Click me!")
if clicked:
    st.write("Boom💣")

# Form: a container that visually groups other elements and widgets together, and always contains a Submit button 
st.header("Form")

with st.form("form0"):
    lname = st.text_input("Enter your last name:")
    fname = st.text_input("Enter your first name:")
    submitted = st.form_submit_button("Submit")
if submitted:
    st.write(f"Hi {fname} {lname}, welcome to DSA3101 Workshop 8.")

# Compare with widgets not using Form
lname1 = st.text_input("Enter your last name again:")
fname1 = st.text_input("Enter your first name again:")
st.write(f"Hi {fname1} {lname1}!")

# Rerun and session
st.header("Rerun and session")

# A todo list example
todo_list = ["Wk7"]
st.write(f'My current todo list is: {todo_list}.')
new_totdo = st.text_input('Enter your next todo item:')
if st.button('Add the new todo item'):
    todo_list.append(new_totdo)
    st.write(f'My new todo list is: {todo_list}.')

st.markdown("User's past input not recorded.")
    
st.divider()
st.markdown("A **rerun**: the entire python script is re-executed from top to bottom.")
st.markdown("A rerun happens when the python code is modified, or a widget is interacted.")
st.markdown("Variables declared in the script are *not persistent* across reruns.")
st.markdown("To persist variable across reruns, use **st.session_state**.")

st.markdown("""A **session** is a single instance of viewing an app. 
            If you view an app from two different tabs in your browser, 
            each tab will have its own session. If the user refreshes their browser page 
            or reloads the URL to the app, the session resets.""")


st.header("Session State")

# The todo list example revisited: using st.session_state
if "todo_list" not in st.session_state:
    st.session_state.todo_list = ["Wk7"]
new_totdo = st.text_input('Enter your next todo item again:')
if st.button('Add the new todo item again'):
    st.session_state.todo_list.append(new_totdo)
st.write(f'My new todo list is: {st.session_state.todo_list}.')
st.markdown("User's past input not recorded by using st.session_state.")

st.divider()
# Another example about session state and button

# without st.session_state
clicked = st.button("Click me")
if clicked:
    st.write("✅ Button was clicked!")
else:
    st.write("❌ Waiting for click...")

# with st.session_state
st.divider()
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False
if st.button("Click me again"):
    st.session_state.button_clicked = True
if st.session_state.button_clicked:
    st.write("✅ Button was clicked!")
else:
    st.write("❌ Waiting for click...")

st.markdown("""Some widgets like st.button, st.form_submit_button, 
            do not persist any internal state, unless you explicitly manage it using st.session_state.""")
st.markdown("""On the first rerun after the button is clicked, it returns True.
            On all subsequent reruns, it returns False — unless the button is clicked again.""")

st.header("Fragment")
st.markdown("""Streamlit lets you turn functions into fragments, 
            which can rerun independently from the full script. 
            When a user interacts with a widget inside a fragment, 
            only the fragment reruns.""")
st.markdown("Use **@st.fragment** decorator to define the function.")

st.header("Caching")
st.markdown("""The basic idea behind caching is to store the results of 
            expensive function calls and return the cached result 
            when the same inputs occur again. 
            This avoids repeated execution of a function with the same input values.""")
st.markdown("Use **@st.cache_data** or **@st.cache_resource** decorator to define the function.")

@st.cache_data()
def preview(filename):
    time.sleep(5)
    df = pd.read_csv(filename)
    st.dataframe(df.head(3))
    
preview('data/nus-dsa.csv')
