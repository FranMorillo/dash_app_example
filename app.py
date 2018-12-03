
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import flask

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
df = pd.read_csv('nama_10_gdp_1_Data.csv', error_bad_lines = False, engine = 'python', na_values = [':', 'NaN'])
df.groupby('GEO').size()
df=df[~df.GEO.str.contains("Euro")]
df=df.drop(columns=['Flag and Footnotes'])
df=df.reset_index(drop=True)
df=df.rename(index=str, columns={"TIME": "Year", "GEO": "Country",'UNIT':'Unit','NA_ITEM':'Indicator Name','Value':'Value'})

df['Indicator'] = df['Indicator Name'] + ' (' + df['Unit'] + ')'

app = dash.Dash()
available_indicators = df['Indicator'].unique()
available_countries = df['Country'].unique()

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id = 'xaxis-column1',
                options = [{'label': i, 'value': i} for i in available_indicators],
                value = available_indicators[0],
            ),
            dcc.RadioItems(
                id = 'xaxis-type1',
                options = [{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value = 'Linear',
                labelStyle = {'display': 'inline-block'},
                style = {'font-size': '10px', 'font-family': 'Arial, Helvetica, sans-serif'}
            )
        ],
        style = {'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id = 'yaxis-column1',
                options = [{'label': i, 'value': i} for i in available_indicators],
                value = available_indicators[1],
            ),
            dcc.RadioItems(
                id = 'yaxis-type1',
                options = [{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value = 'Linear',
                labelStyle = {'display': 'inline-block'},
                style = {'font-size': '10px', 'font-family': 'Arial, Helvetica, sans-serif'}
            )
        ], style = {'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id = 'indicator-graphic1'),
    html.Div([
        dcc.Slider(
            id = 'year--slider1',
            min = df['Year'].min(),
            max = df['Year'].max(),
            value = df['Year'].max(),
            step = None,
            marks = {str(year): str(year) for year in df['Year'].unique()}
        )
    ], 
        style = {'margin' : '10px 40px'}
    ),
    html.Div([
    ], 
        style = {'margin': '50px 10px 20px 10px', 'background-color': 'black', 'height': '2px'}
    ),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id = 'country2',
                options = [{'label': i, 'value': i} for i in available_countries],
                value = available_countries[0],
            )
        ],
        style = {'width': '48%', 'display': 'inline-block', 'height': '130px'}),

        html.Div([
            dcc.Dropdown(
                id = 'yaxis-column2',
                options = [{'label': i, 'value': i} for i in available_indicators],
                value = available_indicators[0],
            )
        ],
        style = {'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ], 
        style = {'margin-top': '20px'}
    ),

    dcc.Graph(id = 'indicator-graphic2')
])

@app.callback(
    dash.dependencies.Output('indicator-graphic1', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('xaxis-type1', 'value'),
     dash.dependencies.Input('yaxis-type1', 'value'),
     dash.dependencies.Input('year--slider1', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['Year'] == year_value]
    
    return {
        'data': [go.Scatter(
            x = dff[dff['Indicator'] == xaxis_column_name]['Value'],
            y = dff[dff['Indicator'] == yaxis_column_name]['Value'],
            text = dff[dff['Indicator'] == yaxis_column_name]['Country'],
            mode = 'markers',
            marker = {
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis = {
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis = {
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin = {'l': 40, 'b': 40, 't': 40, 'r': 40},
            hovermode = 'closest'
        )
    }

@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('country2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value')])

def update_graph(country_name, yaxis_column_name):    
    
    return {
        'data': [go.Scatter(
            x = df[(df['Country'] == country_name) & (df['Indicator'] == yaxis_column_name)]['Year'].values,
            y = df[(df['Country'] == country_name) & (df['Indicator'] == yaxis_column_name)]['Value'].values,
            mode = 'lines'
        )],
        'layout': go.Layout(
            yaxis = {
                'title': yaxis_column_name,
                'titlefont': {'size': 10},
                'type': 'linear'
            },
            margin = {'l': 40, 'b': 40, 't': 40, 'r': 40},
            hovermode = 'closest'
        )
    }

if __name__ == '__main__':
    app.run_server()


# In[2]:


get_ipython().run_line_magic('tb', '')

