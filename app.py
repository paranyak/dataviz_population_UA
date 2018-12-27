import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('./kids_sorted_eng.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = ['#F8EFBA', '#ffdd59', '#F97F51', '#ff5e57', '#ef5777', '#B33771', '#82589F', '#182C61', '#58B19F', '#0be881']

app.layout = html.Div([html.Div([
    html.Div([dcc.Graph(id='graph-with-slider')], style={"width": "60%"}),
    html.Div(id='click-data', style={"width": "35%", "height": "800px"})
], style={"display": "flex", "justify-content": "center", "align-content": "center", "margin-bottom": "20px"}),

    html.Div([dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): {'label': str(year), 'style': {"font-family": 'Courier New, monospace', "font-size": 16, "color": '#7f7f7f'}} for year in df['year'].unique()},
    )], style={"width": "90%", "margin": "0 auto"})])


@app.callback(
    dash.dependencies.Output('click-data', 'children'),
    [dash.dependencies.Input('graph-with-slider', 'clickData'),
     dash.dependencies.Input('year-slider', 'value')])
def display_click_data(clickData, year):
    value_city = []
    value_village = []

    if clickData:
        filtered_df = df[df.year == year]
        filtered_region = filtered_df[filtered_df.region == clickData['points'][0]['y']]
        labels = list(filtered_region.age)
        for i in range(len(filtered_region.city)):
            value_city.append(int((list(filtered_region.city)[i]).replace(" ", "")))
            value_village.append(int((list(filtered_region.village)[i]).replace(" ", "")))
        print("VALUES: ", value_city, value_village, " labels : ", labels)

        traces = []
        for i in range(len(labels)):
            if value_city[i] != 0 and value_village[i] != 0:
                traces.append(go.Scatter(
                    x=["city", "village"],
                    y=[value_city[i], value_village[i]],
                    name=labels[i],
                    marker=dict(
                        color=colors[i],
                        size=20
                    ), line=dict(width=8)
                ))
        print("traces:", traces)
        return html.Div([
            html.H5(['Amount of mothers in ' + str(year) + ' year in ' + clickData['points'][0]['y'] + ' obl.'],
                    style={"margin": "7px auto 0 auto",
                           "text-align": "center",
                           "font-family": 'Courier New, monospace', "font-size": 24, "color": '#7f7f7f'}),
            html.Div(dcc.Graph(
        figure={
            'data': traces,
            'layout': go.Layout(font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'),
                                height=750,
                                hovermode='closest')
        }
    ))])


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
        sorty = [y for _, y in sorted(zip(amount_city, areas))]
        sortx = sorted(amount_city)
    traces.append({
        "y": sorty,
        "x": sortx,
        "mode": "markers",
        "name": "city",
        "type": "scatter",
        "marker": dict(
            size=15,
            color=colors[7]
        ),
    })
    traces.append({
        "y": areas,
        "x": amount_village,
        "mode": "markers",
        "name": "village",
        "type": "scatter",
        "marker": dict(
            size=15,
            color=colors[1]
        )
    })

    return {
        'data': traces,
        'layout': go.Layout(
            title='Amount of kids...',
            hovermode='closest',
            font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'),
            xaxis=dict(title='Amount of kids', titlefont=dict(size=20),
                       showgrid=False,
                       zeroline=False,
                       showline=False
                       ),
            yaxis=dict(
                        showgrid=False,
                        zeroline=False,
                        showline=False),
            # yaxis={'title': 'Region', 'titlefont': dict(size=20, color='black')},
            margin={'l': 170, 'b': 60, 't': 60, 'r': 0},
            height=800
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
