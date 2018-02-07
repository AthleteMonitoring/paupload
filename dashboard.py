import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import pandas as pd
import numpy as np
import plotly

app = dash.Dash()

app.scripts.config.serve_locally = True
# app.css.config.serve_locally = True

df = pd.read_csv(
    'data_example.csv'
)

app.layout = html.Div([
    html.H4('6 Nations Dummy Data'),
    dt.DataTable(
        rows=df.to_dict('records'),

        # optional - sets the order of columns
        columns=sorted(df.columns),
        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id='datatable-df'
    ),
    html.Div(id='selected-indexes'),
    dcc.Graph(
        id='graph-df'
    ),
], className="container")


@app.callback(
    Output('datatable-df', 'selected_row_indices'),
    [Input('graph-df', 'clickData')],
    [State('datatable-df', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(
    Output('graph-df', 'figure'),
    [Input('datatable-df', 'rows'),
     Input('datatable-df', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    fig = plotly.tools.make_subplots(
        rows=5, cols=3,
        subplot_titles=('Wk1_RPE-match', 'Wk1_Mins_Played', 'Wk1_Total_Load',
                        'Wk2_RPE-match', 'Wk2_Mins_Played', 'Wk2_Total_Load',
                        'Wk3_RPE-match', 'Wk3_Mins_Played', 'Wk3_Total_Load',
                        'Wk4_RPE-match', 'Wk4_Mins_Played', 'Wk4_Total_Load',
                        'Wk5_RPE-match', 'Wk5_Mins_Played', 'Wk5_Total_Load',
                        ),
        shared_xaxes=True)
    marker = {'color': ['#0074D9']*len(dff)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#FF851B'
    fig.append_trace({
        'x': dff['Player_ID'],
        'y': dff['Wk1_RPE-match'],
        'type': 'bar',
        'marker': marker
    }, 1, 1)
    fig.append_trace({
        'x': dff['Player_ID'],
        'y': dff['Wk1_Mins_Played'],
        'type': 'bar',
        'marker': marker
    }, 1, 2)
    fig.append_trace({
        'x': dff['Player_ID'],
        'y': dff['Wk1_Total_Load'],
        'type': 'bar',
        'marker': marker
    }, 1, 3)
    fig.append_trace({
        'x': dff['Player_ID'],
        'y': dff['Wk2_RPE-match'],
        'type': 'bar',
        'marker': marker
    }, 2, 1)
    fig.append_trace({
        'x': dff['Player_ID'],
        'y': dff['Wk2_Mins_Played'],
        'type': 'bar',
        'marker': marker
    }, 2, 2)
    fig.append_trace({
        'x': dff['Player_ID'],
        'y': dff['Wk2_Total_Load'],
        'type': 'bar',
        'marker': marker
    }, 2, 3) 
    fig.append_trace({
        'x': dff['Player_ID'],
        'y': dff['Wk3_RPE-match'],
        'type': 'bar',
        'marker': marker
    }, 3, 1)
    fig.append_trace({
        'x': dff['Player_ID'],
        'y': dff['Wk3_Mins_Played'],
        'type': 'bar',
        'marker': marker
    }, 3, 2)
    fig.append_trace({
        'x': dff['Player_ID'],
        'y': dff['Wk3_Total_Load'],
        'type': 'bar',
        'marker': marker
    }, 3, 3) 
    fig.append_trace({
        'x': dff['Player_ID'],
        'y': dff['Wk4_RPE-match'],
        'type': 'bar',
        'marker': marker
    }, 4, 1)
    fig.append_trace({
        'x': dff['Player_ID'],
        'y': dff['Wk4_Mins_Played'],
        'type': 'bar',
        'marker': marker
    }, 4, 2)
    fig.append_trace({
        'x': dff['Player_ID'],
        'y': dff['Wk4_Total_Load'],
        'type': 'bar',
        'marker': marker
    }, 4, 3) 
    fig.append_trace({
        'x': dff['Player_ID'],
        'y': dff['Wk5_RPE-match'],
        'type': 'bar',
        'marker': marker
    }, 5, 1)
    fig.append_trace({
        'x': dff['Player_ID'],
        'y': dff['Wk5_Mins_Played'],
        'type': 'bar',
        'marker': marker
    }, 5, 2)
    fig.append_trace({
        'x': dff['Player_ID'],
        'y': dff['Wk5_Total_Load'],
        'type': 'bar',
        'marker': marker
    }, 5, 3)
    fig['layout']['showlegend'] = False
    fig['layout']['height'] = 1200
    fig['layout']['margin'] = {
        'l': 40,
        'r': 10,
        't': 100,
        'b': 200
    }
    fig['layout']['yaxis3']['type'] = 'log'
    return fig


app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

if __name__ == '__main__':
    app.run_server(debug=True)
