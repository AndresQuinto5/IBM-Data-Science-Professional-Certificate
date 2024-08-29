#!/usr/bin/env python
# coding: utf-8

import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
# app.title = "Automobile Statistics Dashboard"

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [i for i in range(1980, 2024)]

# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}),
    
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select Statistics'
        )
    ]),
    
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='dropdown-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=2024
        )
    ]),
    
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'flex': '10px'})
    ])
])

@app.callback(
    Output('dropdown-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def disable_year(report_value):
    return report_value == "Recession Period Statistics"

@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'), Input('dropdown-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
        # Verificar si la columna 'Unemployment_Rate' existe
        if 'Unemployment_Rate' in recession_data.columns:
            # Crear gráfico usando la columna 'Unemployment_Rate'
            unemp_data = recession_data.groupby(['Unemployment_Rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
            R_chart4 = dcc.Graph(
                figure=px.bar(unemp_data,
                    x='Unemployment_Rate',
                    y='Automobile_Sales',
                    color='Vehicle_Type',
                    title='Effect of Unemployment Rate on Vehicle Type and Sales')
            )
        else:
            # Mostrar mensaje de error si la columna no existe
            R_chart4 = html.Div("Error: 'Unemployment_Rate' column not found in data", style={'color': 'red'})

        # Aquí irían los otros gráficos que no necesitan 'Unemployment_Rate'
        # ...

        return [
            # Añadir los otros gráficos aquí
            html.Div(children=R_chart4)
        ]
    
    elif input_year and selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]

        # Crear y mostrar gráficos para las estadísticas anuales
        # ...

        return [
            # Añadir los gráficos aquí
        ]
    
    else:
        return None

if __name__ == '__main__':
    app.run_server(debug=True)
