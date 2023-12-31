from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__)

app.layout = html.Div([
  html.Div([
    html.H1('Dropdown Div', style={'textAlign':'center'}),
    dcc.Dropdown(
        id='dropdown-selection',
        options=[{'label': country, 'value': country} for country in df['country'].unique()],
        value='Canada'  # default value select in drop
    ),
    dcc.Graph(id='graph-content')
   ], style={'width': '48%', 'display': 'inline-block'}),

  html.Div([
    html.H1("Checklist Div"),
    dcc.Checklist(
        id='category-checklist',
        options=[{'label': category, 'value': category} for category in df['continent'].unique()],
        value=df['continent'].unique()  # all value select default
        #,labelStyle={'display': 'block'}  
    ),
    dcc.Graph(id='bar-graph')
  ], style={'width': '48%', 'display': 'inline-block'}),
  
  html.Div([
	html.H1("Slider"),
	dcc.Slider(
        id='slider',
        min=1990, #df['year'].min()
        max=2007, #df['year'].max()
        step=2,
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
    ),
    dcc.Graph(id='scatter-plot')
  ], style={'width': '48%', 'display': 'inline-block'})
])

@app.callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country == value]
    return px.line(dff, x='year', y='pop')

@app.callback(
    Output('bar-graph', 'figure'),
    Input('category-checklist', 'value')
)
def update_bar_graph(selected_categories):
    filtered_df = df[df['continent'].isin(selected_categories)]
    fig = px.bar(filtered_df, x='year', y='gdpPercap', color='continent',
    labels={'year': 'Year', 'gdpPercap': 'GDP per Capita'})
    return fig

@app.callback(
    Output('scatter-plot', 'figure'),
    Input('slider', 'value')
)

def update_scatter_plot(selected_year):
    filtered_df = df[df['year'] == selected_year]

    fig = px.scatter(
        filtered_df,
        x='gdpPercap',
        y='lifeExp',
        size='pop',
        color='continent',
        hover_name='country',
        log_x=True,
        size_max=8
        #,title=f'Scatter Plot for Year {selected_year}'
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
