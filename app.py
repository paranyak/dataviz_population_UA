import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('./kids_sorted_eng.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', './styles.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()}
    ),
    html.Div(id='click-data')
], style={"width": "90%", "margin": "0 auto"})


@app.callback(
    dash.dependencies.Output('click-data', 'children'),
    [dash.dependencies.Input('graph-with-slider', 'clickData'),
     dash.dependencies.Input('year-slider', 'value')])
def display_click_data(clickData, year):
    colors = ['#F8EFBA', '#ffdd59', '#F97F51', '#ff5e57', '#ef5777', '#B33771', '#82589F', '#182C61', '#58B19F', '#0be881']
    value_city = []
    value_village = []

    if clickData:
        filtered_df = df[df.year == year]
        filtered_region = filtered_df[filtered_df.region == clickData['points'][0]['x']]
        labels = list(filtered_region.age)
        for i in range(len(filtered_region.city)):
            value_city.append(int((list(filtered_region.city)[i]).replace(" ", "")))
            value_village.append(int((list(filtered_region.village)[i]).replace(" ", "")))
        print("VALUES: ", value_city, value_village, " labels : ", labels)

        return html.Div([
            html.H5(['Amount of mothers in ' + str(year) + ' year in ' + clickData['points'][0]['x'] + ' obl.'],
                    style={"margin": "40px auto 0 auto",
                    "text-align": "center"}),
            html.Div([dcc.Graph(
                className='six columns',
                figure={
                    'data': [{
                        'values': value_city,
                        'labels': labels,
                        'sort': False,
                        'hoverinfo': 'label+percent+value',
                        'textfont': dict(size=15),
                        'textposition' : 'inside',
                        'marker': dict(colors=colors, line=dict(color='#000000', width=1)),
                        "hole": .3,
                        'type': 'pie',
                    }],
                    'layout': {'title': 'In city'}
                }
            ),
            dcc.Graph(
                className='six columns',
                figure={
                    'data': [{
                        'values': value_village,
                        'labels': labels,
                        'sort': False,
                        'hoverinfo':'label+percent+value',
                        'textfont': dict(size=15),
                        'textposition': 'inside',
                        'marker': dict(colors=colors, line=dict(color='#000000', width=1)),
                        "hole": .3,
                        'type': 'pie',
                    }],
                    'layout': {'title': 'In village'}
                }
            )
        ], className='column', style={"margin-left": "0"})])


@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    traces = []
    areas = []
    amount_city = []
    amount_village = []
    for i in filtered_df.region.unique():
        df_by_continent = filtered_df[filtered_df['region'] == i]
        local_amount = 0
        for j in df_by_continent['city']:
            local_amount += int(j.replace(" ", ""))
        amount_city.append(local_amount)
        local_amount = 0
        for j in df_by_continent['village']:
            local_amount += int(j.replace(" ", ""))
        amount_village.append(local_amount)
        areas.append(i)
    traces.append(go.Bar(
        x=areas,
        y=amount_city,
        name="city",
        marker=dict(
            color='#F97F51',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
    ))
    traces.append(go.Bar(
        x=areas,
        y=amount_village,
        name="village",
        marker=dict(
            color='#B33771',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
    ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'region'},
            yaxis={'title': 'amount'},
            margin={'l': 100, 'b': 100, 't': 30, 'r': 100},
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
