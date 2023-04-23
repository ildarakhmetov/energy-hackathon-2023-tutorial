# Loading data

from dash import Dash, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Data
df = pd.read_csv(
    'https://nyc3.digitaloceanspaces.com/owid-public/data/energy/owid-energy-data.csv'
)

# Instantiate the App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App Layout
app.layout = dbc.Container(
    [
        dcc.Markdown(children='APIC Hackathon 2023 Dashboard'),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id='country-dropdown',
                            options=[x for x in df.country.unique()],
                            multi=True,
                            value=['Canada', 'China'],
                        )
                    ],
                    width=8,
                )
            ]
        ),
        dbc.Row([dbc.Col([dcc.Graph(id="line-chart")], width=8)]),
    ]
)


# Configure Callback
@app.callback(Output('line-chart', 'figure'), Input('country-dropdown', 'value'))
def update_graph(countries_selected):
    df_filtered = df[df.country.isin(countries_selected)]
    fig = px.line(df_filtered, x='year', y='coal_prod_per_capita', color='country')
    return fig


# Run the App
if __name__ == '__main__':
    app.run_server(debug=True)
