# Streamlit Exam Master Document (Detailed, Verbose, and Practical)

This document is an exam-focused, detailed reference for Streamlit.
It is intentionally long and explicit so you can revise quickly without hunting through official docs.

## 1) What Streamlit Is and Why It Is Different

Streamlit is a Python framework for building data/web apps with very little frontend code.

Key idea:
- You write a normal Python script.
- Every user interaction (button click, slider change, text input update) can trigger a rerun of the script from top to bottom.
- Streamlit keeps widget values and session state so your app still feels interactive.

This rerun model is the most important concept for exams and interviews.

## 2) Core Execution Model (Must Understand)

### 2.1 Top-to-bottom rerun

When an input widget value changes:
1. Streamlit updates internal widget state.
2. Optional callback (`on_change`, `on_click`) runs.
3. Script reruns from the first line.

Implication:
- Never assume line-by-line persistent execution like a notebook cell.
- Use `st.session_state` for values that must persist across reruns.

### 2.2 Widget identity and keys

Widgets are identified by label + placement + optional `key`.

Best practice:
- Always provide explicit `key` for important widgets.

### 2.3 Stateless code vs stateful UI

Your script file is stateless by default, but Streamlit session state makes UI stateful per browser session.

## 3) Streamlit Setup and Minimal App

Install:

```bash
pip install streamlit
```

Create file `app.py`:

```python
import streamlit as st

# Sets browser tab title and layout behavior for this app page.
# Important: call this near the top before most UI elements.
st.set_page_config(
	page_title="My First Streamlit App",
	page_icon="📘",
	layout="wide",  # "centered" or "wide"
	initial_sidebar_state="expanded",  # "auto" | "expanded" | "collapsed"
)

# st.title renders a top-level heading on the page.
st.title("Hello Streamlit")

# st.write is a convenience function that can display strings, numbers,
# DataFrames, markdown-like text, and many Python objects automatically.
st.write("This is a minimal app.")
```

Run:

```bash
streamlit run app.py
```

## 4) Text and Display APIs

### 4.1 `st.title`, `st.header`, `st.subheader`, `st.caption`, `st.text`

Purpose:
- Structured text hierarchy.

Example:

```python
import streamlit as st

st.title("Main App Title")
st.header("Section Header")
st.subheader("Subsection Header")
st.caption("Small helper text / metadata")
st.text("Fixed-width plain text block")
```

### 4.2 `st.markdown`

Purpose:
- Render markdown, links, bullet lists, inline code.
- Can render HTML only when `unsafe_allow_html=True` (use carefully).

```python
import streamlit as st

# Markdown for rich text formatting.
st.markdown("""
### Markdown Area
- Item 1
- Item 2
`inline code`
""")

# Avoid unsafe HTML unless necessary.
# st.markdown("<b>bold via HTML</b>", unsafe_allow_html=True)
```

### 4.3 `st.write`

Purpose:
- General-purpose output function.

```python
import streamlit as st
import pandas as pd

df = pd.DataFrame({"name": ["Alice", "Bob"], "score": [88, 92]})

# st.write auto-detects object type and renders a suitable view.
st.write("Quick message")
st.write(123)
st.write(df)
```

### 4.4 `st.code`, `st.latex`, `st.metric`, `st.json`

Purpose:
- Render code, equations, KPI metrics, and JSON.

```python
import streamlit as st

st.code("print('hello world')", language="python")

# LaTeX equation rendering.
st.latex(r"\hat{y} = \beta_0 + \beta_1 x")

# KPI card-like display.
st.metric(label="Daily Active Users", value="1,240", delta="+5.2%")

# Pretty-prints dictionary/list JSON content.
st.json({"model": "xgboost", "accuracy": 0.941})
```

## 5) Input Widgets (High-Value Exam Section)

### 5.1 `st.button`

Purpose:
- Trigger one-time action on click.
- Returns `True` only on rerun immediately after click.

```python
import streamlit as st

# Returns True once when clicked, then False on later reruns unless clicked again.
if st.button("Run Training", key="train_button"):
	st.success("Training started")
```

### 5.2 `st.checkbox`, `st.toggle`

Purpose:
- Boolean input.

```python
import streamlit as st

show_debug = st.checkbox("Show debug info", value=False, key="show_debug")

# toggle behaves similarly but with switch-like UI.
use_cache = st.toggle("Use cache", value=True, key="use_cache")

if show_debug:
	st.write("Debug panel visible")
```

### 5.3 `st.radio`, `st.selectbox`, `st.multiselect`, `st.pills`, `st.segmented_control`

Purpose:
- Single/multi choice selection.

```python
import streamlit as st

model = st.radio(
	"Choose model type",
	options=["Linear Regression", "Random Forest", "XGBoost"],
	index=1,
	key="model_radio",
)

city = st.selectbox(
	"Choose city",
	options=["Singapore", "Tokyo", "Seoul"],
	index=0,
	key="city_select",
)

features = st.multiselect(
	"Select features",
	options=["gpa", "income", "experience", "age"],
	default=["gpa", "experience"],
	key="feature_multiselect",
)

st.write("Model:", model)
st.write("City:", city)
st.write("Features:", features)
```

### 5.4 `st.slider`, `st.select_slider`, `st.number_input`

Purpose:
- Numeric and ordinal input.

```python
import streamlit as st

learning_rate = st.slider(
	"Learning rate",
	min_value=0.001,
	max_value=0.3,
	value=0.05,
	step=0.001,
	key="learning_rate_slider",
)

epoch_count = st.number_input(
	"Epochs",
	min_value=1,
	max_value=1000,
	value=100,
	step=1,
	key="epochs_input",
)

size_label = st.select_slider(
	"Dataset size",
	options=["small", "medium", "large"],
	value="medium",
	key="dataset_size_slider",
)

st.write(learning_rate, epoch_count, size_label)
```

### 5.5 `st.text_input`, `st.text_area`, `st.chat_input`

Purpose:
- Text capture (single line, multiline, and chat-style).

```python
import streamlit as st

name = st.text_input("Your name", placeholder="Enter full name", key="name_input")

notes = st.text_area(
	"Experiment notes",
	height=120,
	placeholder="Write your observations...",
	key="notes_area",
)

prompt = st.chat_input("Ask something", key="chat_prompt")

if prompt:
	st.write(f"You asked: {prompt}")
```

### 5.6 `st.date_input`, `st.time_input`

Purpose:
- Date/time selection.

```python
import datetime as dt
import streamlit as st

chosen_date = st.date_input("Pick date", value=dt.date.today(), key="date_picker")
chosen_time = st.time_input("Pick time", value=dt.time(9, 0), key="time_picker")

st.write("Date:", chosen_date)
st.write("Time:", chosen_time)
```

### 5.7 `st.file_uploader`, `st.camera_input`

Purpose:
- Upload files or capture camera images.

```python
import pandas as pd
import streamlit as st

uploaded_csv = st.file_uploader("Upload CSV", type=["csv"], key="csv_upload")

if uploaded_csv is not None:
	# Reads uploaded file object directly into DataFrame.
	df = pd.read_csv(uploaded_csv)
	st.dataframe(df)

photo = st.camera_input("Take a photo", key="camera_capture")
if photo is not None:
	st.image(photo, caption="Captured image")
```

### 5.8 `st.color_picker`

Purpose:
- Hex color selection.

```python
import streamlit as st

chosen_color = st.color_picker("Pick a highlight color", value="#00A86B", key="color_picker")
st.write("Selected:", chosen_color)
```

## 6) Data Display and Tables

### 6.1 `st.dataframe` vs `st.table`

Purpose:
- `st.dataframe`: interactive scroll/sort.
- `st.table`: static table.

```python
import pandas as pd
import streamlit as st

df = pd.DataFrame({"x": [1, 2, 3], "y": [10, 20, 30]})

st.dataframe(df, use_container_width=True)
st.table(df)
```

### 6.2 `st.data_editor`

Purpose:
- Editable table UI; can return edited values.

```python
import pandas as pd
import streamlit as st

source_df = pd.DataFrame(
	{
		"student": ["Ann", "Ben", "Cara"],
		"score": [78, 85, 91],
	}
)

# Returns a DataFrame with user edits.
edited_df = st.data_editor(source_df, num_rows="dynamic", key="score_editor")
st.write("Edited result")
st.dataframe(edited_df)
```

## 7) Charts and Visualization APIs

### 7.1 Built-in quick charts

`st.line_chart`, `st.bar_chart`, `st.area_chart` for fast plotting.

```python
import pandas as pd
import streamlit as st

chart_df = pd.DataFrame(
	{
		"day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
		"sales": [100, 120, 115, 140, 160],
	}
).set_index("day")

st.line_chart(chart_df)
st.bar_chart(chart_df)
st.area_chart(chart_df)
```

### 7.2 `st.pyplot`, `st.altair_chart`, `st.plotly_chart`, `st.vega_lite_chart`

Purpose:
- Display third-party plotting library figures.

```python
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title("Sine Wave")

# Renders Matplotlib figure inside Streamlit app.
st.pyplot(fig)
```

## 8) Media APIs

### 8.1 `st.image`, `st.audio`, `st.video`

Purpose:
- Show image/audio/video from file path, URL, bytes, uploaded object.

```python
import streamlit as st

# Local path example if file exists.
# st.image("assets/logo.png", caption="Logo")

# URL example.
st.image("https://picsum.photos/600/200", caption="Sample image from URL")

# Audio/video examples (commented unless files exist).
# st.audio("sample.mp3")
# st.video("sample.mp4")
```

### 8.2 `st.download_button`

Purpose:
- Let users download generated text/data/files.

```python
import io
import pandas as pd
import streamlit as st

df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

buffer = io.StringIO()
df.to_csv(buffer, index=False)
csv_data = buffer.getvalue()

st.download_button(
	label="Download CSV",
	data=csv_data,
	file_name="export.csv",
	mime="text/csv",
	key="download_csv_button",
)
```

## 9) Layout APIs (Frequently Tested)

### 9.1 `st.sidebar`

Purpose:
- Separate controls from main content.

```python
import streamlit as st

st.sidebar.title("Control Panel")
threshold = st.sidebar.slider("Threshold", 0.0, 1.0, 0.5, key="sidebar_threshold")
st.write("Threshold:", threshold)
```

### 9.2 `st.columns`

Purpose:
- Horizontal layout.

```python
import streamlit as st

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
	st.write("Left")
with col2:
	st.write("Center (wider)")
with col3:
	st.write("Right")
```

### 9.3 `st.tabs`, `st.expander`, `st.container`, `st.empty`

Purpose:
- Organize sections and dynamic placeholders.

```python
import time
import streamlit as st

tab1, tab2 = st.tabs(["Overview", "Details"])

with tab1:
	st.write("Overview content")

with tab2:
	st.write("Detailed content")

with st.expander("Click to expand"):
	st.write("Hidden until expanded")

box = st.container(border=True)
with box:
	st.write("Grouped in one container")

placeholder = st.empty()
placeholder.write("Loading...")
time.sleep(0.2)
placeholder.success("Done")
```

## 10) Status and Feedback APIs

### 10.1 `st.success`, `st.info`, `st.warning`, `st.error`, `st.exception`

Purpose:
- Communicate state clearly.

```python
import streamlit as st

st.success("Operation completed")
st.info("This is informational")
st.warning("Please check your input")
st.error("Something failed")

try:
	1 / 0
except Exception as exc:
	st.exception(exc)
```

### 10.2 `st.progress`, `st.spinner`, `st.toast`, `st.balloons`, `st.snow`

Purpose:
- Progress and celebration effects.

```python
import time
import streamlit as st

with st.spinner("Processing..."):
	progress = st.progress(0)
	for i in range(1, 101):
		time.sleep(0.005)
		progress.progress(i)

st.toast("Completed", icon="✅")
# st.balloons()
# st.snow()
```

### 10.3 `st.status`

Purpose:
- Multi-step status container.

```python
import time
import streamlit as st

with st.status("Running pipeline", expanded=True) as status:
	st.write("Step 1: Load data")
	time.sleep(0.2)
	st.write("Step 2: Train model")
	time.sleep(0.2)
	status.update(label="Pipeline complete", state="complete")
```

## 11) Control Flow APIs

### 11.1 `st.stop`

Purpose:
- Stop script execution immediately (without crashing).

```python
import streamlit as st

api_key = st.text_input("API key", type="password", key="api_key_input")
if not api_key:
	st.warning("Please provide API key")
	st.stop()  # Prevents execution of code below until key exists.

st.success("Key received, continuing...")
```

### 11.2 `st.rerun`

Purpose:
- Programmatically trigger rerun.

```python
import streamlit as st

if "count" not in st.session_state:
	st.session_state.count = 0

if st.button("Increment", key="increment_button"):
	st.session_state.count += 1
	st.rerun()  # Force immediate redraw with updated state.

st.write("Count:", st.session_state.count)
```

### 11.3 `st.switch_page` (for multipage apps)

Purpose:
- Navigate to another page script.

```python
import streamlit as st

# Requires multipage setup in a pages/ folder.
# if st.button("Go to Analytics"):
#     st.switch_page("pages/2_Analytics.py")
```

## 12) Forms and Event Handling

### 12.1 `st.form` and `st.form_submit_button`

Purpose:
- Batch multiple inputs and submit once.

```python
import streamlit as st

with st.form("user_form"):
	username = st.text_input("Username", key="form_username")
	age = st.number_input("Age", min_value=1, max_value=120, value=20, key="form_age")

	# Submit button only valid inside a form.
	submitted = st.form_submit_button("Submit")

if submitted:
	st.success(f"Saved {username}, age {age}")
```

When to use form:
- Prevent rerun after every single input change.
- Collect related inputs as one transaction.

### 12.2 Callbacks (`on_change`, `on_click`)

Purpose:
- Trigger function when widget changes/clicks.

```python
import streamlit as st

if "name_upper" not in st.session_state:
	st.session_state.name_upper = ""

def sync_uppercase() -> None:
	# Callback reads source widget value from session_state,
	# then updates another state key.
	st.session_state.name_upper = st.session_state.raw_name.upper()

st.text_input(
	"Name",
	key="raw_name",
	on_change=sync_uppercase,
)

st.write("Uppercase:", st.session_state.name_upper)
```

## 13) Session State (`st.session_state`) Deep Dive

Purpose:
- Persist data per user session across reruns.

Common operations:

```python
import streamlit as st

# Initialize once.
if "counter" not in st.session_state:
	st.session_state.counter = 0

# Read value.
st.write("Counter:", st.session_state.counter)

# Mutate value.
if st.button("+1", key="plus_one"):
	st.session_state.counter += 1

# Delete a key.
if st.button("Reset", key="reset_counter"):
	del st.session_state["counter"]
	st.rerun()
```

Pitfalls:
- Accessing missing key raises exception if not initialized.
- Keep key names consistent across widgets/state.

## 14) Caching (`st.cache_data`, `st.cache_resource`)

### 14.1 `st.cache_data`

Purpose:
- Cache return values of pure-ish data functions.

```python
import pandas as pd
import streamlit as st

@st.cache_data(ttl=600)
def load_data(path: str) -> pd.DataFrame:
	# Expensive read is cached for 10 minutes.
	return pd.read_csv(path)

# Repeated calls with same argument avoid disk read.
# df = load_data("data.csv")
```

### 14.2 `st.cache_resource`

Purpose:
- Cache heavy global resources (model connections, DB engines, clients).

```python
import streamlit as st

@st.cache_resource
def get_big_model():
	# Pretend this is expensive to initialize.
	return {"name": "demo-model", "version": "1.0"}

model = get_big_model()
st.write(model)
```

Rule of thumb:
- Data result cache: `cache_data`.
- Shared heavyweight object cache: `cache_resource`.

## 15) Chat APIs

### 15.1 `st.chat_message` + `st.chat_input`

Purpose:
- Build conversational interfaces.

```python
import streamlit as st

if "messages" not in st.session_state:
	st.session_state.messages = []

# Display existing message history.
for msg in st.session_state.messages:
	with st.chat_message(msg["role"]):
		st.write(msg["content"])

user_prompt = st.chat_input("Send a message", key="chat_box")
if user_prompt:
	st.session_state.messages.append({"role": "user", "content": user_prompt})

	# Very simple bot echo.
	bot_reply = f"Echo: {user_prompt}"
	st.session_state.messages.append({"role": "assistant", "content": bot_reply})
	st.rerun()
```

## 16) Sidebar Patterns

Common exam pattern:
1. Put filters in sidebar.
2. Use filters in main area.
3. Show KPIs + chart + table.

```python
import pandas as pd
import streamlit as st

df = pd.DataFrame(
	{
		"region": ["N", "S", "E", "W"],
		"sales": [120, 90, 110, 130],
	}
)

st.sidebar.header("Filters")
selected = st.sidebar.multiselect(
	"Regions",
	options=df["region"].tolist(),
	default=df["region"].tolist(),
	key="region_filter",
)

filtered = df[df["region"].isin(selected)]

st.metric("Total Sales", int(filtered["sales"].sum()))
st.bar_chart(filtered.set_index("region"))
st.dataframe(filtered)
```

## 17) Multipage Apps

Folder structure:

```text
my_app/
  app.py
  pages/
	1_Overview.py
	2_Modeling.py
	3_Reports.py
```

Behavior:
- Streamlit auto-detects pages.
- Sidebar displays page navigation.

Tip:
- Share utilities in separate modules and import them.

## 18) Common Errors and Exam Pitfalls

1. Forgetting rerun behavior and expecting notebook-like persistence.
2. Using mutable globals instead of `st.session_state`.
3. Not initializing `session_state` keys before reading.
4. Recomputing expensive functions each rerun because no cache.
5. Using duplicated widget labels without keys in complex layouts.
6. Putting form submit button outside `st.form`.
7. Attempting heavy blocking loops without feedback (`st.progress` / `st.status`).
8. Mixing chart libraries without careful figure handling.

## 19) End-to-End Simple Streamlit App (Runnable)

This sample app includes many components listed above:
- Page config
- Sidebar filters
- Text inputs
- Numeric widgets
- Form
- Session state
- Data editor
- Charts
- Metrics
- Download button
- Status/progress

```python
# app.py
import io
import time
import pandas as pd
import streamlit as st

# ------------------------------------------------------------
# 1) Page setup
# ------------------------------------------------------------
st.set_page_config(
	page_title="Streamlit Exam Demo",
	page_icon="🧪",
	layout="wide",
	initial_sidebar_state="expanded",
)

st.title("Streamlit Exam Demo App")
st.caption("A compact app demonstrating common Streamlit APIs")

# ------------------------------------------------------------
# 2) Session state initialization
# ------------------------------------------------------------
if "submit_count" not in st.session_state:
	st.session_state.submit_count = 0

# ------------------------------------------------------------
# 3) Sidebar controls
# ------------------------------------------------------------
st.sidebar.header("Control Panel")
min_score = st.sidebar.slider("Minimum score", 0, 100, 50, key="min_score_slider")
show_table = st.sidebar.checkbox("Show table", value=True, key="show_table_checkbox")

# ------------------------------------------------------------
# 4) Data source (small static dataset for demo)
# ------------------------------------------------------------
df = pd.DataFrame(
	{
		"student": ["Alice", "Ben", "Cara", "Dev", "Eli"],
		"score": [78, 85, 91, 66, 88],
		"hours_studied": [6, 8, 9, 4, 7],
	}
)

filtered_df = df[df["score"] >= min_score]

# ------------------------------------------------------------
# 5) Main layout with columns
# ------------------------------------------------------------
left, right = st.columns([2, 1])

with left:
	st.subheader("Editable Data")

	# data_editor returns user-edited DataFrame.
	edited_df = st.data_editor(filtered_df, key="editable_df")

	if show_table:
		st.dataframe(edited_df, use_container_width=True)

with right:
	st.subheader("KPIs")
	st.metric("Rows", len(edited_df))
	st.metric("Average Score", round(float(edited_df["score"].mean()), 2) if len(edited_df) else 0)

# ------------------------------------------------------------
# 6) Simple chart
# ------------------------------------------------------------
st.subheader("Score Chart")
if len(edited_df):
	st.bar_chart(edited_df.set_index("student")["score"])
else:
	st.warning("No rows after filtering")

# ------------------------------------------------------------
# 7) Form for controlled submission
# ------------------------------------------------------------
st.subheader("Feedback Form")
with st.form("feedback_form"):
	username = st.text_input("Your name", key="feedback_name")
	comment = st.text_area("Comment", key="feedback_comment")
	submitted = st.form_submit_button("Submit")

if submitted:
	st.session_state.submit_count += 1
	st.success(f"Thanks {username or 'anonymous'}! Submission recorded.")

st.info(f"Total submissions this session: {st.session_state.submit_count}")

# ------------------------------------------------------------
# 8) Simulated processing status/progress
# ------------------------------------------------------------
if st.button("Run Fake Pipeline", key="pipeline_button"):
	with st.status("Processing pipeline", expanded=True) as status:
		progress = st.progress(0)
		for i in range(1, 101):
			time.sleep(0.003)
			progress.progress(i)
		status.update(label="Pipeline finished", state="complete")
	st.toast("Pipeline done", icon="✅")

# ------------------------------------------------------------
# 9) Download edited data as CSV
# ------------------------------------------------------------
buffer = io.StringIO()
edited_df.to_csv(buffer, index=False)
st.download_button(
	"Download filtered CSV",
	data=buffer.getvalue(),
	file_name="filtered_students.csv",
	mime="text/csv",
	key="download_filtered_csv",
)
```

## 20) How To Run the Example App (Step-by-Step)

1. Create a file named `app.py` and paste the full example code from Section 19.
2. Open terminal in the same folder as `app.py`.
3. Install Streamlit if not installed:

```bash
pip install streamlit pandas
```

4. Run the app:

```bash
streamlit run app.py
```

5. Streamlit opens a local browser tab (usually `http://localhost:8501`).
6. Interact with widgets and observe reruns + state behavior.

## 21) Quick Revision Checklist (Before Exam)

1. Can you explain rerun behavior clearly?
2. Do you know when to use `session_state`?
3. Do you know difference between `st.dataframe`, `st.table`, `st.data_editor`?
4. Can you build a sidebar filter + KPI + chart layout quickly?
5. Can you use `st.form` to avoid immediate reruns on every input?
6. Can you explain `st.cache_data` vs `st.cache_resource`?
7. Can you run and debug a minimal app from terminal?

If you master these, you are well prepared for most Streamlit exam tasks.

## 22) Extended `st.` API Catalog (One-Line Revision Map)

Use this section as a rapid memory map. The sections above contain detailed examples.

Text and display:
- `st.title`: Page-level heading.
- `st.header`: Section heading.
- `st.subheader`: Subsection heading.
- `st.caption`: Small muted helper text.
- `st.text`: Plain fixed-width text.
- `st.markdown`: Markdown content renderer.
- `st.write`: Smart generic renderer for many Python types.
- `st.code`: Syntax-highlighted code block.
- `st.latex`: LaTeX formula rendering.
- `st.divider`: Horizontal visual separator.
- `st.badge`: Compact label/tag style marker.

Inputs and selection:
- `st.button`: Stateless click trigger.
- `st.download_button`: Trigger file download.
- `st.link_button`: Clickable URL button.
- `st.page_link`: Link to page/path in app.
- `st.checkbox`: Boolean input.
- `st.toggle`: Switch-style boolean input.
- `st.radio`: Single choice from options.
- `st.selectbox`: Dropdown single choice.
- `st.multiselect`: Multi-choice selection.
- `st.slider`: Numeric range/value slider.
- `st.select_slider`: Slider over ordered labels.
- `st.pills`: Pill-style single/multi selector.
- `st.segmented_control`: Segment selector UI.
- `st.text_input`: Single-line text.
- `st.text_area`: Multi-line text.
- `st.chat_input`: Chat prompt input.
- `st.number_input`: Numeric typed input.
- `st.date_input`: Date picker.
- `st.time_input`: Time picker.
- `st.file_uploader`: Upload files.
- `st.camera_input`: Capture camera image.
- `st.color_picker`: Color selector.

Data and metrics:
- `st.dataframe`: Interactive table.
- `st.table`: Static table.
- `st.data_editor`: Editable tabular UI.
- `st.metric`: KPI metric card.
- `st.json`: JSON pretty display.

Charts:
- `st.line_chart`: Quick line chart.
- `st.bar_chart`: Quick bar chart.
- `st.area_chart`: Quick area chart.
- `st.pyplot`: Matplotlib figure renderer.
- `st.altair_chart`: Altair chart renderer.
- `st.plotly_chart`: Plotly figure renderer.
- `st.vega_lite_chart`: Vega-Lite spec renderer.
- `st.map`: Plot lat/lon points on map.
- `st.scatter_chart`: Quick scatter chart.

Media:
- `st.image`: Display image(s).
- `st.audio`: Display audio player.
- `st.video`: Display video player.

Layout and structure:
- `st.sidebar`: Sidebar container.
- `st.columns`: Horizontal columns.
- `st.tabs`: Tabbed content panes.
- `st.expander`: Collapsible section.
- `st.container`: Group block container.
- `st.empty`: Replaceable placeholder.
- `st.popover`: Click-to-open floating panel.
- `st.dialog`: Modal-like dialog pattern.

Feedback and status:
- `st.success`: Success alert.
- `st.info`: Info alert.
- `st.warning`: Warning alert.
- `st.error`: Error alert.
- `st.exception`: Exception traceback block.
- `st.progress`: Progress bar.
- `st.spinner`: Spinner during context block.
- `st.status`: Multi-step status container.
- `st.toast`: Temporary toast notification.
- `st.balloons`: Celebration animation.
- `st.snow`: Snow animation.

Execution and navigation:
- `st.stop`: Halt execution now.
- `st.rerun`: Trigger immediate rerun.
- `st.switch_page`: Navigate to another page.
- `st.set_page_config`: Set page metadata/layout.

State and caching:
- `st.session_state`: Per-session key-value state store.
- `st.cache_data`: Cache function return data.
- `st.cache_resource`: Cache heavy reusable resources.

Chat:
- `st.chat_message`: Render user/assistant message blocks.

Advanced and embedding:
- `st.html`: Render controlled HTML.
- `st.components.v1.html`: Embed custom HTML/JS component.
- `st.components.v1.iframe`: Embed external page via iframe.

## 23) Last-Minute Practical Tips

1. Start every app with `st.set_page_config`.
2. Give widgets stable `key` values.
3. Use sidebar for filters, main area for outputs.
4. Cache data/model loading where possible.
5. Use forms for grouped inputs and deliberate submission.
6. Use `session_state` for counters, chat history, and user workflow state.
7. Show clear status during long tasks.

## 24) Exam Drill: 20 Likely Streamlit Practical Questions With Model Answers

Use this as a high-intensity revision set.
For each question:
- First, try solving on your own in 5 to 10 minutes.
- Then compare to the model answer.
- Finally, explain why rerun + session state behavior works the way it does.

### Q1) Create a title, subtitle, and explanatory text.

What examiners test:
- Basic page composition.
- Knowing difference between heading levels and generic text output.

Model answer:

```python
import streamlit as st

st.title("Student Performance Dashboard")
st.subheader("Module: DSA3101")
st.write("Use the controls to filter records and inspect trends.")
```

### Q2) Build a number input and compute a square in real time.

What examiners test:
- Widget return values.
- Immediate rerun update pattern.

Model answer:

```python
import streamlit as st

x = st.number_input("Enter a number", value=2.0, key="q2_x")
st.write("Square:", x * x)
```

### Q3) Show a button that increments a counter persistently.

What examiners test:
- `st.button` one-shot behavior.
- Correct `st.session_state` initialization.

Model answer:

```python
import streamlit as st

if "q3_count" not in st.session_state:
	st.session_state.q3_count = 0

if st.button("Increment", key="q3_increment"):
	st.session_state.q3_count += 1

st.write("Count:", st.session_state.q3_count)
```

### Q4) Use sidebar filters to subset a DataFrame.

What examiners test:
- Sidebar-driven filtering.
- `multiselect` and DataFrame boolean indexing.

Model answer:

```python
import pandas as pd
import streamlit as st

df = pd.DataFrame(
	{
		"dept": ["A", "A", "B", "C"],
		"score": [70, 85, 90, 60],
	}
)

selected = st.sidebar.multiselect(
	"Departments",
	options=sorted(df["dept"].unique()),
	default=sorted(df["dept"].unique()),
	key="q4_dept_filter",
)

filtered = df[df["dept"].isin(selected)]
st.dataframe(filtered)
```

### Q5) Upload a CSV and display first 5 rows.

What examiners test:
- `st.file_uploader` usage.
- Handling `None` before reading file.

Model answer:

```python
import pandas as pd
import streamlit as st

uploaded = st.file_uploader("Upload CSV", type=["csv"], key="q5_upload")

if uploaded is not None:
	df = pd.read_csv(uploaded)
	st.write("Preview:")
	st.dataframe(df.head())
else:
	st.info("Please upload a CSV file.")
```

### Q6) Create a form with name and age, and show output only on submit.

What examiners test:
- Form transaction semantics.
- Preventing immediate rerun-driven output updates.

Model answer:

```python
import streamlit as st

with st.form("q6_form"):
	name = st.text_input("Name", key="q6_name")
	age = st.number_input("Age", min_value=1, max_value=120, value=21, key="q6_age")
	submitted = st.form_submit_button("Submit")

if submitted:
	st.success(f"Saved user: {name}, age {age}")
```

### Q7) Display success/warning/error messages based on score.

What examiners test:
- Conditional feedback APIs.

Model answer:

```python
import streamlit as st

score = st.slider("Score", 0, 100, 50, key="q7_score")

if score >= 85:
	st.success("Excellent")
elif score >= 60:
	st.warning("Pass, but can improve")
else:
	st.error("Below passing threshold")
```

### Q8) Cache an expensive data-loading function.

What examiners test:
- `st.cache_data` semantics.

Model answer:

```python
import pandas as pd
import streamlit as st

@st.cache_data(ttl=300)
def load_data(path: str) -> pd.DataFrame:
	return pd.read_csv(path)

# Example call if path exists:
# df = load_data("data.csv")
# st.dataframe(df.head())
st.write("Use load_data(path) to avoid repeated expensive reads.")
```

### Q9) Use two columns: controls on left, chart on right.

What examiners test:
- `st.columns` layout composition.

Model answer:

```python
import pandas as pd
import streamlit as st

df = pd.DataFrame({"x": [1, 2, 3, 4], "y": [3, 5, 4, 6]}).set_index("x")

left, right = st.columns([1, 2])
with left:
	show_chart = st.checkbox("Show chart", value=True, key="q9_show_chart")
with right:
	if show_chart:
		st.line_chart(df)
```

### Q10) Add a download button for filtered CSV results.

What examiners test:
- Download pattern with in-memory buffer/string.

Model answer:

```python
import io
import pandas as pd
import streamlit as st

df = pd.DataFrame({"student": ["A", "B"], "score": [88, 93]})
min_score = st.slider("Min score", 0, 100, 80, key="q10_min_score")
filtered = df[df["score"] >= min_score]

buffer = io.StringIO()
filtered.to_csv(buffer, index=False)

st.download_button(
	"Download filtered CSV",
	data=buffer.getvalue(),
	file_name="filtered.csv",
	mime="text/csv",
	key="q10_download",
)
```

### Q11) Use `st.stop()` when required input is missing.

What examiners test:
- Early guard clauses in Streamlit apps.

Model answer:

```python
import streamlit as st

token = st.text_input("Access token", type="password", key="q11_token")
if not token:
	st.warning("Token required to continue")
	st.stop()

st.success("Token present. Continue workflow.")
```

### Q12) Use a callback to derive uppercase name from input.

What examiners test:
- `on_change` callback mechanics + session state updates.

Model answer:

```python
import streamlit as st

if "q12_upper" not in st.session_state:
	st.session_state.q12_upper = ""

def make_upper() -> None:
	st.session_state.q12_upper = st.session_state.q12_raw.upper()

st.text_input("Name", key="q12_raw", on_change=make_upper)
st.write("Uppercase:", st.session_state.q12_upper)
```

### Q13) Edit a table and compute updated average dynamically.

What examiners test:
- `st.data_editor` return value + downstream calculations.

Model answer:

```python
import pandas as pd
import streamlit as st

base = pd.DataFrame({"student": ["A", "B", "C"], "score": [80, 90, 85]})
edited = st.data_editor(base, key="q13_editor")

st.metric("Average Score", round(float(edited["score"].mean()), 2))
```

### Q14) Build tabs for overview and details.

What examiners test:
- Tabbed navigation in one page.

Model answer:

```python
import streamlit as st

overview, details = st.tabs(["Overview", "Details"])

with overview:
	st.write("High-level summary appears here.")

with details:
	st.write("Detailed diagnostics appear here.")
```

### Q15) Create an expander for optional debug information.

What examiners test:
- Progressive disclosure with `st.expander`.

Model answer:

```python
import streamlit as st

st.write("Main output visible by default.")
with st.expander("Show debug info"):
	st.json({"step": "preprocess", "rows": 1200, "null_ratio": 0.02})
```

### Q16) Show progress for a simulated pipeline.

What examiners test:
- User feedback during loops with `st.progress` and `st.spinner`.

Model answer:

```python
import time
import streamlit as st

if st.button("Run Pipeline", key="q16_run"):
	with st.spinner("Running..."):
		bar = st.progress(0)
		for i in range(1, 101):
			time.sleep(0.005)
			bar.progress(i)
	st.success("Pipeline completed")
```

### Q17) Build a very simple chat interface.

What examiners test:
- `st.chat_message` + `st.chat_input` + message history.

Model answer:

```python
import streamlit as st

if "q17_messages" not in st.session_state:
	st.session_state.q17_messages = []

for msg in st.session_state.q17_messages:
	with st.chat_message(msg["role"]):
		st.write(msg["content"])

prompt = st.chat_input("Say something", key="q17_prompt")
if prompt:
	st.session_state.q17_messages.append({"role": "user", "content": prompt})
	st.session_state.q17_messages.append({"role": "assistant", "content": f"Echo: {prompt}"})
	st.rerun()
```

### Q18) Show KPI metrics for count and max value.

What examiners test:
- `st.metric` usage and simple aggregation.

Model answer:

```python
import pandas as pd
import streamlit as st

df = pd.DataFrame({"value": [5, 9, 12, 7]})
st.metric("Count", len(df))
st.metric("Max", int(df["value"].max()))
```

### Q19) Create date and time inputs and print selected values.

What examiners test:
- Date/time widgets and Python datetime integration.

Model answer:

```python
import datetime as dt
import streamlit as st

picked_date = st.date_input("Date", value=dt.date.today(), key="q19_date")
picked_time = st.time_input("Time", value=dt.time(9, 0), key="q19_time")

st.write("Selected date:", picked_date)
st.write("Selected time:", picked_time)
```

### Q20) Build an all-in-one mini dashboard question.

Question prompt:
- Create a page with:
1. Sidebar slider for minimum score.
2. Editable table.
3. KPI for average score.
4. Bar chart by student.
5. CSV download.

What examiners test:
- End-to-end composition and state awareness.

Model answer:

```python
import io
import pandas as pd
import streamlit as st

st.title("Q20 Mini Dashboard")

df = pd.DataFrame(
	{
		"student": ["Ana", "Bo", "Cy", "Di"],
		"score": [72, 89, 95, 81],
	}
)

min_score = st.sidebar.slider("Minimum score", 0, 100, 70, key="q20_min_score")
filtered = df[df["score"] >= min_score]

edited = st.data_editor(filtered, key="q20_editor")

avg_score = round(float(edited["score"].mean()), 2) if len(edited) else 0.0
st.metric("Average Score", avg_score)

if len(edited):
	st.bar_chart(edited.set_index("student")["score"])
else:
	st.warning("No rows after filter")

buffer = io.StringIO()
edited.to_csv(buffer, index=False)
st.download_button(
	"Download CSV",
	data=buffer.getvalue(),
	file_name="q20_filtered.csv",
	mime="text/csv",
	key="q20_download",
)
```

## 25) How To Use This Drill Efficiently

1. Attempt Q1 to Q10 without notes.
2. Attempt Q11 to Q20 with a 45-minute timer.
3. For each wrong/slow question, classify issue type:
   - API memory issue
   - rerun/session-state issue
   - pandas logic issue
   - layout/composition issue
4. Rewrite only the weak questions from scratch the next day.

## 26) Ultra-Short Oral Answers (For Viva/Interview Style Exam)

1. Why does Streamlit rerun the script?
   - Because widgets are declarative; on interaction, Streamlit recomputes the page from top to bottom with updated widget/state values.

2. When to use `st.session_state`?
   - When values must persist across reruns in a user session, such as counters, wizard steps, or chat history.

3. `st.cache_data` vs `st.cache_resource`?
   - `cache_data` for function return data; `cache_resource` for heavy singleton-like objects (models, clients, engines).

4. Why use forms?
   - To collect multiple inputs and submit once, instead of rerunning logic on every single field change.

5. Most common bug in beginner Streamlit apps?
   - Forgetting rerun semantics and not initializing state keys safely.
