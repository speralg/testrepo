# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
print(spacex_df.columns)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = list(spacex_df['Launch Site'].unique())
launch_sites.append("All Sites")
def Class(value):
    if value == 0:
        return "failure"
    else:
        return "success"    
spacex_df["class1"] = spacex_df["class"].map(Class) 

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                html.P("Select Launch Site:"),
                                html.Div([
                                    #html.Label("Select Launch Site:"),
                                    dcc.Dropdown(
                                    id='site-dropdown',
                                    options=launch_sites,
                                    value='All Sites',
                                    placeholder='Select a Launch Site'
                                    )
                                ]),
                                
                                                                    
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                html.Div([
                                    dcc.RangeSlider(
                                    min=min_payload, 
                                    max=max_payload, 
                                    step=2500,
                                    value=[0, 2500],    
                                    id='payload-slider'
                                    )
                                ]),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))

def update_pie_chart(selected_launch_site):
    if selected_launch_site == 'All Sites':
        # Filter the data for success launches
        success_data = spacex_df[spacex_df['class'] == 1]

        # Plot Pie chart 
        # use groupby to create relevant data for plotting
        data = success_data.groupby('Launch Site')['class'].count().reset_index()                          
        #pie_chart = dcc.Graph(
        figure=px.pie(data, values='class', names='Launch Site', title="Total Success Launches By Site")#)

        # return pie_chart
        return figure

    else:                              
        # Filter the data for launch site
        launch_site_data = spacex_df[spacex_df['Launch Site'] == selected_launch_site]

        # Plot Pie chart 
        # use groupby to create relevant data for plotting
        count = launch_site_data['class1'].value_counts()
        print(count)
        count_df = pd.DataFrame(count).reset_index()
        print(count_df)
        count_df.columns = ['class1', 'count']
        print(count_df)

        #pie_chart = dcc.Graph(
        figure=px.pie(count_df, values='count', names='class1', title='Total Launches By "{}"'.format(selected_launch_site))#)

        #return pie_chart
        return figure

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider', component_property='value')])

def update_scatter_chart(selected_launch_site, payload_mass_range):
    
    # Filter the data for PayLoad
    print(payload_mass_range[0])
    print(payload_mass_range[1])
    min_range = float(payload_mass_range[0])
    max_range = float(payload_mass_range[1])
    payload_range_data = spacex_df.query("`Payload Mass (kg)` >= @min_range and `Payload Mass (kg)` <= @max_range")
    
    if selected_launch_site == 'All Sites':

        # Plot Scatter chart 
        #scatter_chart = dcc.Graph(
        figure=px.scatter(payload_range_data, x='Payload Mass (kg)', y='class1', color="Booster Version Category", title="Correlation between Payload and Success for all Sites")#)

        #return scatter_chart
        return figure
    else:                              
        # Filter the data for launch site
        launch_site_data = payload_range_data[payload_range_data['Launch Site'] == selected_launch_site]

        # Plot Scatter chart 
        #scatter_chart = dcc.Graph(
        figure=px.scatter(launch_site_data, x='Payload Mass (kg)', y='class1' , color="Booster Version Category", title='Correlation between Payload and Success for "{}"'.format(selected_launch_site))#)

        #return scatter_chart
        return figure




# Run the app
if __name__ == '__main__':
    app.run_server()
