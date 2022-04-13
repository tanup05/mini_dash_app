from pydoc import classname
import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.graph_objects as go
import sqlite3
import sqlvalidator
import os

app = dash.Dash(__name__)
server = app.server
#--------------------------------DATABASE CONNECTIVITY--------------------------------------------------

con = sqlite3.connect('./data/moody2022_new.db', check_same_thread=False)
df = pd.read_sql_query("SELECT * FROM moody2022_new", con)

#----------------------------------APP LAYOUT------------------------------------------------

app.layout = html.Div([
    
    html.Div([
        html.H4("Dashboard")
    ], className = 'header', ),

    html.Div([
        dcc.Input(
        id = 'my_txt_input',
        type = 'text',
        name = 'text',
        debounce = True,
        placeholder="SELECT * FROM moody2022_new;",
        style = {'border-radius': '5px', 'background-color': '#f0fff0', 'width' : '100%', 'height': 100, 
                'align':'center', 'align-items':'center', 'justify-content': 'center'}
    )
    ]),

    html.Br(),
    html.Div([
        dcc.RadioItems(
            id = 'radio_input',
            options={
                'Mean': 'Mean',
                'Standard Deviation': 'Mean & Standard Deviation',
                'Median': 'Median'
            },
            value  = 'Median',
            inline = True,
            style = {'color' : '#060225'}
        )
    ], style = dict(width = '100%', justifyContent = 'center')),
    html.Br(),
    html.Div([
        dcc.Graph(
        id= 'div_output',
        style = {'width' : '100%', 'align':'center', 'border-radius': '5px'}
    )
    ])
], style = dict(fontfamily = 'Consolas', backgroundcolor = 'rgb(225, 220, 220)', color = 'rgb(8, 1, 68)', fontsize = '2.5em'))

#-------------------------------------CALLBACKS-----------------------------------------------------------

@app.callback(
    Output('div_output', 'figure'),
    Input('my_txt_input', 'value'),
    Input('radio_input', 'value')
)

def update_graph(txt_inserted, radio_select):

    if not txt_inserted:
        txt_inserted = 'SELECT * FROM MOODY2022_NEW;'
    else:
        txt_inserted = txt_inserted

    try:
        query_check = sqlvalidator.parse(txt_inserted)
        query_check.is_valid()
    except:
        print(query_check.errors)

    df1 = pd.read_sql_query(txt_inserted.lower(), con)

    fig = go.Figure()

    if radio_select=='Standard Deviation':
        fig.add_trace(go.Box(
            y = df['SCORE'], x = df['GRADE'],
            name = 'Depicts overall data',
            marker_color = 'olive',
            notched = True,
            boxmean = 'sd'
            #marker_color_line = 'midnightblue'
        ))
        fig.add_trace(go.Box(
            y = df1['SCORE'], x = df1['GRADE'],
            name = 'Depicts Sliced data',
            marker_color = 'orchid',
            notched = True,
            boxmean = 'sd'
            #marker_color_line = 'magenta'
        ))
    elif radio_select == 'Mean':
        fig.add_trace(go.Box(
            y = df['SCORE'], x = df['GRADE'],
            name = 'Depicts overall data',
            marker_color = 'olive',
            notched = True,
            boxmean = True
            #marker_color_line = 'midnightblue'
        ))
        fig.add_trace(go.Box(
            y = df1['SCORE'], x = df1['GRADE'],
            name = 'Depicts Sliced data',
            marker_color = 'orchid',
            notched = True,
            boxmean = True
            #marker_color_line = 'magenta'
        ))
    else:
        fig.add_trace(go.Box(
            y = df['SCORE'], x = df['GRADE'],
            name = 'Depicts overall data',
            marker_color = 'olive',
            notched = True
            #marker_color_line = 'midnightblue'
        ))
        fig.add_trace(go.Box(
            y = df1['SCORE'], x = df1['GRADE'],
            name = 'Depicts Sliced data',
            marker_color = 'orchid',
            notched = True
            #marker_color_line = 'magenta'
        ))

    fig.update_layout(
        title = 'Distribution of Scores by Grade for all',
        yaxis_title = 'Scores (out of 100)',
        xaxis_title = 'Letter Grade',
        boxmode = 'group',
        margin = dict(l=50, r=50, t=50, b=50),
        paper_bgcolor = 'linen',
        plot_bgcolor = 'honeydew'
    )
    fig.update_xaxes(categoryorder = 'category ascending')

    #fig = px.box(df, x = 'GRADE', y = txt_inserted, color = 'TEXTING_IN_CLASS',
    #            title = 'Box Plots')
    return (fig)

# close connection
con.commit()

# server.secret_key = os.environ.get(‘SECRET_KEY’, ‘my-secret-key’)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
