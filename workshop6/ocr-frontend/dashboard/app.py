import os
import time
from dash import (
    Dash,
    html,
    dcc,
    Input,
    Output,
    callback,
    callback_context,
    dash_table,
    State,
    no_update,
)
import dash
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
from dashboard.processing import preprocess, preprocess_v2, create_analytics_df
import dash_ag_grid as dag
import json
import datetime
import plotly.express as px
import base64
import io
from io import BytesIO
import plotly.graph_objects as go  


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    return html.Div(
        [
            html.H5(filename),
            html.H6(datetime.datetime.fromtimestamp(date)),
            dash_table.DataTable(
                df.to_dict("records"), [{"name": i, "id": i} for i in df.columns]
            ),
            html.Hr(),  # horizontal line
            # For debugging, display the raw contents provided by the web browser
            html.Div("Raw Content"),
            html.Pre(
                contents[0:200] + "...",
                style={"whiteSpace": "pre-wrap", "wordBreak": "break-all"},
            ),
        ]
    )

def analaytics():
    df = pd.read_csv('./dashboard/analytics_data.csv')
    # Combine locations
    df['Location'] = df['Location'].replace([' UTown Residences, North Tower', ' UTown Residences, South Tower'], 'UTown Residences')
    df['Location'] = df['Location'].replace([' Yale-NUS College - 28 College Ave West', ' Yale-NUS College - 12 College Ave West'], 'Yale-NUS College')
    # Now, when you aggregate data (for heatmap or bar graph), this new combined location will be treated as a single entity
    # For example, if aggregating for a heatmap:
    aggregated_df = df.groupby(['Latitude', 'Longitude', 'Location'])['Value'].sum().reset_index()

    # For the Latitude and Longitude of the combined location, you might want to use the average, or one of the two locations' coordinates
    # Here's how to use the average coordinates for the combined location
    average_coords = df[df['Location'] == 'Combined Location'][['Latitude', 'Longitude']].mean()
    df.loc[df['Location'] == 'Combined Location', ['Latitude', 'Longitude']] = average_coords.values

    df['Date'] = pd.to_datetime(df['Month'] + ' ' + df['Year'].astype(str), format='%B %Y')
    return df
def create_dash_app(server, df):

    df = preprocess(df)

    #analytics df
    new_df = analaytics()

    #colour code
    dark_scale  = [
    (0.00, '#000080'),  # Navy blue for the lowest values
    (0.25, '#0000FF'),  # Blue
    (0.50, '#800080'),  # Purple
    (0.75, '#C71585'),  # Medium violet red
    (1.00, '#FFC0CB')   # Light pink for the highest values
]
    # Generate a list of unique dates for the range slider
    unique_dates = new_df['Date'].dt.date.unique()
    date_marks = {i: date.strftime('%b %Y') for i, date in enumerate(unique_dates, start=1)}

    # Generate a list of waste types for the dropdown
    waste_types = new_df['Waste Type'].unique()
    
    # Define the initial map to display
    initial_fig = px.density_mapbox(new_df, lat="Latitude", lon="Longitude", z="Value",
                            hover_name="Location", 
                            radius=50,  # Increased radius for larger heatboxes
                            center=dict(lat=1.3066096663336357, lon=103.77257778077148), zoom=15.5,
                            mapbox_style="carto-positron",
                            color_continuous_scale=dark_scale,  # Example color scale
                            range_color=[0, max(new_df['Value'])]
                            )
    date_marks = {
        1: unique_dates[0].strftime('%b %Y'),       # Start date label
        len(unique_dates): unique_dates[-1].strftime('%b %Y')  # End date label
    }



    analaytics_settings = dbc.Card(
    [
        dbc.CardHeader("Filter Options"),
        dbc.CardBody([
            html.H5("Type of Waste", className="card-title"),
            dcc.Checklist(
                id='waste-type-checkbox',
                options=[{'label': i, 'value': i} for i in waste_types],
                value=[waste_types[0]],  # Default checked value(s)
                inline=True  # Arrange checkboxes inline
            ),
            html.H5("Date Range", className="card-title"),
                dcc.RangeSlider(
            id='date-slider',
            min=1,
            max=len(unique_dates),
            value=[1, len(unique_dates)],
            marks=date_marks,
            step=1
        ),
        html.Div(id='date-range-text', style={'margin-top': '20px', 'fontSize': 16})
        
        ,
        ]),
    ],
    id="analytics",
    style={"display": "none", "backgroundColor": "#FFF9C4"},  # Adjust the width of the sidebar
)

   

    app = Dash(
        server=server,
        use_pages=True,
        pages_folder="",
        url_base_pathname="/dashboard/",
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            dbc.themes.FLATLY,
            dbc.icons.FONT_AWESOME,
        ],
        prevent_initial_callbacks="initial_duplicate",
        suppress_callback_exceptions=True,
    )

    getRowStyle = {
        "styleConditions": [
            {
                "condition": "params.data.is_abnormal",
                "style": {"backgroundColor": ""},
            },
        ],
        "defaultStyle": {"color": "black"},
    }
    columns = [
        {"headerName": "Row ID", "valueGetter": {"function": "params.node.id"},"hide": True},
        {
            "field": "binCenterName",
            "checkboxSelection": True,
            "headerCheckboxSelection": True,
            "headerName": "Bin Center",
            "filter": "agTextColumnFilter",
        },
        {
            "field": "Date",
            "filter": "agDateColumnFilter",
            "valueGetter": {
                "function": "d3.timeParse('%d/%m/%Y')(params.data.Date)"
            },
            "valueFormatter": {
                "function": "params.data.Date"
            },
            "filterParams": {
                "browserDatePicker": True,
                "minValidYear": 2023,
                "maxValidYear": 2024,
            },
        },
        {
            "field": "Time",
            "filter": "agTextColumnFilter",
            "hide": True,
        },
        {
            "field": "extractedWeight",
            "headerName": "Extracted (KG)",
            "filter": "agNumberColumnFilter",
            "cellStyle": {
                "styleConditions": [
                    {
                        "condition": "params.data.is_error === true && params.data.manualWeight == null",
                        "style": {"backgroundColor": "#FFBF00"},
                    },
                    {
                        "condition": "params.data.is_error === true  && params.data.manualWeight != null ",
                        "style": {"backgroundColor": "lightcoral"},
                    },
                ]
            },
        },
        {
            "field": "referenceWeight",
            "headerName": "Reference (KG)",
            "hide": True,
            "filter": "agNumberColumnFilter",
        },
        {
            "field": "manualWeight",
            "headerName": "Manual  (KG)",
            "hide": True,
            "filter": "agNumberColumnFilter",
        },
        {"field": "is_abnormal", "hide": True},
        {"field": "is_error", "hide": True},
        {
            "field": "rfidWeight",
            "headerName": "RFID (KG)",
            "filter": "agNumberColumnFilter",
        },
        {
            "field": "recordedWeight",
            "headerName": "Acutal (KG)",
            "filter": "agNumberColumnFilter",
            "cellStyle": {
                "styleConditions": [
                    {
                        "condition": "params.data.manualWeight != null ",
                        "style": {"backgroundColor": "mediumaquamarine"},
                    },
                    {
                        "condition": "params.data.recordedWeight < 0 ",
                        "style": {"backgroundColor": "lightcoral"},
                    },
                    {
                        "condition": "params.data.recordedWeight === 0 ",
                        "style": {"backgroundColor": "#FFBF00"},
                    }
                ]
            },
        },
        {
            "field": "discrepancy_reason",
            "headerName": "Discrepancy",
            "filter": "agTextColumnFilter",
            "cellStyle": {
                "styleConditions": [
                    {
                        "condition": "params.data.discrepancy_reason != null ",
                        "style": {"backgroundColor": "lightcoral"},
                    }
                ]
            },
        },
        {
            "field": "Image",
            "headerName": "Image",
            "cellRenderer": "DBC_Button_Simple",
            "cellRendererParams": {"color": "primary"},
            "textAlign": "center",
        },
    ]

    defaultColDef = {
        "flex": 2,
        "minWidth": 150,
        "filter": True,
        "floatingFilter": True,
        "sortable": True,
    }

    legend = html.Div(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("TABLE LEGEND", className="card-title"),
                        html.Div(dbc.Badge("Error", color="danger"), className="mb-2"),
                        html.Div(
                            dbc.Badge("Potential Error", color="warning"),
                            className="mb-2",
                        ),
                        html.Div(
                            dbc.Badge("Error Corrected", color="success"),
                            className="mb-2",
                        ),
                    ]
                ),
                id="legend",
                style={"display": "none", "backgroundColor": "#FFF9C4"},
            )
        ]
    )




    dashboard_layout = html.Div(
        [
            # Main content
            html.Div(
                [
                    # Header
                    html.Div(
                        html.H1(
                            "OCR Extraction Report",
                            style={
                                "textAlign": "center",  # Align left
                                "color": "white",
                                "fontFamily": "Poppins",
                                "font-weight": "bold",
                                "font-size": "1.5em",  # Reduced font size
                                "margin": "0",
                                "padding": "20px",
                            },
                        ),
                        style={
                            "background": "linear-gradient(to right, #003300 40%, #FFA500)",  # Example gradient color
                            "border": "1px solid #ccc",  # border for emphasis
                            "border-radius": "5px",  # rounded corners
                            "text-align": "center",  # center the box
                            "width": "100%",  # example width
                            "margin": "auto",  # center horizontally
                        },
                    ),
                    html.Div(
                        [
                            dcc.Dropdown(
                                id="column-filter",
                                options=[
                                    {"label": "Date", "value": "Date"},
                                    {"label": "Time", "value": "Time"},
                                    {
                                        "label": "Extracted Weight",
                                        "value": "extractedWeight",
                                    },
                                    {
                                        "label": "Reference Weight",
                                        "value": "referenceWeight",
                                    },
                                    {"label": "Manual Weight", "value": "manualWeight"},
                                    {"label": "RFID Weight", "value": "rfidWeight"},
                                    {
                                        "label": "Recorded Weight",
                                        "value": "recordedWeight",
                                    },
                                    {
                                        "label": "Discrepancy Reason",
                                        "value": "discrepancy_reason",
                                    },
                                ],
                                value=[
                                    "binCenterName",
                                    "Date",
                                    "extractedWeight",
                                    "rfidWeight",
                                    "recordedWeight",
                                    "discrepancy_reason",
                                    "Image",
                                ],  # default value: all columns
                                multi=True,  # allow multiple values to be selected
                            ),  # Data Table
                            
                            dag.AgGrid(
                                id="datatable-interactivity",
                                columnDefs=columns,
                                rowData=df.to_dict("records"),
                                dashGridOptions={
                                    "rowSelection": "multiple",
                                    "pagination": True,
                                    "paginationAutoPageSize": False,
                                    "paginationPageSize": 5,

                                },
                                defaultColDef=defaultColDef,
                                getRowStyle=getRowStyle,
                                csvExportParams={
                                    "fileName": "ag_grid_test.csv",
                                },
                            ),
                            dbc.Button(
                                "Download CSV",
                                color="primary",
                                className="me-2",
                                id="csv-button",
                                n_clicks=0,
                                style={
                                    "float": "right",
                                    "marginTop": "20px",
                                    "padding": "10px",
                                },
                            ),
                        ],
                        style={"padding": "50px"},
                    ),
                    # analytics
                    html.Div([
                        dcc.Tabs(
                            id='tabs',
                            value='tab-rfid',
                            children=[
                                dcc.Tab(label='RFID', value='tab-rfid'),
                                dcc.Tab(label='OCR', value='tab-ocr'),
                            ],
                            style={
                                'marginLeft': '0',  # Align tabs to the left side of their container
                                'width': '50%',     # The tabs component will take the full width of its container
                                "padding": "50px"
                            }
                        ),
                        html.Div(id='tabs-content', style={'padding': '20px'})  # Adds padding around the content
                    ], style={'textAlign': 'center'}) ,
                    # Modal
                    html.Div(
                        [
                            dbc.Modal(
                                id="modal",
                                children=[
                                    dbc.ModalHeader("Image"),
                                    dbc.ModalBody(
                                        html.Div(
                                            [
                                                html.Img(
                                                    id="modal-image",
                                                    style={"width": "100%"},
                                                ),
                                                html.Div(id="modal-extracted-weight"),
                                                dcc.Input(
                                                    id="modal-manual-weight",
                                                    type="number",
                                                    placeholder="Enter manual weight",
                                                ),
                                            ]
                                        ),
                                    ),
                                    dbc.ModalFooter(
                                        [
                                            
                                            dbc.Button(
                                                "Submit",
                                                id="submit-button",
                                                className="btn-primary",
                                            ),
                                        ]
                                    ),
                                ],
                            ),
                        ]
                    ),
                    html.Div(id="dd-output-container"),
                    html.Div(id="dbc-btn-simple-value-changed"),
                    # download
                ],
                className="main",
                style={
                    "height": "100%",
                    "width": "100%",
                    "position": "relative",
                    "left": "0",
                    "top": "0",
                    "backgroundColor": "white",
                },
            ),
        ],
    )

    analytics_layout = html.Div(
        [
            # Main content
            html.Div(
                [
                    html.Div(
                        html.H1(
                            "Analytics",
                            style={
                                "textAlign": "center",
                                "color": "white",
                                "fontFamily": "Poppins",
                                "font-weight": "bold",
                                "font-size": "1.5em",  # Reduced font size
                                "margin": "0",
                                "padding": "20px",
                            },
                        ),
                        style={
                            "background": "linear-gradient(to right, #003300 40%, #FFA500)",  # Example gradient color
                            "border": "1px solid #ccc",  # border for emphasis
                            "border-radius": "5px",  # rounded corners
                            "text-align": "center",  # center the box
                            "width": "100%",  # example width
                            "margin": "auto",  # center horizontally
                        },
                    ),
                    # Map Component
                    dcc.Graph(id='waste-heatmap', figure=initial_fig),

                    # Bar Graph Component
                    dcc.Graph(id='waste-bar-graph')

                ]
            )
        ]
    )

    upload_layout = html.Div(
        [
            # Main content
            html.Div(
                [
                    html.Div(
                        html.H1(
                            "Upload CSV File to Clean or Transform",
                            style={
                                "textAlign": "center",
                                "color": "white",
                                "fontFamily": "Poppins",
                                "font-weight": "bold",
                                "font-size": "1.5em",  # Reduced font size
                                "margin": "0",
                                "padding": "20px",
                            },
                        ),
                        style={
                            "background": "linear-gradient(to right, #003300 40%, #FFA500)",  # Example gradient color
                            "border": "1px solid #ccc",  # border for emphasis
                            "border-radius": "5px",  # rounded corners
                            "text-align": "center",  # center the box
                            "width": "100%",  # example width
                            "margin": "auto",  # center horizontally
                        },
                    ),
                    html.Br(),
                    dcc.Upload(
                        id="upload-data",
                        children=html.Div(
                            [
                                "Drag and Drop or ",
                                html.A(
                                    "Select Files",
                                    style={
                                        "color": "#49B265",
                                        "textDecoration": "underline",
                                    },
                                ),
                                html.Br(),
                                html.I(
                                    className="fa fa-upload",
                                    style={"font-size": "24px", "margin-top": "10px"},
                                ),
                            ]
                        ),
                        style={
                            "width": "100%",
                            "height": "200px",
                            "borderWidth": "2px",
                            "font-size": "34px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            "padding": "50px",
                            "fontFamily": "Poppins",
                        },
                        # Allow multiple files to be uploaded
                        multiple=True,
                    ),
                    html.Br(),
                    html.Br(),
                    dcc.Store(id="store"),
                    html.Div(id="output-data-upload"),
                ],
                style={"width": "100%", "margin": "auto"},
            ),
            dbc.Button(
                [
                    html.I(className="fa fa-download me-2"),
                    "Download CSV",
                ],
                color="primary",
                className="me-2",
                id="csv-button-transform",
                n_clicks=0,
                style={"float": "right", "marginTop": "20px", "padding": "10px"},
            ),
            dcc.Download(id="download-csv"),
        ]
    )

    dash.register_page("dashboard", layout=dashboard_layout)
    dash.register_page("analytics", layout=analytics_layout)
    dash.register_page("upload", layout=upload_layout)

    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#e9e9e9",
    }

    # the styles for the main content position it to the right of the sidebar and
    # add some padding.
    CONTENT_STYLE = {
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    }

    sidebar = html.Div(
        [
            html.Div(
                [
                    html.I(
                        className="fas fa-trash-alt",
                        style={
                            "font-size": "35px",
                            "display": "inline-block",
                            "color": "green",
                            "position": "relative",
                        },
                    ),  # Font Awesome waste icon
                    html.H2(
                        "OCR", className="display-4", style={"display": "inline-block"}
                    ),
                ],
                style={
                    "display": "flex",
                    "align-items": "center",
                    "justify-content": "center",
                    "height": "100px",
                },
            ),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink(
                        "Home", href="/dashboard/", active="exact", style={"color": "#49B265"}
                    ),
                    dbc.NavLink(
                        "Analytics",
                        href="/dashboard/analytics",
                        active="exact",
                        style={"color": "#49B265"},
                    ),
                    dbc.NavLink(
                        "Upload",
                        href="/dashboard/upload",
                        active="exact",
                        style={"color": "#49B265"},
                    ),
                ],
                vertical=True,
                pills=True,
            ),
            legend,
            analaytics_settings,
        ],
        style=SIDEBAR_STYLE,
    )

    content = html.Div(id="page-content", style=CONTENT_STYLE)

    app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

    # For upload file and returning processed file
    @app.callback(Output('store', 'data'),
                    Input('upload-data', 'contents'),
                    State('upload-data', 'filename'),
                    State('upload-data', 'last_modified'),
                    prevent_initial_call=True)
    def update_output(contents, list_of_names, list_of_dates):
        if [contents, list_of_names, list_of_dates] == [None, None, None]:
            return dash.no_update

        content_type, content_string = contents[0].split(',')

        decoded = base64.b64decode(content_string)

        df = pd.read_excel(io.BytesIO(decoded), header=None)
        json_data = df.to_json(date_format='iso', orient='records', lines=True)
        folder_name = 'static'
        file_name = 'df.json'
        file_path = os.path.join(folder_name, file_name)

        with open(file_path, 'w') as f:
            f.write(json_data)

        df_cleaned_path = os.path.join("static", "df_cleaned.json")

        while not os.path.exists(df_cleaned_path):
            print(f"File {df_cleaned_path} not found. Waiting...")
            time.sleep(5)  # Wait for 5 seconds before checking again.

        # If the loop exits, it means the file exists.
        with open(df_cleaned_path, 'r') as f:
            json_data = f.read()
        
        last_comma_index = json_data.rfind(',')
        if last_comma_index != -1:
            json_data = json_data[:last_comma_index] + json_data[last_comma_index + 1:]
        cleaned_json_data = json_data
        df_read = pd.read_json(cleaned_json_data)
        return df_read.to_json(orient='split')  #I have to convert to json format to store in dcc.Store


    # Goal here is to then extract dataframe from dcc.store by reading json and output a table

    @app.callback(
        Output("output-data-upload", "children"),
        Input("store", "data"),
        prevent_initial_call=True,
    )
    def output_from_store(stored_data):
        print(stored_data)

        df = pd.read_json(stored_data, orient="split")
        print(df)

        return html.Div(
            [
                html.H2("Cleaned File", style={"display": "inline-block"}),
                html.Br(),
                html.Div(
                    [
                        dash_table.DataTable(
                            data=df.to_dict("records"),
                            columns=[{"name": i, "id": i} for i in df.columns],
                        ),
                        html.Hr(),  # horizontal line
                    ]
                ),
            ]
        )

    @app.callback(
        Output("download-csv", "data"),
        Input("csv-button-transform", "n_clicks"),
        Input("store", "data"),
        prevent_initial_call=True,
    )
    def download_csv(n_clicks, stored_data):
        # Get the stored data
        if n_clicks > 0:
            df = pd.read_json(stored_data, orient="split")

            return dcc.send_data_frame(df.to_csv, filename="cleaned_file.csv")

    @app.callback(
        Output("datatable-interactivity", "exportDataAsCsv"),
        Output("datatable-interactivity", "csvExportParams"),
        Input("csv-button", "n_clicks"),
    )
    def export_data_as_csv(n_clicks):
        if n_clicks:
            return True, {"onlySelected": True}
        return False, {}

    @app.callback(
        [
            Output("modal", "is_open"),
            Output("modal-image", "src"),
            Output("modal-manual-weight", "value"),
            Output("datatable-interactivity", "rowData"),
            
        ],
        [
            Input("datatable-interactivity", "cellRendererData"),
            Input("submit-button", "n_clicks"),
        ],
        [
            State("modal-manual-weight", "value"),
            State("datatable-interactivity", "rowData"),
        ],
    )
    def update_modal_and_table(
        cell_renderer_data, n_clicks, manual_weight, current_row_data
    ):
        ctx = callback_context  # Get the callback context to determine what triggered the callback
        if (
            not ctx.triggered
        ):  # This case occurs at initialization when neither input has triggered the callback yet
            return (
                no_update,
                no_update,
                no_update,
                no_update,
            )  # Return no_update to leave the Outputs unchanged
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[
            0
        ]  # Get the ID of the component that triggered the callback

        # Convert current_row_data back to a DataFrame for easier manipulation
        df = pd.DataFrame(current_row_data)

        if (
            trigger_id == "submit-button" and cell_renderer_data is not None
        ):  # Check if the submit button was clicked
            row_index = int(cell_renderer_data.get("rowId"))
            if row_index is not None:
                df.loc[row_index, "manualWeight"] = manual_weight
                new_data = df.copy()
                test = preprocess_v2(new_data)
                return (
                    False,
                    None,
                    None,
                    test.to_dict("records"),
                )  # Close the modal, clear image and manual weight fields, and update table data

        elif (
            trigger_id == "datatable-interactivity" and cell_renderer_data is not None
        ):  # Check if the datatable triggered the callback
            row_index = int(cell_renderer_data.get("rowId"))
            
            if row_index is not None:
                image_url = df.loc[row_index, "image"]
                manual_weight = df.loc[
                    row_index, "manualWeight"
                ]  # Assuming your column name is 'manualWeight'
                return (
                    True,
                    "../"+image_url,
                    manual_weight,
                    no_update,
                )  # Open the modal, set image URL and manual weight fields, and leave table data unchanged

        return (
            no_update,
            no_update,
            no_update,
            no_update,
        )  # Return no_update to leave the Outputs unchanged if none of the above conditions are met

    @app.callback(
        Output("datatable-interactivity", "columnState"),
        Input("column-filter", "value"),
        State("datatable-interactivity", "columnState"),
        prevent_initial_call=True,
    )
    def update_columns_and_data(selected_columns, currcols):

        for curr in currcols:
            if curr["colId"] not in selected_columns:
                curr["hide"] = True
            else:
                curr["hide"] = False
            if curr["colId"] == "binCenterName" or curr["colId"] == "Image":
                curr["hide"] = False

        return currcols

    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == "/dashboard/":
            return dashboard_layout
        elif pathname == "/dashboard/analytics":
            return analytics_layout
        elif pathname == "/dashboard/upload":
            return upload_layout

    @app.callback([Output("legend", "style"),
                   Output("analytics","style")], [Input("url", "pathname")])
    def toggle_legend(pathname):
        if pathname == "/dashboard/":  # If we are on the home page
            return {"display": "block"},{"display": "none"}  # Show the legend
        elif pathname == "/dashboard/analytics":
            return {"display": "none"},{"display": "block"}
        else:
            return {"display": "none"},{"display": "none"}
    
    @app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value'), Input('datatable-interactivity', 'rowData')]
)
    def update_graphs(tab, row_data):
        # Convert the current row data into a DataFrame
        current_df = pd.DataFrame(row_data)
        
        

        
        error_count_by_date,error_count_by_bin,rfid_issues_by_date,rfid_issues_by_bin= create_analytics_df(current_df)
        # graphs
        # Create the Plotly figures here (this should be done outside of the callback or in a separate callback)
        rfid_issues_by_date_fig = px.bar(
            rfid_issues_by_date,
            x='Date',
            y=rfid_issues_by_date.columns[1:],  # Exclude the Date column for y values
            title='RFID Errors Over Time',
            labels={'value': 'Count of Errors', 'variable': 'Type of RFID Error'},
            barmode='stack'
        )

        rfid_issues_by_date_fig.update_layout(xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                    
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            ))

        rfid_issues_by_bin_fig = px.bar(
            rfid_issues_by_bin,
            x='binCenterName',
            y=rfid_issues_by_bin.columns[1:],  # Exclude the binCenterName column for y values
            title='RFID Errors by Bin Center',
            labels={'value': 'Count of Errors', 'variable': 'Type of RFID Error'},
            barmode='stack'
        )

        rfid_issues_by_bin_fig.update_layout(
        xaxis_title='Bin Center Name',
        yaxis_title='Count of Errors'
        )

        # For OCR performance figures, you need to ensure the figures are created based on error_count_by_date and error_count_by_bin DataFrames
        # Assume error_count_by_date is a DataFrame with 'Date', 'OCR Error', and 'Potential Error' columns
        ocr_performance_by_date_fig = px.area(
            error_count_by_date,
            x='Date',
            y=[ 'Potential Error','OCR Error'],  # Replace with actual column names if different
            title='OCR Performance Errors Over Time'
        )

        # Update the layout for axis titles and add the range slider
        ocr_performance_by_date_fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Percentage of Errors',
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                    
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            )
        )

        ocr_performance_by_bin_fig = px.bar(
            error_count_by_bin,
            x='binCenterName',
            y=[ 'Potential Error','OCR Error'],  # Replace with actual column names if different
            title='OCR Performance Errors by Bin Center',
            barmode='stack'
        )

        ocr_performance_by_bin_fig.update_layout(
        xaxis_title='Bin Center Name',
        yaxis_title='Counts of Errors'
        )   

        figures = [rfid_issues_by_date_fig, rfid_issues_by_bin_fig, ocr_performance_by_date_fig, ocr_performance_by_bin_fig]

        for fig in figures:
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=40, b=30)  # Adjust margins if needed
            )
        

        # Then, depending on the active tab, return the appropriate figures
        if tab == 'tab-rfid':
            return html.Div(
                style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'},
                children=[
                    html.Div(style={'flex': '1', 'minWidth': '50%'}, children=[dcc.Graph(figure=rfid_issues_by_date_fig)]),
                    html.Div(style={'flex': '1', 'minWidth': '50%'}, children=[dcc.Graph(figure=rfid_issues_by_bin_fig)])
                ]
            )
        elif tab == 'tab-ocr':
            return html.Div(
                style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'},
                children=[
                    html.Div(style={'flex': '1', 'minWidth': '50%'}, children=[dcc.Graph(figure=ocr_performance_by_date_fig)]),
                    html.Div(style={'flex': '1', 'minWidth': '50%'}, children=[dcc.Graph(figure=ocr_performance_by_bin_fig)])
                ]
            )
    # Callback to update map based on selected date range and waste types
    @app.callback(
        [Output('waste-heatmap', 'figure'), Output('waste-bar-graph', 'figure')],
        [Input('date-slider', 'value'), Input('waste-type-checkbox', 'value')]
    )
    def update_output(slider_values, selected_waste_types):
        # Convert slider values to dates
        start_date, end_date = unique_dates[slider_values[0] - 1], unique_dates[slider_values[1] - 1]

        # Filter the DataFrame based on the selected date range and waste types
        filtered_df = new_df[(pd.to_datetime(new_df['Date']).dt.date >= start_date) &
                        (pd.to_datetime(new_df['Date']).dt.date <= end_date) &
                        (new_df['Waste Type'].isin(selected_waste_types))]

        # Aggregate the data for heatmap
        aggregated_df_heatmap = filtered_df.groupby(['Latitude', 'Longitude', 'Location'])['Value'].sum().reset_index()

        # Create the updated figure for the heatmap
        fig_heatmap = px.density_mapbox(aggregated_df_heatmap, lat="Latitude", lon="Longitude", z="Value",
                                        hover_name="Location", 
                                        radius=50, 
                                        center=dict(lat=1.3066096663336357, lon=103.77257778077148), zoom=15.5,
                                        mapbox_style="carto-positron",
                                        color_continuous_scale=dark_scale,
                                        range_color=[0, max(aggregated_df_heatmap['Value'])]
                                        )
                                        
        # Overlay with a scatter plot for location labels
        fig_heatmap.add_trace(
            go.Scattermapbox(
                lat=aggregated_df_heatmap['Latitude'],
                lon=aggregated_df_heatmap['Longitude'],
                mode='markers+text',
                marker=go.scattermapbox.Marker(size=9),
                text=aggregated_df_heatmap['Location'],  # Assuming 'Location' is the column with location names
                textposition='top right'
            )
        )
        # Aggregate the data for bar graph
        aggregated_df_bar = filtered_df.groupby(['Location', 'Waste Type'])['Value'].sum().reset_index()

        # Create the updated figure for the bar graph (stacked)
        fig_bar = px.bar(aggregated_df_bar, x='Location', y='Value', color='Waste Type', barmode='stack')

        return fig_heatmap, fig_bar
    
    @app.callback(
    Output('date-range-text', 'children'),
    [Input('date-slider', 'value')]
)
    def update_date_range_text(slider_value):
        # Assuming slider_value is a list of two elements: [start_index, end_index]
        if slider_value:
            start_date = unique_dates[slider_value[0] - 1].strftime('%b %Y')
            end_date = unique_dates[slider_value[1] - 1].strftime('%b %Y')
            return f"Selected Date Range: {start_date} to {end_date}"
        return "Select a date range"

        
   

    return app
