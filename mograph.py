import getpass
import math
import pandas as pd
import numpy as np
import datetime as dt
import urllib.parse

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default='notebook'

import plotly.express as px
from IPython.display import Markdown as md

pd.set_option('display.max_columns', None)
pd.options.plotting.backend = "plotly"


line_shape='linear'
template='plotly'


# https://github.com/plotly/plotly.py/issues/799
# https://github.com/plotly/plotly.py/issues/801
def weekhour_to_timestamp(dataframe):
    df = dataframe.copy()
    (df['day'], df['hour']) = divmod(df['weekhour'],  24)
    df['timestamp'] = df.apply(
        lambda x: pd.Timedelta(days=x['day'], hours=x['hour']) + pd.to_datetime('1970/01/05'),
        axis=1
    )
#     df['timestamp'] = df['timedelta'] + pd.to_datetime('1970/01/05')
    return df


def hour_to_timestamp(dataframe):
    df = dataframe.copy()
    df['timestamp'] = df.apply(
        lambda x: pd.Timedelta(hours=x['hour']) + pd.to_datetime('1970/01/05'),
        axis=1
    )
    return df

def day_figure(dataframe, title, columns, columnnames=None, t='timestamp', xtitle='Date', ytitle='kWh'):
    df = dataframe.copy()
    xtickformat=''
    
    if (columnnames is None):
        columnnames=columns
    if (len(columnnames) < len(columns)):
        columnames=columns
    
    if (t=='hour'):
        df = hour_to_timestamp(df)
        t='timestamp'
        xtitle = 'Hour'
        xtickformat='%I %p'

    fig = go.Figure()

    for i in range(len(columns)):
        fig.add_trace(
            go.Scatter(
                x=df[t],
                y=df[columns[i]],
                name=columnnames[i],
                line=dict(shape=line_shape)
            )
        )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(
        xaxis=dict(
            title=dict(text=xtitle),
            tickformat=xtickformat,
            tickangle=30
        )
    )
    fig.update_layout(
        yaxis=dict(
            title=dict(text=ytitle)
        )
    )
    fig.update_layout(title_text=title)
    return fig

def week_figure(dataframe, title, columns, columnnames=None, t='timestamp', xtitle='Date', ytitle='kWh', slider=True):
    df = dataframe.copy()
    xtickformat=''
    
    if (columnnames is None):
        columnnames=columns
    if (len(columnnames) < len(columns)):
        columnames=columns
    
    if (t=='weekhour'):
        df = weekhour_to_timestamp(df)
        t='timestamp'
        xtitle = 'Weekday'
        xtickformat='%a %I %p'

    fig = go.Figure()

    for i in range(len(columns)):
        fig.add_trace(
            go.Scatter(
                x=df[t],
                y=df[columns[i]],
                name=columnnames[i],
                line=dict(shape=line_shape)
            )
        )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(
        xaxis=dict(
            title=dict(text=''),
            tickformat=xtickformat,
            tickangle=30
        )
    )
    fig.update_layout(
        yaxis=dict(
            title=dict(text=ytitle)
        )
    )
    fig.update_layout(title_text=title)
    
    if (slider):
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(
                            count=12,
                            label="12h",
                            step="hour",
                            stepmode="backward"
                        ),
                        dict(
                            count=1,
                            label="1d",
                            step="day",
                            stepmode="backward"
                        ),
                        dict(
                            step="all"
                        )
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date",
                title=dict(
                    text=xtitle
                ),
                tickangle=0
            )
        )
    return fig


def month_figure(dataframe, title, columns, columnnames=None, t='timestamp', xtitle='Date', ytitle='kWh', slider=True):
    df = dataframe.copy()
    xtickformat=''
    
    if (columnnames is None):
        columnnames=columns
    if (len(columnnames) < len(columns)):
        columnames=columns
    
#     if (t=='weekhour'):
#         df = weekhour_to_timestamp(df)
#         t='timestamp'
#         xtitle = 'Weekday'
#         xtickformat='%a %I %p'

    fig = go.Figure()

    for i in range(len(columns)):
        fig.add_trace(
            go.Scatter(
                x=df[t],
                y=df[columns[i]],
                name=columnnames[i],
                line=dict(shape=line_shape)
            )
        )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(
        xaxis=dict(
            title=dict(text=''),
            tickformat=xtickformat,
            tickangle=30
        )
    )
    fig.update_layout(
        yaxis=dict(
            title=dict(text=ytitle)
        )
    )
    fig.update_layout(title_text=title)
    
    if (slider):
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(
                            count=1,
                            label="1d",
                            step="day",
                            stepmode="backward"
                        ),
                        dict(
                            count=7,
                            label="1w",
                            step="day",
                            stepmode="backward"
                        ),
                        dict(
                            count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"
                        ),
                        dict(
                            step="all"
                        )
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date",
                title=dict(
                    text='Date'
                ),
                tickangle=0
            )
        )
    return fig



def year_figure(dataframe, title, columns, columnnames=None, t='timestamp', xtitle='Date', ytitle='kWh', slider=True):
    df = dataframe.copy()
    xtickformat=''
    
    if (columnnames is None):
        columnnames=columns
    if (len(columnnames) < len(columns)):
        columnames=columns

    fig = go.Figure()

    for i in range(len(columns)):
        fig.add_trace(
            go.Scatter(
                x=df[t],
                y=df[columns[i]],
                name=columnnames[i],
                line=dict(shape=line_shape)
            )
        )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(
        xaxis=dict(
            title=dict(text=''),
            tickformat=xtickformat,
            tickangle=30
        )
    )
    fig.update_layout(
        yaxis=dict(
            title=dict(text=ytitle)
        )
    )
    fig.update_layout(title_text=title)
    
    if (slider):
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(
                            count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"
                        ),
                        dict(
                            count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"
                        ),
                        dict(
                            count=1,
                            label="YTD",
                            step="year",
                            stepmode="backward"
                        ),
                        dict(
                            count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"
                        ),
                        dict(
                            step="all"
                        )
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date",
                title=dict(
                    text='Date'
                ),
                tickangle=0
            )
        )
    return fig


#Implementation based on https://stackoverflow.com/questions/64741015/plotly-how-to-color-the-fill-between-two-lines-based-on-a-condition

# new: name of column with new data
# old: name of column with old data
# t: name of column with index
def difference_figure2(dataframe, title, new, old, t='timestamp', xtitle='Date', ytitle='kWh', slider=True):
    df = dataframe.copy()
    ls = "linear"
    xtickformat=''
    
    if (t=='weekhour'):
        df = weekhour_to_timestamp(df)
        t='timestamp'
        xtitle = 'Weekday'
        xtickformat='%a %I %p'

    df["green_above"] = df.apply(lambda row: row[new] if row[new] > row[old] else row[old], axis="columns")
    df["red_below"] = df.apply(lambda row: row[new] if row[new] <= row[old] else row[old], axis="columns")
    
    
    fig = go.Figure()


    # We need to use an invisible trace so we can reset "next y"
    # for the red area indicator
    fig.add_trace(
        go.Scatter(
            x=df[t],
            y=df[old],
            line_color='rgba(0,0,0,0)',
            name="Before ToU",
            showlegend=False,
            hoverinfo='skip',
            line=dict(shape=ls)
        )
    )
    #
    fig.add_trace(
        go.Scatter(
            x=df[t],
            y=df["red_below"],
            name="Before ToU",
            line_color='rgba(0,0,0,0)',
            connectgaps=False,
            fillcolor='rgba(255,100,0,0.4)',
            fill='tonexty',
            showlegend=False,
            hoverinfo='skip',
            line=dict(shape=ls)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df[t],
            y=df[old],
            name="Before ToU",
            line_color='rgba(0,0,0,0)',
            showlegend=False,
            hoverinfo='skip',
            line=dict(shape=ls)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df[t],
            y=df["green_above"],
            name="After ToU",
            line_color='rgba(0,0,0,0)',
            connectgaps=False,
            fillcolor='rgba(0,100,250,0.4)',
            fill='tonexty',
            showlegend=False,
            hoverinfo='skip',
            line=dict(shape=ls)
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=df[t],
            y=df[old],
            line_color='rgba(250,0,0,1)',
            name="Before ToU",
            line=dict(shape=ls, width=1)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df[t],
            y=df[new],
            name="After ToU",
            line_color="blue",
            line=dict(shape=ls)
        )
    )
    
    fig.update_layout(
        template=template
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(
        xaxis=dict(
            title=dict(text=''),
            tickformat=xtickformat,
            tickangle=30
        )
    )
    fig.update_layout(
        yaxis=dict(
            title=dict(text=ytitle)
        )
    )
    
    fig.update_layout(title_text=title)
    
    
    if (slider):
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(
                            count=12,
                            label="12h",
                            step="hour",
                            stepmode="backward"
                        ),
                        dict(
                            count=1,
                            label="1d",
                            step="day",
                            stepmode="backward"
                        ),
                        dict(
                            step="all"
                        )
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date",
                title=dict(
                    text=xtitle
                ),
                tickangle=0
            )
        )
    return fig