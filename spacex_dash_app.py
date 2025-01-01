# Import required libraries
import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Read the dataset
spacex_df = pd.read_csv('/Users/user/Downloads/spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Launch Site Dropdown
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS SLC 40', 'value': 'CCAFS SLC 40'},
                     {'label': 'VAFB SLC 4E', 'value': 'VAFB SLC 4E'},
                     {'label': 'KSC LC 39A', 'value': 'KSC LC 39A'},
                     {'label': 'LC-40', 'value': 'LC-40'}
                 ],
                 value='ALL',  # Default value
                 placeholder="Select a Launch Site here",
                 searchable=True),
    html.Br(),
    
    # Pie chart for success/failure rate
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    
    # Payload range slider
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                    marks={0: '0', 10000: '10000'}, value=[min_payload, max_payload]),
    
    # Scatter chart for success vs payload
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callback for success-pie-chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
                     names='Launch Site', 
                     title='Launch Success Count for All Sites')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', 
                     title=f'Success vs. Failure for {entered_site}')
    return fig

# Callback for success-payload-scatter-chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def get_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df
    min_payload_value, max_payload_value = payload_range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= min_payload_value) &
                              (filtered_df['Payload Mass (kg)'] <= max_payload_value)]
    
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
    
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                     color='Booster Version Category',
                     title=f'Success vs Payload Mass for {entered_site}' if entered_site != 'ALL' else 'Success vs Payload Mass for All Sites')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
