import streamlit as st
import pandas as pd
import MySQLdb
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

db_config = st.secrets["mysql"]
conn = MySQLdb.connect(
    host=db_config["host"],
    user=db_config["username"],
    passwd=db_config["password"],
    port=db_config["port"],
    db=db_config["database"]
)

cursor = conn.cursor()
query = "SELECT wing_width, wing_length, time_sec FROM measurements;"
cursor.execute(query)
columns = [desc[0] for desc in cursor.description]
results = cursor.fetchall()
df = pd.DataFrame(results, columns=columns)
cursor.close()
conn.close()

if df.empty:
    st.warning("No data available to visualise.")
    st.stop()

chart_type = st.sidebar.selectbox("Select Visualisation Type", [
    "Select a visualisation",
    "Heatmap",
    "Histogram",
    "Scatter Plot",
    "3D Surface Plot",
    "Line Plot (Fixed Wing Length)",
    "Line Plot (Fixed Wing Width)",
    "Box Plot (Fixed Wing Length)",
    "Box Plot (Fixed Wing Width)",
    "Bar Plot (Fixed Wing Length)",
    "Bar Plot (Fixed Wing Width)"
])

def apply_filters(df, wing_width_filter=None, wing_length_filter=None):
    if wing_width_filter:
        df = df[df['wing_width'].between(*wing_width_filter)]
    if wing_length_filter:
        df = df[df['wing_length'].between(*wing_length_filter)]
    return df

apply_ww_filter = chart_type in [
    "Heatmap", "Histogram", "Scatter Plot", "3D Surface Plot",
    "Line Plot (Fixed Wing Length)",
    "Box Plot (Fixed Wing Length)",
    "Bar Plot (Fixed Wing Length)"
]

apply_wl_filter = chart_type in [
    "Heatmap", "Histogram", "Scatter Plot", "3D Surface Plot",
    "Line Plot (Fixed Wing Width)",
    "Box Plot (Fixed Wing Width)",
    "Bar Plot (Fixed Wing Width)"
]

ww_min, ww_max, wl_min, wl_max = None, None, None, None
if apply_ww_filter:
    ww_min, ww_max = st.sidebar.slider("Filter Wing Width", float(df['wing_width'].min()), float(df['wing_width'].max()),
                                       (float(df['wing_width'].min()), float(df['wing_width'].max())))
if apply_wl_filter:
    wl_min, wl_max = st.sidebar.slider("Filter Wing Length", float(df['wing_length'].min()), float(df['wing_length'].max()),
                                       (float(df['wing_length'].min()), float(df['wing_length'].max())))

filtered_df = apply_filters(df,
                            (ww_min, ww_max) if apply_ww_filter else None,
                            (wl_min, wl_max) if apply_wl_filter else None)

if chart_type == "Heatmap":
    st.subheader("Heatmap")
    pivot = filtered_df.pivot_table(index='wing_length', columns='wing_width', values='time_sec', aggfunc='mean')
    fig = go.Figure(data=go.Heatmap(z=pivot.values, x=pivot.columns, y=pivot.index, colorscale='Viridis'))
    fig.update_layout(title="Heatmap of Time by Wing Width and Length", xaxis_title="Wing Width", yaxis_title="Wing Length")
    st.plotly_chart(fig, use_container_width=True, key="heatmap")

elif chart_type == "Histogram":
    st.subheader("Histogram")
    fig = px.histogram(filtered_df, x='time_sec', nbins=30, title="Distribution of Time")
    st.plotly_chart(fig, use_container_width=True, key="histogram")

elif chart_type == "Scatter Plot":
    st.subheader("Scatter Plot")
    vary_size = st.checkbox("Vary point size by time_sec", value=False)
    fig = px.scatter(
        filtered_df,
        x="wing_width",
        y="wing_length",
        size="time_sec" if vary_size else None,
        hover_data=["wing_width", "wing_length", "time_sec"]
    )
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "3D Surface Plot":
    st.subheader("3D Surface Plot")
    pivot = filtered_df.pivot_table(index='wing_length', columns='wing_width', values='time_sec', aggfunc='mean')
    fig = go.Figure(data=[go.Surface(z=pivot.values, x=pivot.columns, y=pivot.index)])
    fig.update_layout(title="3D Surface of Time", scene=dict(xaxis_title='Wing Width', yaxis_title='Wing Length', zaxis_title='Time (s)'))
    st.plotly_chart(fig, use_container_width=True, key="surface")

elif chart_type == "Line Plot (Fixed Wing Length)":
    st.subheader("Line Plot of Time vs Wing Width (at Fixed Wing Length)")
    selected_wl = st.selectbox("Select a wing length", sorted(df['wing_length'].unique()))
    subset_df = df[df['wing_length'] == selected_wl]
    agg_func = st.radio("Aggregation method", ["mean", "median"], key="agg_wl")
    if agg_func == "mean":
        aggregated_df = subset_df.groupby('wing_width')['time_sec'].mean().reset_index()
    else:
        aggregated_df = subset_df.groupby('wing_width')['time_sec'].median().reset_index()
    fig = px.line(aggregated_df, x='wing_width', y='time_sec',
                  title=f"Time vs Wing Width (Wing Length = {selected_wl})")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Line Plot (Fixed Wing Width)":
    st.subheader("Line Plot of Time vs Wing Length (at Fixed Wing Width)")
    selected_ww = st.selectbox("Select a wing width", sorted(df['wing_width'].unique()))
    subset_df = df[df['wing_width'] == selected_ww]
    agg_func = st.radio("Aggregation method", ["mean", "median"], key="agg_ww")
    if agg_func == "mean":
        aggregated_df = subset_df.groupby('wing_length')['time_sec'].mean().reset_index()
    else:
        aggregated_df = subset_df.groupby('wing_length')['time_sec'].median().reset_index()
    fig = px.line(aggregated_df, x='wing_length', y='time_sec',
                  title=f"Time vs Wing Length (Wing Width = {selected_ww})")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Box Plot (Fixed Wing Width)":
    st.subheader("Box Plot (at Fixed Wing Width)")
    fig = px.box(filtered_df, x='wing_width', y='time_sec', points=False,
                 title="Distribution of Time by Wing Width")
    st.plotly_chart(fig, use_container_width=True, key="box_w_width")

elif chart_type == "Box Plot (Fixed Wing Length)":
    st.subheader("Box Plot (at Fixed Wing Length)")
    fig = px.box(filtered_df, x='wing_length', y='time_sec', points=False,
                 title="Distribution of Time by Wing Length")
    st.plotly_chart(fig, use_container_width=True, key="box_w_length")

elif chart_type == "Bar Plot (Fixed Wing Width)":
    st.subheader("Bar Plot (at Fixed Wing Width)")
    agg_func = st.sidebar.radio("Aggregation Method", ["mean", "median"])
    bar_df = filtered_df.groupby('wing_width')['time_sec'].agg(agg_func).reset_index()
    fig = px.bar(bar_df, x='wing_width', y='time_sec',
                 title=f"{agg_func.title()} Time by Wing Width",
                 labels={'time_sec': f'{agg_func.title()} Time (s)', 'wing_width': 'Wing Width'})
    st.plotly_chart(fig, use_container_width=True, key="bar_w_width")

elif chart_type == "Bar Plot (Fixed Wing Length)":
    st.subheader("Bar Plot (at Fixed Wing Length)")
    agg_func = st.sidebar.radio("Aggregation Method", ["mean", "median"])
    bar_df = filtered_df.groupby('wing_length')['time_sec'].agg(agg_func).reset_index()
    fig = px.bar(bar_df, x='wing_length', y='time_sec',
                 title=f"{agg_func.title()} Time by Wing Length",
                 labels={'time_sec': f'{agg_func.title()} Time (s)', 'wing_length': 'Wing Length'})
    st.plotly_chart(fig, use_container_width=True, key="bar_w_length")
