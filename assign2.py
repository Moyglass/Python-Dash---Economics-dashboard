# -*- coding: utf-8 -*-
"""
The code used here is an edited version of the dashboard example from moodle
Most of the changes made help restrict certain columns being used for some variables
also changes to data inputs, themes used etc...

Student No.: A00304383
"""

import pandas as pd
import dash
from dash import dash_table
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px

# Load data from CSV file
data = pd.read_csv('C:/Users/User/Desktop/data2.csv') 

# Create Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# Define layout
controls = dbc.Card(
    [
        html.Div(
            [
                html.H4("Visualisation controls", className="card-title"),
                html.P(
                    "Line graph, Bar chart or scatterplot",
                    className="card-text",
                ),
               
            ]
        ),
        html.Div(
            [
                dbc.Label("X variable"),
                dcc.Dropdown(
        id='x-axis',
        options=[{'label': 'Year', 'value': 'Year'}],
        value='Year',style={'color':'black'}#LOAD Year TO X AXIS WHEN LOADING DASHBOARD
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Y variable"),
                dcc.Dropdown(
        id='y-axis',
        options=[{'label': col, 'value': col} for col in data.columns[1:8]],
        value='GDP (current US$)',style={'color':'black'}#LOAD GDP TO Y AXIS WHEN LOADING DASHBOARD
                ),
            ]
        ),
          html.Div(
            [
                dbc.Label("Z variable"),
                dcc.Dropdown(
        id='z-axis',
        options=[{'label': col, 'value': col} for col in data.columns[1:8]],
        value='Unemployment, total (% of total labor force) (national estimate)',style={'color':'black'}
                ),
            ]
        ),
        html.Div(
    [
        dbc.Label("Graph type"),
        dcc.Dropdown(
            id='graph-type',
            options=[{'label': 'Line chart', 'value': 'line'},
                     {'label': 'Bar chart', 'value': 'bar'},
                     {'label': 'Scatter plot', 'value': 'scatter'}],
            value='line',style={'color':'black'}
        ),
           ]
),


    ],
    body=True,
style={'border-style': 'dotted',
  'border-color': 'red'})

controls2 = dbc.Card(
    [
        html.Div(
            [
                html.H4("Visualisation controls", className="card-title"),
                html.P(
                    "Sunburst chart and Treemap",
                    className="card-text",
                ),
               
            ]
        ),
         html.Div(
            [
                dbc.Label("Year"),
                dcc.Dropdown(
                    id="hierarchy-dropdown",
                    options=[
                        {"label": col, "value": col} for col in data.columns[[0]]],
                    value="Year",style={'color':'black'}
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Value"),
                dcc.Dropdown(
                    id="value-dropdown",
                    options=[{"label": col, "value": col} for col in data.columns[[3, 6, 8]]],
                    value="Inflation %",style={'color':'black'}
                ),
            ]
        ),

           ],
           body=True,
       style={'border-style': 'dotted',
         'border-color': 'red'})

app.layout = dbc.Container(
    [
        html.H1("Philippines economic dashboard",style={'text-align': 'center'}),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=6),#ADDS GRAPHS TO DASHBOARD
                dbc.Col(dcc.Graph(id='plot', className='plot',style={'margin-top': '30px'}), md=6),
                dbc.Col(controls2, md=6),
                dbc.Col(dcc.Graph(id="sunburst-chart", className="sunburst-chart",style={'margin-top': '25px','margin-bottom': '25px'}), md=6),
                dbc.Col(dcc.Graph(id="treemap-chart", className="treemap-chart",style={'margin-top': '25px','margin-bottom': '25px'}), md=6),
                dbc.Col(dash_table.DataTable(
            id='data-table',
            columns=[{'name': col, 'id': col} for col in data.columns],
            data=data.to_dict('records'), page_size=14,
        style_table={'overflowX': 'auto'},
             style_cell={
        'height': 'auto',
        # all three widths are needed
        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
        'whiteSpace': 'normal'
    },style_data={'color':'black'},style_header={'color':'black'}),md=12)
            ],
            align="center",
        ),
    ],
    fluid=True,
)

# Update plot when dropdowns are changed
@app.callback(
    dash.dependencies.Output('plot', 'figure'),
    [dash.dependencies.Input('x-axis', 'value'),
     dash.dependencies.Input('y-axis', 'value'),
     dash.dependencies.Input('z-axis', 'value'),
     dash.dependencies.Input('graph-type', 'value')])
def update_plot(x_col, y_col,z_col, graph_type):
    if graph_type == 'line':
        fig = px.line(data, x=x_col, y=y_col, markers=True, title='Line Graph')
        fig.update_layout(
        plot_bgcolor='#F8F9FA',
        paper_bgcolor='#343A40',
        font=dict(color='white')
    )
    elif graph_type == 'bar':
        fig = px.bar(data, x=x_col, y=y_col, title='Barchart')
        fig.update_layout(
        plot_bgcolor='#F8F9FA',
        paper_bgcolor='#343A40',
        font=dict(color='white')
    )
    elif graph_type == 'scatter':
        fig = px.scatter(data, x=x_col, y=y_col, size=y_col, color=z_col, log_x=True, size_max=60, title='Scatterplot')
        fig.update_layout(
        plot_bgcolor='#F8F9FA',
        paper_bgcolor='#343A40',
        font=dict(color='white')
    )
    return fig


@app.callback(
    dash.dependencies.Output("sunburst-chart", "figure"),
    [
        dash.dependencies.Input("hierarchy-dropdown", "value"),
        dash.dependencies.Input("value-dropdown", "value"),
    ],
)
def update_sunburst_chart(hierarchy_col, value_col):
    fig = px.sunburst(
        data,
        path=[value_col, hierarchy_col],
        values=value_col,
        color=hierarchy_col,
        color_continuous_scale=px.colors.qualitative.Alphabet,
        title='Sunburst Graph',
        )
    fig.update_layout(
    plot_bgcolor='#F8F9FA',
    paper_bgcolor='#343A40',
    font=dict(color='white')
)
    return fig


@app.callback(
        dash.dependencies.Output("treemap-chart", "figure"),
        [
        dash.dependencies.Input("hierarchy-dropdown", "value"),
        dash.dependencies.Input("value-dropdown", "value"),
    ],
)
def update_treemap_chart(hierarchy_col, value_col):
    fig = px.treemap(data, path=[value_col, hierarchy_col], values=value_col,
                  color=hierarchy_col, 
                  color_continuous_scale='RdBu',
                  title='Treemap')
    fig.update_layout(
    plot_bgcolor='#F8F9FA',
    paper_bgcolor='#343A40',
    font=dict(color='white')
)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)