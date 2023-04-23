# Getting Started with Plotly Dash

## APIC Energy Hackathon 2023

> by Ildar Akhmetov (ildar@ualberta.ca)*

### Set up the ReplIt environment

Go to <https://replit.com/@ildarakhmetov0/PlotlyDashWorkshopDev>.

Create a ReplIt account if you don't have one.

Click on the **"Fork"** button to create your own copy of the project.

### Version 1: Hello World

You should see the `main.py` file open in the editor.

Click on the **"Run"** button to start the server.

You'll see the following message in the console:

```txt
Dash is running on http://0.0.0.0:80/

 * Serving Flask app 'main'
 * Debug mode: on
```

You'll also see the Webview open in a new tab. Copy the URL from the address bar and paste it into a new browser tab.

### Version 2: Loading Data

Let's read the data. We'll be using the [Data on Energy by Our World in Data](https://github.com/owid/energy-data) dataset.

```python
# Load the data
df = pd.read_csv(
    'https://nyc3.digitaloceanspaces.com/owid-public/data/energy/owid-energy-data.csv'
)
```

We will filter the data by country. Let's compare the coal production in Canada and the China.

```python
df_filtered = df[df['country'].isin(['Canada', 'China'])]
```

Now, let's create a line chart that shows the coal production in Canada and China over time.

```python
# Create a line chart
fig = px.line(df_filtered, x='year', y='coal_prod_per_capita', color='country')
```

Finally, we need to add the chart to the app layout.

```python
app.layout = dbc.Container(
    [
        dcc.Markdown(children='APIC Hackathon 2023 Dashboard'),
        dbc.Row([dbc.Col([dcc.Graph(figure=fig)], width=8)]),
    ]
)
```

Run the app to see the result.

### Version 3: Adding Interactivity

Now, let's add some interactivity to the chart. Let's add a dropdown menu that allows the user to select the country.

First, we'll remove the `df_filtered` variable and the `fig` variable. We don't need them anymore.

Then, we'll add a dropdown menu to the app layout. Add the following code fragment between the `dcc.Markdown` and the `dbc.Row` lines.

```python
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
```

Here, we create a dropdown menu with the `dcc.Dropdown` component. We set the `id` to `country-dropdown` so that we can refer to it in the callback function. We set the `options` to the list of unique countries in the dataset. We set the `multi` parameter to `True` so that the user can select multiple countries. Finally, we set the `value` to the list of countries that we want to be selected by default.

Next, we'll update the `app.layout` variable. The row referred to the figure `fig` that we removed. Now, it'll refer to a figure that we'll create on the fly. 

In the following line

```python
dbc.Row([dbc.Col([dcc.Graph(figure=fig)], width=8)]),
```

we'll replace `fig` with `dcc.Graph(id='line-chart')`. This will create a placeholder for the figure. We'll create the figure in the callback function.

Next, we'll add a callback function that will create the figure based on the selected country.

```python
@app.callback(Output('line-chart', 'figure'), Input('country-dropdown', 'value'))
def update_graph(countries_selected):
    df_filtered = df[df.country.isin(countries_selected)]
    fig = px.line(df_filtered, x='year', y='coal_prod_per_capita', color='country')
    return fig
```

The function takes the list of countries selected in the dropdown menu as an input. It filters the data by the selected countries and creates a line chart. Finally, it returns the figure.

Take a moment to understand the `@app.callback` decorator. It tells Dash that this function is a callback function. The `Output` and `Input` parameters tell Dash which components the function depends on and which components it updates.

> What is a callback function? A callback function is a function that is called when an event occurs. In this case, the event is the user selecting a country in the dropdown menu.

Run the app to see the result!

### What's Next?

You can find the final version of the app here: <https://github.com/ildarakhmetov/energy-hackathon-2023-tutorial/blob/main/final_version.py>.

Explore the Plotly Dash documentation to learn more about the components and the layout: <https://dash.plotly.com/>.
