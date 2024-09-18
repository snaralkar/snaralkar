import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import warnings
# Suppress warnings
warnings.filterwarnings('ignore')

# Load and prepare prod data
def load_and_prepare_prod_data(file_path, sheet_name):
    data = pd.read_excel(file_path, sheet_name=sheet_name)
    data.columns = data.columns.str.replace(" ", "_").str.lower()
    data['dt_ids'] = pd.to_numeric(data['dt_ids'], errors='coerce').astype('Int64')
    data["date_of_down"] = pd.to_datetime(data["date_of_down"], errors='coerce')
    data["month_name"] = data["date_of_down"].dt.month_name()
    data['year'] = data["date_of_down"].dt.year
    return data

# Load and prepare adr data
def load_and_prepare_adr_data(file_path, sheet_name):
    adr_data = pd.read_excel(file_path, sheet_name=sheet_name)
    adr_data.columns = adr_data.columns.str.replace(" ", "_").str.lower()
    adr_data['total_zips_transferred'] = pd.to_numeric(adr_data['total_zips_transferred'], errors='coerce').astype('Int64')
    adr_data["date_of_transfer"] = pd.to_datetime(adr_data["date_of_transfer"], errors='coerce')
    adr_data["month_name"] = adr_data["date_of_transfer"].dt.month_name()
    adr_data['year'] = adr_data["date_of_transfer"].dt.year
    adr_data['date'] = adr_data['date_of_transfer'].dt.date
    return adr_data

# Load and prepare labelimg data
def load_and_prepare_labelimg_data(file_path, sheet_name):
    limg_data = pd.read_excel(file_path, sheet_name=sheet_name)
    limg_data.columns = limg_data.columns.str.replace(" ", "_").str.lower()
    limg_data['total_uploaded'] = pd.to_numeric(limg_data['total_uploaded'], errors='coerce').astype('Int64')
    limg_data["uploaded_date"] = pd.to_datetime(limg_data["uploaded_date"], errors='coerce')
    limg_data["month_name"] = limg_data["uploaded_date"].dt.month_name()
    limg_data['year'] = limg_data["uploaded_date"].dt.year
    return limg_data

# Load and prepare aiq data
def load_and_prepare_aiq_data(file_path, sheet_name):
    aiq_data = pd.read_excel(file_path, sheet_name=sheet_name)
    aiq_data.columns = aiq_data.columns.str.replace(" ", "_").str.lower()
    aiq_data['total_uploaded'] = pd.to_numeric(aiq_data['total_uploaded'], errors='coerce').astype('Int64')
    aiq_data["uploaded_date"] = pd.to_datetime(aiq_data["uploaded_date"], errors='coerce')
    aiq_data["month_name"] = aiq_data["uploaded_date"].dt.month_name()
    aiq_data['year'] = aiq_data["uploaded_date"].dt.year
    return aiq_data



# Load initial data for 'Prod_Download'&'ADR_Transfer'&'LabelIMG_Uploading'&AIQ_Uploading
file_path = "New_Final_Dashboard_Sheet_DB.xlsx"
prod_data = load_and_prepare_prod_data(file_path, sheet_name='Prod_Download')
adr_data = load_and_prepare_adr_data(file_path, sheet_name='ADR_Transfer')
labelimg_data = load_and_prepare_labelimg_data(file_path, sheet_name = 'LabelImg_Uploading')
aiq_data = load_and_prepare_aiq_data(file_path, sheet_name = 'AIQ_Uploading')

# Extract the most recent dates from all four columns across sheets
latest_date_of_down = pd.to_datetime(prod_data['date_of_down']).max()
latest_date_of_transfer = pd.to_datetime(adr_data['date_of_transfer']).max()
latest_uploaded_date_1 = pd.to_datetime(labelimg_data['uploaded_date']).max()
latest_uploaded_date_2 = pd.to_datetime(aiq_data['uploaded_date']).max() 

# Get the most recent date overall
latest_date = max(latest_date_of_down, latest_date_of_transfer, latest_uploaded_date_1, latest_uploaded_date_2)

# Format as "Month-Year"
last_updated = latest_date.strftime("%b-%Y")

# Create a Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('Data Bank Dashboard', style={
        'textAlign': 'center',
        'color': '#87CEEB'  # Sky blue color
    }),

    # Refresh button with image
    html.Button(
        html.Img(src='/assests/refresh-button.png', style={
            'width': '50px',
            'height': '50px',
            'cursor': 'pointer'
        }),
        id='refresh-button',
        n_clicks=0,
        style={
            'border': 'none',
            'background-color': 'transparent',
            'position': 'absolute',
            'top': '10px',
            'right': '20px',
        }
    ),

    #Last Updated
    html.Div([
        html.H6(f"Last Updated: {last_updated}", style={
            'position': 'absolute', 
            'top': '10px', 
            'left': '20px', 
            'padding': '10px 20px', 
            'background-color': '#87CEEB',
            'border': 'none',
            'border-radius': '5px',
            'color': 'white',
            'font-size': '16px',
            'cursor': 'pointer',
            'box-shadow': '0px 2px 8px rgba(0, 0, 0, 0.1)',
        })
    ]),

    # Navigation buttons
    html.Div([
        html.Button('Prod Data', id='prod-data-button', n_clicks=0, 
                    style={'margin': '15px', 
                        'padding': '10px 20px', 
                        'background-color': '#87CEEB', 
                        'color': 'white',
                        'border': 'none',
                        'border-radius': '5px', 
                        'cursor': 'pointer',
                        'font-size': '16px'
                    }),
        html.Button('ADR', id='adr-button', n_clicks=0, 
                    style={'margin': '15px', 
                        'padding': '10px 20px', 
                        'background-color': '#87CEEB', 
                        'color': 'white',
                        'border': 'none',
                        'border-radius': '5px', 
                        'cursor': 'pointer',
                        'font-size': '16px'
                    }),
        html.Button('ADE-LabelIMG', id='ade-labelimg-button', n_clicks=0, 
                    style={
                        'margin': '15px', 
                        'padding': '10px 20px', 
                        'background-color': '#87CEEB', 
                        'color': 'white',
                        'border': 'none',
                        'border-radius': '5px', 
                        'cursor': 'pointer',
                        'font-size': '16px'
                    }),
        html.Button('ADE-AIQ', id='ade-aiq-button', n_clicks=0, 
                    style={
                        'margin': '15px', 
                        'padding': '10px 20px', 
                        'background-color': '#87CEEB', 
                        'color': 'white',
                        'border': 'none',
                        'border-radius': '5px', 
                        'cursor': 'pointer',
                        'font-size': '16px'
                    }),
    ], style={'textAlign': 'center', 'margin-bottom': '20px','gap': '20px'}),

        #---------------------------------------------------------------------------Main 4 Content---------------------------------------------------------------------------

    html.Div(id='main-content', children=[
        #---------------------------------------------------------------------------Prod Content---------------------------------------------------------------------------

        html.Div(id='prod-content', children=[
            # Filters in one row with enhanced style
            html.Div([
                # Year Dropdown
                dcc.Dropdown(
                    id='year-dropdown-1',
                    multi=True,
                    options=[{'label': year, 'value': year} for year in prod_data['year'].unique()],
                    placeholder='Select Years',
                    style={
                        'width': '100%', 
                        'padding': '5px 10px', 
                        'border': '1px solid #d1d1d1', 
                        'border-radius': '8px',
                        'background-color': '#ffffff',
                        'font-size': '16px',
                        'color': '#333',
                        'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.1)',
                        'transition': 'all 0.3s ease-in-out',
                        'cursor': 'pointer',
                        'outline': 'none',
                        'align-items': 'center'
                    },
                    className='dropdown-custom'
                ),
                # Document Names Dropdown
                dcc.Dropdown(
                    id='document-names-1-dropdown',
                    multi=True,
                    options=[{'label': doc, 'value': doc} for doc in prod_data['document_names'].unique()],
                    placeholder='Select Document Names',
                    style={
                        'width': '100%', 
                        'padding': '5px 10px', 
                        'border': '1px solid #d1d1d1', 
                        'border-radius': '8px',
                        'background-color': '#ffffff',
                        'font-size': '16px',
                        'color': '#333',
                        'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.1)',
                        'transition': 'all 0.3s ease-in-out',
                        'cursor': 'pointer',
                        'outline': 'none',
                        'align-items': 'center'
                    },
                    className='dropdown-custom'
                ),
                # Site Names Dropdown
                dcc.Dropdown(
                    id='site-names-1-dropdown',
                    multi=True,
                    options=[{'label': sites, 'value': sites} for sites in prod_data['sites'].unique()],
                    placeholder='Select Sites Names',
                    style={
                        'width': '100%', 
                        'padding': '5px 10px', 
                        'border': '1px solid #d1d1d1', 
                        'border-radius': '8px',
                        'background-color': '#ffffff',
                        'font-size': '16px',
                        'color': '#333',
                        'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.1)',
                        'transition': 'all 0.3s ease-in-out',
                        'cursor': 'pointer',
                        'outline': 'none',
                        'align-items': 'center'
                    },
                    className='dropdown-custom'
                ),
            ], style={
                'display': 'flex', 
                'justify-content': 'space-between',
                'align-items': 'center', 
                'width': '70%',
                'margin': '35px auto',
                'gap': '20px',  # Added gap to make spacing consistent
            }),

            # Cards for KPIs
            html.Div([
                html.Div([html.H4("Total DT IDs Downloaded Count"), html.P(id="total-dt-ids")], 
                        className="card", style={'border': '1px solid #007BFF', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)','padding': '15px', 'width': '17%', 'textAlign': 'center', 'background-color': '#87CEEB'}),
                html.Div([html.H4("Total Unique Documents Count"), html.P(id="unique-documents-1-count")], 
                        className="card", style={'border': '1px solid #007BFF', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)','padding': '15px', 'width': '17%', 'textAlign': 'center', 'background-color': '#87CEEB'}),
                html.Div([html.H4("Total Unique Sites Count"), html.P(id="unique-sites-1-count")], 
                        className="card", style={'border': '1px solid #007BFF', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)','padding': '15px', 'width': '17%', 'textAlign': 'center', 'background-color': '#87CEEB'}),
                html.Div([html.H4("Total Unique Instances Count"), html.P(id="unique-instances")], 
                        className="card", style={'border': '1px solid #007BFF', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)','padding': '15px', 'width': '17%', 'textAlign': 'center', 'background-color': '#87CEEB'}),
                html.Div([html.H4("Total Unique Tickets Count"), html.P(id="unique-tickets-1")], 
                        className="card", style={'border': '1px solid #007BFF', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)','padding': '15px', 'width': '17%', 'textAlign': 'center', 'background-color': '#87CEEB'}),
            ], style={'display': 'flex', 'justify-content': 'space-around', 'margin-bottom': '20px'}),

            # Row for first two charts
            html.Div([
                dcc.Graph(id='dt-ids-sites-chart', style={'width': '48%', 'height': '500px', 'padding': '10px', 'background-color': '#ffffff', 'border-radius': '10px','box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),
                dcc.Graph(id='dt-ids-process-chart', style={'width': '48%', 'height': '500px', 'padding': '10px', 'background-color': '#ffffff', 'border-radius': '10px','box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),
            ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px'}),

            # Row for second two charts
            html.Div([
                dcc.Graph(id='dt-ids-document-chart', style={'width': '48%', 'height': '500px', 'padding': '10px', 'background-color': '#ffffff', 'border-radius': '10px','box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),
                dcc.Graph(id='dt-ids-instances-chart', style={'width': '48%', 'height': '500px', 'padding': '10px', 'background-color': '#ffffff', 'border-radius': '10px','box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),
            ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px'}),
        ], style={'display': 'block'}),

        #---------------------------------------------------------------------------ADR Content---------------------------------------------------------------------------
        html.Div(id='adr-content', children=[
            html.Div([
                dcc.Dropdown(
                    id='year-dropdown-2',
                    multi=True,
                    options=[{'label': year, 'value': year} for year in adr_data['year'].unique()],
                    placeholder='Select Years',
                    style={
                        'width': '100%', 
                        'padding': '5px 10px', 
                        'border': '1px solid #d1d1d1', 
                        'border-radius': '8px',
                        'background-color': '#ffffff',
                        'font-size': '16px',
                        'color': '#333',
                        'box-shadow': '0px 2px 8px rgba(0, 0, 0, 0.1)',
                        'transition': 'all 0.3s ease-in-out',
                        'cursor': 'pointer'
                    },
                    className='dropdown-custom'
                ),
                dcc.Dropdown(
                    id='document-names-2-dropdown',
                    multi=True,
                    options=[{'label': doc, 'value': doc} for doc in adr_data['document_names'].unique()],
                    placeholder='Select Document Names',
                    style={
                        'width': '100%', 
                        'padding': '5px 10px', 
                        'border': '1px solid #d1d1d1', 
                        'border-radius': '8px',
                        'background-color': '#ffffff',
                        'font-size': '16px',
                        'color': '#333',
                        'box-shadow': '0px 2px 8px rgba(0, 0, 0, 0.1)',
                        'transition': 'all 0.3s ease-in-out',
                        'cursor': 'pointer'
                    },
                    className='dropdown-custom'
                ),
                dcc.Dropdown(
                    id='site-names-2-dropdown',
                    multi=True,
                    options=[{'label': sites, 'value': sites} for sites in adr_data['sites'].unique()],
                    placeholder='Select Sites Names',
                    style={
                        'width': '100%', 
                        'padding': '5px 10px', 
                        'border': '1px solid #d1d1d1', 
                        'border-radius': '8px',
                        'background-color': '#ffffff',
                        'font-size': '16px',
                        'color': '#333',
                        'box-shadow': '0px 2px 8px rgba(0, 0, 0, 0.1)',
                        'transition': 'all 0.3s ease-in-out',
                        'cursor': 'pointer',
                        'align-items': 'center',
                    },
                    className='dropdown-custom'
                )
            ], style={
                'display': 'flex', 
                'justify-content': 'space-between',
                'align-items': 'center', 
                'width': '70%',
                'margin': '35px auto',
                'gap': '20px',
            }),
            html.Div([
                html.Div([html.H4("Total Zips Transferred Count"), html.P(id="total-zt-count")], className="card", style={'border': '1px solid #007BFF', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)','padding': '15px', 'width': '17%', 'textAlign': 'center', 'background-color': '#87CEEB'}),
                html.Div([html.H4("Total Unique Documents Count"), html.P(id="unique-documents-2-count")], className="card", style={'border': '1px solid #007BFF', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)','padding': '15px', 'width': '17%', 'textAlign': 'center', 'background-color': '#87CEEB'}),
                html.Div([html.H4("Total Unique Sites Count"), html.P(id="unique-sites-2-count")], className="card", style={'border': '1px solid #007BFF', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)','padding': '15px', 'width': '17%', 'textAlign': 'center', 'background-color': '#87CEEB'}),
                html.Div([html.H4("Total Unique Tickets Count"), html.P(id="unique-tickets-2")], className="card", style={'border': '1px solid #007BFF', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)','padding': '15px', 'width': '17%', 'textAlign': 'center', 'background-color': '#87CEEB'}),
            ], style={'display': 'flex', 'justify-content': 'space-around', 'margin-bottom': '20px'}),
            html.Div([
                dcc.Graph(id='zt-counts-document-chart', style={'width': '48%', 'height': '500px', 'padding': '10px', 'background-color': '#ffffff', 'border-radius': '10px','box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),
                dcc.Graph(id='zt-counts-sites-chart', style={'width': '48%', 'height': '500px', 'padding': '10px', 'background-color': '#ffffff', 'border-radius': '10px','box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),
            ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px'}),
            html.Div([
                dcc.Graph(id='zt-counts-month-name-sites-documents-chart', style={'width': '48%', 'height': '500px', 'padding': '10px', 'background-color': '#ffffff', 'border-radius': '10px','box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),
                dcc.Graph(id='zt-counts-date-of-transfer-chart', style={'width': '48%', 'height': '500px', 'padding': '10px', 'background-color': '#ffffff', 'border-radius': '10px','box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),
            ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px'}),
        ], style={'display': 'none'}),
        
        #---------------------------------------------------------------------------ADE_LabelIMG Content---------------------------------------------------------------------------
        html.Div(id='ade-labelimg-content', children=[
            # ADE-LabelIMG content
            html.Div([
                # Dropdowns for filters in one row
                dcc.Dropdown(
                    id='year-dropdown-3',
                    multi=True,
                    options=[{'label': year, 'value': year} for year in labelimg_data['year'].unique()],
                    placeholder='Select Years',
                    style={
                        'width': '100%', 
                        'padding': '5px 10px', 
                        'border': '1px solid #d1d1d1', 
                        'border-radius': '8px',
                        'background-color': '#ffffff',
                        'font-size': '16px',
                        'color': '#333',
                        'box-shadow': '0px 2px 8px rgba(0, 0, 0, 0.1)',
                        'transition': 'all 0.3s ease-in-out',
                        'cursor': 'pointer'
                    },
                    className='dropdown-custom'
                ),
                dcc.Dropdown(
                    id='document-names-3-dropdown',
                    multi=True,
                    options=[{'label': doc, 'value': doc} for doc in labelimg_data['document_names'].unique()],
                    placeholder='Select Document Names',
                    style={
                        'width': '100%', 
                        'padding': '5px 10px', 
                        'border': '1px solid #d1d1d1', 
                        'border-radius': '8px',
                        'background-color': '#ffffff',
                        'font-size': '16px',
                        'color': '#333',
                        'box-shadow': '0px 2px 8px rgba(0, 0, 0, 0.1)',
                        'transition': 'all 0.3s ease-in-out',
                        'cursor': 'pointer'
                    },
                    className='dropdown-custom'
                ),
                dcc.Dropdown(
                    id='purpose-names-3-dropdown',
                    multi=True,
                    options=[{'label': purpose, 'value': purpose} for purpose in labelimg_data['purpose'].unique()],
                    placeholder='Select Purpose Names',
                    style={
                        'width': '100%', 
                        'padding': '5px 10px', 
                        'border': '1px solid #d1d1d1', 
                        'border-radius': '8px',
                        'background-color': '#ffffff',
                        'font-size': '16px',
                        'color': '#333',
                        'box-shadow': '0px 2px 8px rgba(0, 0, 0, 0.1)',
                        'transition': 'all 0.3s ease-in-out',
                        'cursor': 'pointer'
                    },
                    className='dropdown-custom'
                )
            ], style={
                'display': 'flex', 
                'justify-content': 'space-between',
                'align-items': 'center', 
                'width': '70%',
                'margin': '35px auto',
                'gap': '20px',
            }),

            # KPI Cards section
            html.Div([
                html.Div([html.H4("Total Documents Uploaded Count"), html.P(id="total-uploaded-count")], 
                    className="card", style={'border': '1px solid #007BFF', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)','padding': '15px', 'width': '17%', 'textAlign': 'center', 'background-color': '#87CEEB'}
                ),
                html.Div([html.H4("Total Unique Documents Count"), html.P(id="unique-documents-3-count")], 
                    className="card", style={'border': '1px solid #007BFF', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)','padding': '15px', 'width': '17%', 'textAlign': 'center', 'background-color': '#87CEEB'}
                ),
                html.Div([html.H4("Total Unique Purpose Count"), html.P(id="unique-purpose-3-count")], 
                    className="card", style={'border': '1px solid #007BFF', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)','padding': '15px', 'width': '17%', 'textAlign': 'center', 'background-color': '#87CEEB'}
                ),
                html.Div([html.H4("Total Unique Tickets Count"), html.P(id="unique-tickets-3")], 
                    className="card", style={'border': '1px solid #007BFF', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)','padding': '15px', 'width': '17%', 'textAlign': 'center', 'background-color': '#87CEEB'}
                )
            ], style={'display': 'flex', 'justify-content': 'space-around', 'margin-bottom': '20px'}),

            # Graphs Section 1
            html.Div([
                dcc.Graph(id='doc-uploaded-counts-document-chart', style={'width': '48%', 'height': '500px', 'padding': '10px', 'background-color': '#ffffff', 'border-radius': '10px','box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),
                dcc.Graph(id='doc-uploaded-counts-purpose-chart', style={'width': '48%', 'height': '500px', 'padding': '10px', 'background-color': '#ffffff', 'border-radius': '10px','box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'})
            ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px'}),

            # Graphs Section 2
            html.Div([
                dcc.Graph(id='doc-uploaded-counts-month-name-purpose-documents-chart', style={'width': '48%', 'height': '500px', 'padding': '10px', 'background-color': '#ffffff', 'border-radius': '10px','box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),
                dcc.Graph(id='doc-uploaded-counts-date-of-transfer-by-doc-chart', style={'width': '48%', 'height': '500px', 'padding': '10px', 'background-color': '#ffffff', 'border-radius': '10px','box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'})
            ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px'})
        ], style={'display': 'none'}),

        #---------------------------------------------------------------------------ADE_AIQ Content---------------------------------------------------------------------------

        html.Div(id='ade-aiq-content', children=[
            # ADE-AIQ content
            html.Div([
                # Dropdowns for filters in one row
                dcc.Dropdown(
                    id='year-dropdown-4',
                    multi=True,
                    options=[{'label': year, 'value': year} for year in aiq_data['year'].unique()],
                    placeholder='Select Years',
                    style={
                        'width': '100%', 
                        'padding': '5px 10px', 
                        'border': '1px solid #d1d1d1', 
                        'border-radius': '8px',
                        'background-color': '#ffffff',
                        'font-size': '16px',
                        'color': '#333',
                        'box-shadow': '0px 2px 8px rgba(0, 0, 0, 0.1)',
                        'transition': 'all 0.3s ease-in-out',
                        'cursor': 'pointer'
                    },
                    className='dropdown-custom'
                ),
                dcc.Dropdown(
                    id='document-names-4-dropdown',
                    multi=True,
                    options=[{'label': doc, 'value': doc} for doc in aiq_data['document_names'].unique()],
                    placeholder='Select Document Names',
                    style={
                        'width': '100%', 
                        'padding': '5px 10px', 
                        'border': '1px solid #d1d1d1', 
                        'border-radius': '8px',
                        'background-color': '#ffffff',
                        'font-size': '16px',
                        'color': '#333',
                        'box-shadow': '0px 2px 8px rgba(0, 0, 0, 0.1)',
                        'transition': 'all 0.3s ease-in-out',
                        'cursor': 'pointer'
                    },
                    className='dropdown-custom'
                ),
                dcc.Dropdown(
                    id='purpose-names-4-dropdown',
                    multi=True,
                    options=[{'label': purpose, 'value': purpose} for purpose in aiq_data['purpose'].unique()],
                    placeholder='Select Purpose Names',
                    style={
                        'width': '100%', 
                        'padding': '5px 10px', 
                        'border': '1px solid #d1d1d1', 
                        'border-radius': '8px',
                        'background-color': '#ffffff',
                        'font-size': '16px',
                        'color': '#333',
                        'box-shadow': '0px 2px 8px rgba(0, 0, 0, 0.1)',
                        'transition': 'all 0.3s ease-in-out',
                        'cursor': 'pointer'
                    },
                    className='dropdown-custom'
                )
            ], style={
                'display': 'flex', 
                'justify-content': 'space-between',
                'align-items': 'center', 
                'width': '70%',
                'margin': '35px auto',
                'gap': '20px',
            }),

            # KPI Cards section
            html.Div([
                html.Div([html.H4("Total Documents Uploaded Count"), html.P(id="total-uploaded-count-4")], 
                    className="card", style={'border': '1px solid #007BFF', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)','padding': '15px', 'width': '17%', 'textAlign': 'center', 'background-color': '#87CEEB'}
                ),
                html.Div([html.H4("Total Unique Documents Count"), html.P(id="unique-documents-4-count")], 
                    className="card", style={'border': '1px solid #007BFF', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)','padding': '15px', 'width': '17%', 'textAlign': 'center', 'background-color': '#87CEEB'}
                ),
                html.Div([html.H4("Total Unique Purpose Count"), html.P(id="unique-purpose-4-count")], 
                    className="card", style={'border': '1px solid #007BFF', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)','padding': '15px', 'width': '17%', 'textAlign': 'center', 'background-color': '#87CEEB'}
                ),
                html.Div([html.H4("Total Unique Tickets Count"), html.P(id="unique-tickets-4-count")], 
                    className="card", style={'border': '1px solid #007BFF', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)','padding': '15px', 'width': '17%', 'textAlign': 'center', 'background-color': '#87CEEB'}
                )
            ], style={'display': 'flex', 'justify-content': 'space-around', 'margin-bottom': '20px'}),

            # Graphs Section 1
            html.Div([
                dcc.Graph(id='doc-uploaded-counts-document-chart-1', style={'width': '48%', 'height': '500px', 'padding': '10px', 'background-color': '#ffffff', 'border-radius': '10px','box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),
                dcc.Graph(id='doc-uploaded-counts-purpose-chart-1', style={'width': '48%', 'height': '500px', 'padding': '10px', 'background-color': '#ffffff', 'border-radius': '10px','box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'})
            ], style={'display': 'flex', 'justify-content': 'space-around', 'margin-bottom': '20px'}),

            # Graphs Section 2
            html.Div([
                dcc.Graph(id='doc-uploaded-counts-month-name-purpose-documents-chart-1', style={'width': '48%', 'height': '500px', 'padding': '10px', 'background-color': '#ffffff', 'border-radius': '10px','box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),
                dcc.Graph(id='doc-uploaded-counts-date-of-transfer-by-doc-chart-1', style={'width': '48%', 'height': '500px', 'padding': '10px', 'background-color': '#ffffff', 'border-radius': '10px','box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'})
            ], style={'display': 'flex', 'justify-content': 'space-around', 'margin-bottom': '20px'})
        ], style={'display': 'none'}),

    ])
])
#---------------------------------------------------------------------------Prod KPIs and Dropdowns---------------------------------------------------------------------------

# Callback to update KPIs and dropdown options
@app.callback(
    [Output('total-dt-ids', 'children'),
     Output('unique-documents-1-count', 'children'),
     Output('unique-sites-1-count', 'children'),
     Output('unique-instances', 'children'),
     Output('unique-tickets-1', 'children'),
     Output('year-dropdown-1', 'options'),
     Output('document-names-1-dropdown', 'options'),
     Output('site-names-1-dropdown', 'options')],
    [Input('year-dropdown-1', 'value'),
     Input('document-names-1-dropdown', 'value'),
     Input('site-names-1-dropdown', 'value')]
)
def update_prod_kpis_and_dropdown(selected_years_1, selected_doc_1, selected_sites_1):
    # Ensure 'prod_data' is available and copied
    data = prod_data.copy() if 'prod_data' in globals() else pd.DataFrame()

    # Apply filters based on the selected inputs
    if selected_years_1:
        data = data[data['year'].isin(selected_years_1)]
    if selected_doc_1:
        data = data[data['document_names'].isin(selected_doc_1)]
    if selected_sites_1:
        data = data[data['sites'].isin(selected_sites_1)]

    # Calculate KPIs
    total_dt_ids = data['dt_ids'].sum()
    unique_documents = data['document_names'].nunique()
    unique_sites = data['sites'].nunique()
    unique_instances = data['instances'].nunique()
    unique_tickets = data['tickets'].nunique()

    # Dropdown options based on the entire dataset (unfiltered prod_data)
    year_options = [{'label': str(year), 'value': year} for year in sorted(prod_data['year'].unique())]
    doc_options = [{'label': doc, 'value': doc} for doc in sorted(prod_data['document_names'].unique())]
    sites_options = [{'label': site, 'value': site} for site in sorted(prod_data['sites'].unique())]

    # Format the KPI values as strings to be displayed
    total_downloaded_count_str = f"{total_dt_ids:,}"  # Format with commas for large numbers
    unique_documents_count_str = f"{unique_documents:,}"
    unique_sites_count_str = f"{unique_sites:,}"
    unique_instances_count_str = f"{unique_instances:,}"
    unique_tickets_count_str = f"{unique_tickets:,}"

    # Return calculated KPIs and dropdown options
    return total_downloaded_count_str, unique_documents_count_str, unique_sites_count_str, unique_instances_count_str, unique_tickets_count_str, year_options, doc_options, sites_options

# Callback to update DT IDs by Site chart
@app.callback(
    Output('dt-ids-sites-chart', 'figure'),
    [Input('year-dropdown-1', 'value'),
     Input('document-names-1-dropdown', 'value'),
     Input('site-names-1-dropdown', 'value')]
)
def update_dt_ids_and_sites_chart(selected_years_1, selected_doc_1, selected_sites_1):
    data = prod_data.copy()

    # Apply filters
    if selected_years_1:
        data = data[data['year'].isin(selected_years_1)]
    if selected_doc_1:
        data = data[data['document_names'].isin(selected_doc_1)]
    if selected_sites_1:
        data = data[data['sites'].isin(selected_sites_1)]

    # Group by sites and get the top 20 sites
    site_wise = data.groupby('sites')['dt_ids'].sum().reset_index()
    site_wise = site_wise.sort_values(by='dt_ids', ascending=False).head(10)
    # Sort the data to ensure largest dt_ids are at the top
    top_10_sites_by_dt_ids = site_wise.sort_values(by='dt_ids', ascending=True)
    # Create bar chart
    fig = px.bar(top_10_sites_by_dt_ids, 
                 x='dt_ids', 
                 y='sites', 
                 title='Top 10 Sites by DT IDs Downloaded',text_auto='.2s',orientation='h',
                 labels={"sites": "Top 10 Sites", "dt_ids": "Total DT IDs Downloaded "}, 
                 color_discrete_sequence=['#87CEEB'])

    return fig

# Callback to update DT IDs by Process chart
@app.callback(
    Output('dt-ids-process-chart', 'figure'),
    [Input('year-dropdown-1', 'value'),
     Input('document-names-1-dropdown', 'value'),
     Input('site-names-1-dropdown', 'value')]
)
def update_dt_ids_process_chart(selected_years_1, selected_doc_1, selected_sites_1):
    data = prod_data.copy()

    # Apply filters
    if selected_years_1:
        data = data[data['year'].isin(selected_years_1)]
    if selected_doc_1:
        data = data[data['document_names'].isin(selected_doc_1)]
    if selected_sites_1:
        data = data[data['sites'].isin(selected_sites_1)]

    # Group by process
    process_wise = data.groupby('process')['dt_ids'].sum().reset_index()

    # Create horizontal bar chart
    fig = px.bar(process_wise, 
                 x='dt_ids', 
                 y='process', 
                 orientation='h', 
                 title='Total DT IDs by Process',
                 text_auto=".2s",
                 labels={"process": "Process", "dt_ids": "Total DT IDs"}, 
                 color_discrete_sequence=['#87CEEB'])

    return fig

# Callback to update DT IDs by Document Names chart
@app.callback(
    Output('dt-ids-document-chart', 'figure'),
    [Input('year-dropdown-1', 'value'),
     Input('document-names-1-dropdown', 'value'),
     Input('site-names-1-dropdown', 'value')]
)
def update_dt_ids_document_chart(selected_years_1, selected_doc_1, selected_sites_1):
    data = prod_data.copy()

    # Apply filters
    if selected_years_1:
        data = data[data['year'].isin(selected_years_1)]
    if selected_doc_1:
        data = data[data['document_names'].isin(selected_doc_1)]
    if selected_sites_1:
        data = data[data['sites'].isin(selected_sites_1)]

    # Group by document names and get the top 20 documents by DT IDs
    doc_wise = data.groupby("document_names")['dt_ids'].sum().reset_index()
    top_20_docs = doc_wise.sort_values(by='dt_ids', ascending=False).head(10)
    top_10_docs_wise_dtids = top_20_docs.sort_values(by='dt_ids',ascending=True)

    # Create bar chart
    fig = px.bar(top_10_docs_wise_dtids, 
                 x="dt_ids", 
                 y="document_names", 
                 title="Top 10 Document Names by DT IDs Downloaded", 
                 color_discrete_sequence=['#87CEEB'], 
                 text_auto='.2s', 
                 labels={"document_names": "Top 10 Document Names", "dt_ids": "Total DT IDs Downloaded"})
    fig.update_layout(xaxis={'categoryorder': 'total descending'})

    return fig

# Callback to update DT IDs by Instance chart
@app.callback(
    Output('dt-ids-instances-chart', 'figure'),
    [Input('year-dropdown-1', 'value'),
     Input('document-names-1-dropdown', 'value'),
     Input('site-names-1-dropdown', 'value')]
)
def update_dt_ids_instance_chart(selected_years_1, selected_doc_1, selected_sites_1):
    data = prod_data.copy()

    # Apply filters
    if selected_years_1:
        data = data[data['year'].isin(selected_years_1)]
    if selected_doc_1:
        data = data[data['document_names'].isin(selected_doc_1)]
    if selected_sites_1:
        data = data[data['sites'].isin(selected_sites_1)]

    # Group by instances
    instance_wise = data.groupby('instances')['dt_ids'].sum().reset_index()

    # Create bar chart
    fig = px.bar(instance_wise, 
                 x='instances', 
                 y='dt_ids', 
                 title='Total DT IDs by Instance',text_auto='.2s',
                 labels={"instances": "Instances", "dt_ids": "Total DT IDs"},
                 color_discrete_sequence=['#87CEEB'])

    return fig

#---------------------------------------------------------------------------ADR KPIs and Dropdowns---------------------------------------------------------------------------

@app.callback(
    [Output('total-zt-count', 'children'),
     Output('unique-documents-2-count', 'children'),
     Output('unique-sites-2-count', 'children'),
     Output('unique-tickets-2', 'children'),
     Output('year-dropdown-2', 'options'),
     Output('document-names-2-dropdown', 'options'),
     Output('site-names-2-dropdown', 'options')],
    [Input('year-dropdown-2', 'value'),
     Input('document-names-2-dropdown', 'value'),
     Input('site-names-2-dropdown', 'value')]
)
def update_adr_kpis_and_dropdown(selected_years_2, selected_doc_2, selected_sites_2):
    # Use the original dataset and filter
    data = adr_data
    
    # Filter based on selections
    if selected_years_2:
        data = data[data['year'].isin(selected_years_2)]
    if selected_doc_2:
        data = data[data['document_names'].isin(selected_doc_2)]
    if selected_sites_2:
        data = data[data['sites'].isin(selected_sites_2)]
    
    # Calculate KPIs
    total_zt_count = data['total_zips_transferred'].sum()
    unique_documents = data['document_names'].nunique()
    unique_sites = data['sites'].nunique()
    unique_tickets = data['tickets'].nunique()
    
    # Dropdown options
    year_options = [{'label': str(year), 'value': year} for year in sorted(adr_data['year'].unique())]
    doc_options = [{'label': doc, 'value': doc} for doc in sorted(adr_data['document_names'].unique())]
    sites_options = [{'label': site, 'value': site} for site in sorted(adr_data['sites'].unique())]
    
        # Format the KPI values as strings to be displayed
    total_zt_count_str = f"{total_zt_count:,}"  # Format with commas for large numbers
    unique_documents_count_str = f"{unique_documents:,}"
    unique_sites_count_str = f"{unique_sites:,}"
    unique_tickets_count_str = f"{unique_tickets:,}"

    return total_zt_count_str, unique_documents_count_str, unique_sites_count_str, unique_tickets_count_str, year_options, doc_options, sites_options


@app.callback(
    Output('zt-counts-document-chart', 'figure'),
    [Input('year-dropdown-2', 'value'),
     Input('document-names-2-dropdown', 'value'),
     Input('site-names-2-dropdown', 'value')]
)
def update_zt_counts_document_chart(selected_years_2, selected_docs_2, selected_sites_2):
    data = adr_data
    if selected_years_2:
        data = data[data['year'].isin(selected_years_2)]
    if selected_docs_2:
        data = data[data['document_names'].isin(selected_docs_2)]
    if selected_sites_2:
        data = data[data['sites'].isin(selected_sites_2)]

    doc_wise = data.groupby("document_names")['total_zips_transferred'].sum().reset_index()
    top_10_docs = doc_wise.sort_values(by='total_zips_transferred', ascending=False).head(10)
    top_10_docs_zips = top_10_docs.sort_values(by='total_zips_transferred',ascending=True)

    fig = px.bar(top_10_docs_zips, 
                 x="total_zips_transferred", 
                 y="document_names", 
                 title="Top 10 Document Names by Zips Transferred", 
                 color_discrete_sequence=['#87CEEB'], 
                 text_auto='.2s', orientation='h',
                 labels={"document_names": "Document Name", "total_zips_transferred": "Zips"})
    fig.update_layout(xaxis={'categoryorder': 'total descending'})
    
    return fig


@app.callback(
    Output('zt-counts-sites-chart', 'figure'),
    [Input('year-dropdown-2', 'value'),
     Input('document-names-2-dropdown', 'value'),
     Input('site-names-2-dropdown', 'value')]
)
def update_zt_counts_sites_chart(selected_years_2, selected_docs_2, selected_sites_2):
    data = adr_data
    if selected_years_2:
        data = data[data['year'].isin(selected_years_2)]
    if selected_docs_2:
        data = data[data['document_names'].isin(selected_docs_2)]
    if selected_sites_2:
        data = data[data['sites'].isin(selected_sites_2)]
    
    site_wise = data.groupby('sites')['total_zips_transferred'].sum().reset_index()
    top_20_sites = site_wise.sort_values(by='total_zips_transferred', ascending=False).head(20)

    fig = px.bar(top_20_sites, 
                 x='sites', 
                 y='total_zips_transferred', 
                 title='Sites wise Zips Transferred', text_auto='.2s',
                 labels={"sites": "Sites", "total_zips_transferred": "Total Zips Transferred"}, 
                 color_discrete_sequence=['#87CEEB'])
    fig.update_traces(text=top_20_sites['total_zips_transferred'], textposition='outside')

    return fig


@app.callback(
    Output('zt-counts-month-name-sites-documents-chart', 'figure'),
    [Input('year-dropdown-2', 'value'),
     Input('document-names-2-dropdown', 'value'),
     Input('site-names-2-dropdown', 'value')]
)
def update_zt_counts_month_name_chart(selected_years_2, selected_docs_2, selected_sites_2):
    data = adr_data
    if selected_years_2:
        data = data[data['year'].isin(selected_years_2)]
    if selected_docs_2:
        data = data[data['document_names'].isin(selected_docs_2)]
    if selected_sites_2:
        data = data[data['sites'].isin(selected_sites_2)]
    
    site_wise = data.groupby('month_name')['total_zips_transferred'].sum().reset_index()
    # Define the correct chronological order for months
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    # Convert 'month_name' to a categorical type with the specified order
    site_wise['month_name'] = pd.Categorical(site_wise['month_name'], categories=month_order, ordered=True)
    # Now sort by the ordered 'month_name' column
    sorted_site_wise = site_wise.sort_values(by='month_name', ascending=False)
    fig = px.bar(sorted_site_wise, 
                 x='total_zips_transferred', 
                 y='month_name', 
                 text_auto='.2s', 
                 title='Month wise Zips Transferred',
                 labels={"month_name": "Months", "total_zips_transferred": "Total Zips Transferred"}, 
                 color_discrete_sequence=['#87CEEB'])
    
    return fig


@app.callback(
    Output('zt-counts-date-of-transfer-chart', 'figure'),
    [Input('year-dropdown-2', 'value'),
     Input('document-names-2-dropdown', 'value'),
     Input('site-names-2-dropdown', 'value')]
)
def update_zt_counts_date_chart(selected_years_2, selected_docs_2, selected_sites_2):
    data = adr_data
    if selected_years_2:
        data = data[data['year'].isin(selected_years_2)]
    if selected_docs_2:
        data = data[data['document_names'].isin(selected_docs_2)]
    if selected_sites_2:
        data = data[data['sites'].isin(selected_sites_2)]

    # Group by 'date_of_transfer' and sum 'total_zips_transferred'
    date_wise = data.groupby('date_of_transfer')['total_zips_transferred'].sum().reset_index()

    # Sort by 'date_of_transfer' in ascending order (which should be the default)
    date_wise = date_wise.sort_values(by='date_of_transfer', ascending=True)

    fig = px.bar(date_wise, 
                 x='date_of_transfer', 
                 y='total_zips_transferred', 
                 title='Dates wise Zips Transferred', 
                 labels={"total_zips_transferred": "Total Zips Transferred", "date_of_transfer": "Dates"}, 
                 color_discrete_sequence=['#87CEEB'])

    return fig

#---------------------------------------------------------------------------ADE_LabelIMG KPIs and Dropdowns---------------------------------------------------------------------------

# Callback to update KPIs and Dropdowns
@app.callback(
    [Output('total-uploaded-count', 'children'),
     Output('unique-documents-3-count', 'children'),
     Output('unique-purpose-3-count', 'children'),
     Output('unique-tickets-3', 'children'),
     Output('year-dropdown-3', 'options'),
     Output('document-names-3-dropdown', 'options'),
     Output('purpose-names-3-dropdown', 'options')],
    [Input('year-dropdown-3', 'value'),
     Input('document-names-3-dropdown', 'value'),
     Input('purpose-names-3-dropdown', 'value')]
)
def update_limg_kpis_and_dropdown(selected_years_3, selected_doc_3, selected_purpose_3):
    # Copy the data to avoid modifying the original dataframe
    limg_data = labelimg_data.copy()

    # Filter data based on selections, handling the case when dropdown values are not selected
    if selected_years_3:
        limg_data = limg_data[limg_data['year'].isin(selected_years_3)]
    if selected_doc_3:
        limg_data = limg_data[limg_data['document_names'].isin(selected_doc_3)]
    if selected_purpose_3:
        limg_data = limg_data[limg_data['purpose'].isin(selected_purpose_3)]

    # Calculate KPIs
    total_doc_uploaded_count = limg_data['total_uploaded'].sum()
    unique_documents = limg_data['document_names'].nunique()
    unique_purposes = limg_data['purpose'].nunique()
    unique_tickets = limg_data['tickets'].nunique()

    # Generate dropdown options from the original dataset (before filtering)
    year_options = [{'label': str(year), 'value': year} for year in sorted(labelimg_data['year'].unique())]
    doc_options = [{'label': doc, 'value': doc} for doc in sorted(labelimg_data['document_names'].unique())]
    purpose_options = [{'label': purpose, 'value': purpose} for purpose in sorted(labelimg_data['purpose'].unique())]

            # Format the KPI values as strings to be displayed
    total_doc_uploaded_count_str = f"{total_doc_uploaded_count:,}"  # Format with commas for large numbers
    unique_documents_count_str = f"{unique_documents:,}"
    unique_purpose_count_str = f"{unique_purposes:,}"
    unique_tickets_count_str = f"{unique_tickets:,}"


    return (total_doc_uploaded_count_str, unique_documents_count_str, unique_purpose_count_str, unique_tickets_count_str, 
            year_options, doc_options, purpose_options)


# Callback to update the "Top 20 Document by Uploaded Count" chart
@app.callback(
    Output('doc-uploaded-counts-document-chart', 'figure'),
    [Input('year-dropdown-3', 'value'),
     Input('document-names-3-dropdown', 'value'),
     Input('purpose-names-3-dropdown', 'value')]
)
def update_doc_uploaded_counts_chart(selected_years_3, selected_doc_3, selected_purpose_3):
    limg_data = labelimg_data.copy()

    # Apply filters
    if selected_years_3:
        limg_data = limg_data[limg_data['year'].isin(selected_years_3)]
    if selected_doc_3:
        limg_data = limg_data[limg_data['document_names'].isin(selected_doc_3)]
    if selected_purpose_3:
        limg_data = limg_data[limg_data['purpose'].isin(selected_purpose_3)]

    doc_wise = limg_data.groupby("document_names")['total_uploaded'].sum().reset_index()
    top_10_docs = doc_wise.sort_values(by='total_uploaded', ascending=False).head(10)
    sorting_docs = top_10_docs.sort_values(by='total_uploaded',ascending=True)

    fig = px.bar(sorting_docs, x="total_uploaded", y="document_names", title="Top 10 Documents Uploaded in LabelIMG Tool",
                 color_discrete_sequence=['#87CEEB'], text='total_uploaded',orientation='h',text_auto='.2s',
                 labels={"document_names": "Document Name", "total_uploaded": "Total Uploaded Documents Count"})
    fig.update_layout(xaxis={'categoryorder': 'total descending'})

    return fig


# Callback to update "Total Uploaded Documents Count by Purpose" chart
@app.callback(
    Output('doc-uploaded-counts-purpose-chart', 'figure'),
    [Input('year-dropdown-3', 'value'),
     Input('document-names-3-dropdown', 'value'),
     Input('purpose-names-3-dropdown', 'value')]
)
def update_doc_uploaded_counts_purpose_chart(selected_years_3, selected_doc_3, selected_purpose_3):
    limg_data = labelimg_data.copy()

    # Apply filters
    if selected_years_3:
        limg_data = limg_data[limg_data['year'].isin(selected_years_3)]
    if selected_doc_3:
        limg_data = limg_data[limg_data['document_names'].isin(selected_doc_3)]
    if selected_purpose_3:
        limg_data = limg_data[limg_data['purpose'].isin(selected_purpose_3)]

    purpose_wise = limg_data.groupby('purpose')['total_uploaded'].sum().reset_index()
    purpose_wise = purpose_wise.sort_values(by='total_uploaded', ascending=False).head(20)

    fig = px.bar(purpose_wise, x='purpose', y='total_uploaded', color='purpose',
                 title='Total Uploaded Documents Count by Purpose',text_auto='.2s',
                 labels={"purpose": "Purpose", "total_uploaded": "Total Uploaded Documents Count"},
                 color_discrete_sequence=['#87CEEB'])
    fig.update_traces(text=purpose_wise['total_uploaded'], textposition='outside')

    return fig


# Callback to update "Total Documents Uploaded by Purpose with Month" chart
@app.callback(
    Output('doc-uploaded-counts-month-name-purpose-documents-chart', 'figure'),
    [Input('year-dropdown-3', 'value'),
     Input('document-names-3-dropdown', 'value'),
     Input('purpose-names-3-dropdown', 'value')]
)
def update_doc_uploaded_counts_month_name_chart(selected_years_3, selected_doc_3, selected_purpose_3):
    limg_data = labelimg_data.copy()

    # Apply filters
    if selected_years_3:
        limg_data = limg_data[limg_data['year'].isin(selected_years_3)]
    if selected_doc_3:
        limg_data = limg_data[limg_data['document_names'].isin(selected_doc_3)]
    if selected_purpose_3:
        limg_data = limg_data[limg_data['purpose'].isin(selected_purpose_3)]

    # Group by 'month_name' and sum 'total_uploaded'
    month_wise = limg_data.groupby('month_name')['total_uploaded'].sum().reset_index()

    # Define the correct chronological order for months
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Convert 'month_name' to a categorical type with the specified order
    month_wise['month_name'] = pd.Categorical(month_wise['month_name'], categories=month_order, ordered=True)

    # Sort the data by the 'month_name' column to ensure it appears in the correct order
    month_wise = month_wise.sort_values('month_name',ascending=False)

    # Create the horizontal bar chart
    fig = px.bar(month_wise, 
                x='total_uploaded', 
                y='month_name',
                title='Total Documents Uploaded by Month', 
                orientation='h', 
                text_auto='.2s',
                labels={"month_name": "Months", "total_uploaded": "Total Documents Uploaded"},
                color_discrete_sequence=['#87CEEB'])

    # Return the figure for display
    return fig


# Callback to update "Total Documents Uploaded Count by Dates" chart
@app.callback(
    Output('doc-uploaded-counts-date-of-transfer-by-doc-chart', 'figure'),
    [Input('year-dropdown-3', 'value'),
     Input('document-names-3-dropdown', 'value'),
     Input('purpose-names-3-dropdown', 'value')]
)
def update_doc_uploaded_counts_by_date_of_transfer_chart(selected_years_3, selected_doc_3, selected_purpose_3):
    limg_data = labelimg_data.copy()

    # Apply filters
    if selected_years_3:
        limg_data = limg_data[limg_data['year'].isin(selected_years_3)]
    if selected_doc_3:
        limg_data = limg_data[limg_data['document_names'].isin(selected_doc_3)]
    if selected_purpose_3:
        limg_data = limg_data[limg_data['purpose'].isin(selected_purpose_3)]

    date_wise = limg_data.groupby('uploaded_date')['total_uploaded'].sum().reset_index()

    fig = px.bar(date_wise, x='uploaded_date', y='total_uploaded',
                 title='Total Documents Uploaded Count by Dates',
                 labels={"uploaded_date": "Uploaded Date", "total_uploaded": "Total Documents Uploaded Count"},
                 color_discrete_sequence=['#87CEEB'])

    return fig

#---------------------------------------------------------------------------ADE_AIQ KPIs and Dropdowns---------------------------------------------------------------------------
@app.callback(
    [Output('total-uploaded-count-4', 'children'),
     Output('unique-documents-4-count', 'children'),
     Output('unique-purpose-4-count', 'children'),
     Output('unique-tickets-4-count', 'children'),
     Output('year-dropdown-4', 'options'),
     Output('document-names-4-dropdown', 'options'),
     Output('purpose-names-4-dropdown', 'options')],
    [Input('year-dropdown-4', 'value'),
     Input('document-names-4-dropdown', 'value'),
     Input('purpose-names-4-dropdown', 'value')]
)
def update_aiq_kpis_and_dropdown(selected_years_4, selected_doc_4, selected_purpose_4):
    global aiq_data
    filtered_aiq_data = aiq_data.copy()  # Make a copy of the dataset to filter

    # Apply filters based on user selections
    if selected_years_4:
        filtered_aiq_data = filtered_aiq_data[filtered_aiq_data['year'].isin(selected_years_4)]
    if selected_doc_4:
        filtered_aiq_data = filtered_aiq_data[filtered_aiq_data['document_names'].isin(selected_doc_4)]
    if selected_purpose_4:
        filtered_aiq_data = filtered_aiq_data[filtered_aiq_data['purpose'].isin(selected_purpose_4)]

    # Calculate KPIs
    total_doc_uploaded_count = filtered_aiq_data['total_uploaded'].sum()  # Sum of total documents uploaded
    unique_documents = filtered_aiq_data['document_names'].nunique()  # Number of unique documents
    unique_purposes = filtered_aiq_data['purpose'].nunique()  # Number of unique purposes
    unique_tickets = filtered_aiq_data['tickets'].nunique()  # Number of unique tickets

    # Prepare dropdown options from the full dataset (aiq_data)
    year_options = [{'label': str(year), 'value': year} for year in sorted(aiq_data['year'].unique())]
    doc_options = [{'label': doc, 'value': doc} for doc in sorted(aiq_data['document_names'].unique())]
    purpose_options = [{'label': purpose, 'value': purpose} for purpose in sorted(aiq_data['purpose'].unique())]

    # Format the KPI values as strings to be displayed
    total_uploaded_str = f"{total_doc_uploaded_count:,}"  # Format with commas for large numbers
    unique_documents_str = f"{unique_documents:,}"
    unique_purposes_str = f"{unique_purposes:,}"
    unique_tickets_str = f"{unique_tickets:,}"

    # Return all outputs
    return total_uploaded_str, unique_documents_str, unique_purposes_str, unique_tickets_str, year_options, doc_options, purpose_options

# Update document count by document chart AIQ
@app.callback(
    Output('doc-uploaded-counts-document-chart-1', 'figure'),
    [Input('year-dropdown-4', 'value'),
     Input('document-names-4-dropdown', 'value'),
     Input('purpose-names-4-dropdown', 'value')]
)
def update_aiq_doc_uploaded_counts_chart(selected_years_4, selected_doc_4, selected_purpose_4):
    global aiq_data  # Ensure aiq_data is a global variable
    
    # Filter the data based on user input
    filtered_data = aiq_data.copy()  # Avoid modifying the original DataFrame
    if selected_years_4:
        filtered_data = filtered_data[filtered_data['year'].isin(selected_years_4)]
    if selected_doc_4:
        filtered_data = filtered_data[filtered_data['document_names'].isin(selected_doc_4)]
    if selected_purpose_4:
        filtered_data = filtered_data[filtered_data['purpose'].isin(selected_purpose_4)]
    
    # Aggregate and plot the top 20 documents
    doc_wise = filtered_data.groupby("document_names")['total_uploaded'].sum().reset_index()
    top_10_docs = doc_wise.sort_values(by='total_uploaded', ascending=False).head(10)
    sorting_docs = top_10_docs.sort_values(by='total_uploaded', ascending=True)

    fig = px.bar(sorting_docs, x="total_uploaded", y="document_names", 
                 title="Top 10 Documents Uploaded in AIQ",orientation='h',
                 color_discrete_sequence=['#87CEEB'], text_auto='.2s',
                 labels={"document_names": "Document Name", "total_uploaded": "Uploaded Documents Count"})
    fig.update_layout(xaxis={'categoryorder': 'total descending'})

    return fig

# Update document count by purpose chart AIQ
@app.callback(
    Output('doc-uploaded-counts-purpose-chart-1', 'figure'),
    [Input('year-dropdown-4', 'value'),
     Input('document-names-4-dropdown', 'value'),
     Input('purpose-names-4-dropdown', 'value')]
)
def update_aiq_doc_uploaded_counts_purpose_chart(selected_years_4, selected_doc_4, selected_purpose_4):
    global aiq_data
    
    filtered_data = aiq_data.copy()
    if selected_years_4:
        filtered_data = filtered_data[filtered_data['year'].isin(selected_years_4)]
    if selected_doc_4:
        filtered_data = filtered_data[filtered_data['document_names'].isin(selected_doc_4)]
    if selected_purpose_4:
        filtered_data = filtered_data[filtered_data['purpose'].isin(selected_purpose_4)]

    purpose_wise = filtered_data.groupby('purpose')['total_uploaded'].sum().reset_index()
    purpose_wise = purpose_wise.sort_values(by='total_uploaded', ascending=False).head(20)

    fig = px.bar(purpose_wise, x='purpose', y='total_uploaded', 
                 title='Uploaded Documents Count by Purpose',text_auto='.2s',
                 labels={"purpose": "Purpose", "total_uploaded": "Uploaded Documents Count"},
                 color_discrete_sequence=['#87CEEB'])
    fig.update_traces(text=purpose_wise['total_uploaded'], textposition='outside')

    return fig

# Update document count by month and purpose chart AIQ
@app.callback(
    Output('doc-uploaded-counts-month-name-purpose-documents-chart-1', 'figure'),
    [Input('year-dropdown-4', 'value'),
     Input('document-names-4-dropdown', 'value'),
     Input('purpose-names-4-dropdown', 'value')]
)
def update_aiq_doc_uploaded_counts_month_name_chart(selected_years_4, selected_doc_4, selected_purpose_4):
    global aiq_data
    
    filtered_data = aiq_data.copy()
    if selected_years_4:
        filtered_data = filtered_data[filtered_data['year'].isin(selected_years_4)]
    if selected_doc_4:
        filtered_data = filtered_data[filtered_data['document_names'].isin(selected_doc_4)]
    if selected_purpose_4:
        filtered_data = filtered_data[filtered_data['purpose'].isin(selected_purpose_4)]

    month_wise = filtered_data.groupby('month_name')['total_uploaded'].sum().reset_index()
    # Define the correct chronological order for months
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Convert 'month_name' to a categorical type with the specified order
    month_wise['month_name'] = pd.Categorical(month_wise['month_name'], categories=month_order, ordered=True)

    # Sort the data by the 'month_name' column to ensure it appears in the correct order
    month_wise = month_wise.sort_values('month_name',ascending=False)

    fig = px.bar(month_wise, x='total_uploaded', y='month_name', text_auto='2s',
                 title='Uploaded Documents by Month',
                 labels={"month_name": "Month", "total_uploaded": "Uploaded Documents"},
                 color_discrete_sequence=['#87CEEB'])

    return fig

# Update document count by date of transfer chart
@app.callback(
    Output('doc-uploaded-counts-date-of-transfer-by-doc-chart-1', 'figure'),
    [Input('year-dropdown-4', 'value'),
     Input('document-names-4-dropdown', 'value'),
     Input('purpose-names-4-dropdown', 'value')]
)
def update_aiq_doc_uploaded_counts_by_date_of_transfer_chart(selected_years_4, selected_doc_4, selected_purpose_4):
    global aiq_data
    
    filtered_data = aiq_data.copy()
    if selected_years_4:
        filtered_data = filtered_data[filtered_data['year'].isin(selected_years_4)]
    if selected_doc_4:
        filtered_data = filtered_data[filtered_data['document_names'].isin(selected_doc_4)]
    if selected_purpose_4:
        filtered_data = filtered_data[filtered_data['purpose'].isin(selected_purpose_4)]

    date_wise = filtered_data.groupby('uploaded_date')['total_uploaded'].sum().reset_index()

    fig = px.bar(date_wise, x='uploaded_date', y='total_uploaded',
                 title='Uploaded Documents Count by Date',
                 labels={"uploaded_date": "Uploaded Date", "total_uploaded": "Uploaded Documents Count"},
                 color_discrete_sequence=['#87CEEB'])

    return fig

#---------------------------------------------------------------------------Button Callback---------------------------------------------------------------------------
@app.callback(
    [Output('prod-content', 'style'),
     Output('adr-content', 'style'),
     Output('ade-labelimg-content', 'style'),
     Output('ade-aiq-content', 'style'),
     Output('prod-data-button', 'style'),
     Output('adr-button', 'style'),
     Output('ade-labelimg-button', 'style'),
     Output('ade-aiq-button', 'style')],
    [Input('prod-data-button', 'n_clicks'),
     Input('adr-button', 'n_clicks'),
     Input('ade-labelimg-button', 'n_clicks'),
     Input('ade-aiq-button', 'n_clicks')]
)
def display_page(prod_clicks, adr_clicks, ade_clicks, aiq_clicks):
    ctx = dash.callback_context

    # Define default button style
    default_style = {'background-color': '#87CEEB', 'color': 'white', 'border': 'none', 'border-radius': '5px', 'padding': '10px 20px'}
    # Define active button style
    active_style = {'background-color': '#1E90FF', 'color': 'white', 'border': 'none', 'border-radius': '5px', 'padding': '10px 20px'}

    if not ctx.triggered:
        # Default page (Prod Data visible)
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, \
               active_style, default_style, default_style, default_style

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Determine which button was clicked and update styles accordingly
    if button_id == 'prod-data-button':
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, \
               active_style, default_style, default_style, default_style

    elif button_id == 'adr-button':
        return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, \
               default_style, active_style, default_style, default_style

    elif button_id == 'ade-labelimg-button':
        return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, \
               default_style, default_style, active_style, default_style

    elif button_id == 'ade-aiq-button':
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, \
               default_style, default_style, default_style, active_style

    # Fallback to default page (Prod Data visible)
    return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, \
           active_style, default_style, default_style, default_style


if __name__ == '__main__':
    app.run_server(debug=True)
