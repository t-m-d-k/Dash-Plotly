from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output
import dash_bootstrap_components as dbc

app = Dash(__name__)
#dbc row col dash plotly

#https://stackoverflow.com/questions/63592900/plotly-dash-how-to-design-the-layout-using-dash-bootstrap-components


colors = {
    'background': '#f7f0f0',
    'text': '#171313'
}



df1 = pd.read_csv(r"test_nsm.csv")
metricsDf = pd.read_csv(r"Input metrics.csv")


fig1 = px.line(metricsDf, x="date", y="Breadth", color_discrete_sequence=['#ff9616'])
fig2 = px.line(metricsDf, x="date", y="Depth", color_discrete_sequence=['#ff9616'])
fig3 = px.line(metricsDf, x="date", y="Frequency", color_discrete_sequence=['#bc7196'])
fig4 = px.line(metricsDf, x="date", y="Stickiness", color_discrete_sequence=['#1f77b4'])




df1["tt_date"] = pd.to_datetime(df1["tt_date"])
df1["date"] = df1['tt_date'].dt.strftime('%d')
df1['datemonth'] = df1["tt_date"].dt.strftime('%b-%d')
df1["month"] = df1['tt_date'].dt.strftime('%m')
df1['year'] = df1['tt_date'].dt.strftime('%Y')

def GetMonthInInt(month):
    MonthInInts = pd.Series(['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'],index=['01', '02', '03', '04', '05' , '06', '07', '08', '09', '10' ,'11' , '12'])
    return MonthInInts[month.lower()]
#df1['newmonth']= df1['month'].apply(GetMonthInInt)


testingDf = df1.groupby(['datemonth', 'year']).agg({'NSM_sess':'sum'}).reset_index()

#testingDf = df1.groupby(['date', 'year']).agg({'NSM_sess':'sum'}).reset_index()
#testingDf = df1.groupby(['month']).agg({'NSM_sess':'sum'}).reset_index()
#testingDf[['year', 'changemonth']] = testingDf['month'].str.split('-', expand=True)

from colour import Color
import plotly.graph_objects as go
#from chart_studio.plotly import iplot
from plotly.offline import iplot







def plotPMByYear_plotly(df, color1,color2):
    
    allYears = list(set(list(df.year)))
    allYears = [str(x) for x in allYears if str(x) != 'nan']
    allYears.sort()
    colors = list(Color(color1).range_to(Color(color2),len(allYears)))
    colors = ['rgb'+str(x.rgb) for x in colors]
    data = []
    i = 0
    print(allYears)
    for year in allYears:
        yeardf = df[df["year"] == year]
        
        #yeardf = df
        trace = go.Scatter(
            x = yeardf['datemonth'],
            y = yeardf['NSM_sess'],
            mode = 'markers',
            marker=dict(color=colors[i]),
            name = year
        )
        i+=1
        data.append(trace)

    layout = go.Layout(
        title = 'Year on Year comparison'
    )

    fig = go.Figure(data=data, layout=layout)
    return fig


fig_nsm = px.line(df1, x="tt_date", y="frac_rol", color_discrete_sequence=['#2ca02c'])

yearDf = df1.groupby(['year']).agg({'tot_sess':'sum','NSM_sess':'sum'}).reset_index()
fig_year = go.Figure(
    data=[
        go.Bar(name='Total', x=yearDf['year'], y=yearDf['tot_sess'], yaxis='y', offsetgroup=1),
        go.Bar(name='NSM ', x=yearDf['year'], y=yearDf['NSM_sess'], yaxis='y2', offsetgroup=2)
    ],
    layout={
        'yaxis': {'title': 'Total Session'},
        'yaxis2': {'title': 'NSM Session', 'overlaying': 'y', 'side': 'right'},
        'xaxis': {'title': 'Period'}
    }
)

monthDf = df1.groupby(['month']).agg({'tot_sess':'sum','NSM_sess':'sum'}).reset_index()
fig_month = go.Figure(
    data=[
        go.Bar(name='Total', x=monthDf['month'], y=monthDf['tot_sess'], yaxis='y', offsetgroup=1),
        go.Bar(name='NSM ', x=monthDf['month'], y=monthDf['NSM_sess'], yaxis='y2', offsetgroup=2)
    ],
    layout={
        'yaxis': {'title': 'Total Session'},
        'yaxis2': {'title': 'NSM Session', 'overlaying': 'y', 'side': 'right'},
        'xaxis': {'title': 'Period'}
    }

)

monthFracDf = df1.groupby(['month']).agg({'Frac':'sum', 'frac_rol': 'sum'}).reset_index()
yearFracDf = df1.groupby(['year']).agg({'Frac':'sum', 'frac_rol': 'sum'}).reset_index()

frac_year = go.Figure(
    data=[
        go.Bar(name='Frac', x=yearFracDf['year'], y=yearFracDf['Frac'], yaxis='y', offsetgroup=1),
        go.Bar(name='frac_rol ', x=yearFracDf['year'], y=yearFracDf['frac_rol'], yaxis='y2', offsetgroup=2)
    ],
    layout={
        'yaxis': {'title': 'Frac'},
        'yaxis2': {'title': 'frac_rol', 'overlaying': 'y', 'side': 'right'},
        'xaxis': {'title': 'Period'}
    }
)

frac_month = go.Figure(
    data=[
        go.Bar(name='Frac', x=monthFracDf['month'], y=monthFracDf['Frac'], yaxis='y', offsetgroup=1),
        go.Bar(name='frac_rol ', x=monthFracDf['month'], y=monthFracDf['frac_rol'], yaxis='y2', offsetgroup=2)
    ],
    layout={
        'yaxis': {'title': 'Frac'},
        'yaxis2': {'title': 'frac_rol', 'overlaying': 'y', 'side': 'right'},
        'xaxis': {'title': 'Period'}
    }
)


frac_year.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

frac_month.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig_year.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig_month.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig3.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig4.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='North Star  Metrics',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    dcc.Graph(
        figure=dict(
            data=[
                dict(
                    x=monthDf['month'],
                    y=monthDf['NSM_sess'],
                    name='NSM Session',
                    marker=dict(
                        color='rgb(26, 255, 26)'
                    )
                ),
                dict(
                    x=monthDf['month'],
                    y=monthDf['tot_sess'],
                    name='Total Session',
                    marker=dict(
                        color='rgb(126, 157, 207)'
                    )
                )
            ],
            layout=dict(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text'],
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=120, r=120, t=60, b=60, pad=4)
                
            )
        ),

        id='my-graph-example'
    ),
    html.Div(style={'backgroundColor': colors['background'],'padding': 10, 'flex': 1, "width": "10%"}, children=[
        
        dcc.RadioItems(['Month', 'Year'], 'Year', id='dropdownoption')]),

            html.Div(style={'display': 'inline-block', "width": "50%"}, children=[
                
            dcc.Graph(id="graph", style={'display': 'inline-block', 'color': 'Red',"width": "90%"}, figure=fig_year.update_layout(barmode='group')),
            ]),
            
            html.Div(style={'display': 'inline-block', "width": "50%"}, children=[
                
            dcc.Graph(id="graph1", style={'display': 'inline-block', 'color': 'Red',"width": "90%"}, figure=frac_year.update_layout(barmode='group')),
            ]),
            dcc.Graph(figure= plotPMByYear_plotly(testingDf, 'blue','red')), 
    dcc.Graph(
        figure=dict(
            data=[
                dict(
                    x=df1['tt_date'],
                    y=df1['Frac'],
                    name='Frac',
                    marker=dict(
                        color='rgb(26, 255, 26)'
                    )
                ),
                dict(
                    x=df1['tt_date'],
                    y=df1['frac_rol'],
                    name='Frac Rol',
                    marker=dict(
                        color='rgb(126, 157, 207)'
                    )
                )
            ],
            layout=dict(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text'],
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=120, r=120, t=60, b=60, pad=4)
                
            )
        ),

        id='my-graph-example1'
    ),
        html.Div(style={'backgroundColor': colors['background'],'padding': 10, 'flex': 1, "width": "60%"}, children=[
        html.H4(children="Rolling Window", style={'textAlign': 'left'}),
        #dcc.Dropdown(['27', '28', '29'], '28', id='dropdownoptionone')]),
        dcc.Slider(1, 30, 1,
               value=28,
               id='my-slider'
    )]),
        
        html.Div(style={'display': 'inline-block'}, children=[
            html.Div(style={'display': 'inline-block', "width": "50%"}, children=[
                html.H4(children="Breadth", style={'textAlign': 'center'}),
                dcc.Graph(id="graphone", style={'display': 'inline-block', 'color': 'Red',"width": "90%"}, figure=fig1),
            ]),
            html.Div(style={'display': 'inline-block', "width": "50%"}, children=[
                html.H4(children="Depth", style={'textAlign': 'center'}),
                dcc.Graph(id="graphtwo", style={'display': 'inline-block',"width": "90%"}, figure=fig2),
            ]),
            html.Div(style={'display': 'inline-block', "width": "50%"}, children=[
                html.H4(children="Frequency", style={'textAlign': 'center'}),
                dcc.Graph(id="graphthree", style={'display': 'inline-block',"width": "90%"}, figure=fig3),
            ]),
            html.Div(style={'display': 'inline-block', "width": "50%"}, children=[
                html.H4(children="Stickiness", style={'textAlign': 'center'}),
                dcc.Graph(id="graphfour", style={'display': 'inline-block',"width": "90%"}, figure=fig4),
            ]),

        ]),
])

@app.callback(Output("graph", "figure"),
              Input("dropdownoption", "value"))
def update_output(dd_val):
    if dd_val.lower() == "year":
        return fig_year 
    else:
        return fig_month
@app.callback(Output("graph1", "figure"),
              Input("dropdownoption", "value"))
def update_output(dd_val):
    if dd_val.lower() == "year":
        return frac_year 
    else:
        return frac_month
        
@app.callback(Output("graphone", "figure"),
              Input("my-slider", "value"))
def update_output(dd_val):

    metricsDf = pd.read_csv(r"Input metrics.csv")
    metricsDfRunningAvg = metricsDf
    metricsDfRunningAvg['Breadth'] = metricsDfRunningAvg['Breadth'].rolling(int(dd_val)).mean()
    fig1 = px.line(metricsDfRunningAvg, x="date", y="Breadth", color_discrete_sequence=['#ff9616'])
    fig1.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
    return fig1 

@app.callback(Output("graphtwo", "figure"),
              Input("my-slider", "value"))
def update_output(dd_val):

    metricsDf = pd.read_csv(r"Input metrics.csv")
    metricsDfRunningAvg = metricsDf
    metricsDfRunningAvg['Depth'] = metricsDfRunningAvg['Depth'].rolling(int(dd_val)).mean()
    fig2 = px.line(metricsDfRunningAvg, x="date", y="Depth", color_discrete_sequence=['#ff9616'])
    fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
    return fig2 
    
@app.callback(Output("graphthree", "figure"),
              Input("my-slider", "value"))
def update_output(dd_val):

    metricsDf = pd.read_csv(r"Input metrics.csv")
    metricsDfRunningAvg = metricsDf
    metricsDfRunningAvg['Frequency'] = metricsDfRunningAvg['Frequency'].rolling(int(dd_val)).mean()
    fig3 = px.line(metricsDfRunningAvg, x="date", y="Frequency", color_discrete_sequence=['#ff9616'])
    fig3.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
    return fig3 

@app.callback(Output("graphfour", "figure"),
              Input("my-slider", "value"))
def update_output(dd_val):

    metricsDf = pd.read_csv(r"Input metrics.csv")
    metricsDfRunningAvg = metricsDf
    metricsDfRunningAvg['Stickiness'] = metricsDfRunningAvg['Stickiness'].rolling(int(dd_val)).mean()
    fig3 = px.line(metricsDfRunningAvg, x="date", y="Stickiness", color_discrete_sequence=['#ff9616'])
    fig3.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
    return fig4 
 
        
        
if __name__ == '__main__':
    app.run_server(debug=True)
    ##hello
