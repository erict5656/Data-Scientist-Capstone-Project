# Import necessary libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Create a sample dataframe similar to spacex_df
# (replace this with your actual spacex_df DataFrame)
spacex_df = pd.read_csv("spacex_dash_app.csv")

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    # Dropdown for selecting launch sites
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center'}),
    
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    
    # Pie chart for launch success counts
    html.Div(dcc.Graph(id='success-pie-chart')),
    
    # RangeSlider for selecting payload range
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={i: f'{i} Kg' for i in range(0, 10001, 1000)},
        value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]
    ),
    
    # Scatter plot for payload vs launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callback for the pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
                     names='Launch Site', 
                     title='Total Success Launches for All Sites')
        return fig
    else:
        # Filter data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_counts = filtered_df['class'].value_counts()
        fig = px.pie(values=success_counts, 
                     names=success_counts.index, 
                     title=f'Total Success vs Failure for site {entered_site}')
        return fig

# Callback for the scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter(selected_site, selected_payload):
    low, high = selected_payload
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    
    if selected_site == 'ALL':
        fig = px.scatter(
            filtered_df, x='Payload Mass (kg)', y='class', 
            color='Booster Version Category', 
            title='Payload vs. Outcome for All Sites')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(
            filtered_df, x='Payload Mass (kg)', y='class', 
            color='Booster Version Category', 
            title=f'Payload vs. Outcome for {selected_site}')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
