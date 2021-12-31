import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

from settings.config import config

def line_chart(df):

    fig = go.Figure()
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    
    if df.empty:

        fig.add_trace(
            go.Scatter(
                x=[], y=[], name="units"
            ),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(
                x=[], y=[], name="cars",
            ),
            secondary_y=True
        )
        title = "Select a unit"

        
    else:

        df1 = df[df.unit == "euro"]
        df2 = df[df.unit == "units"]
        df3 = df[df.unit == "cars"]

        fig.add_trace(
            go.Scatter(
                x=df1["year"], y=df1["value"], name="euro", line_color="black"
            ),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(
                x=df2["year"], y=df2["value"], name="units", line_color="grey"
            ),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(
                x=df3["year"], y=df3["value"], name="cars", line_color="red"
            ),
            secondary_y=True
        )

        region_name = df.region.unique()[0]
        country_name = df.country.unique()[0] if "country" in list(df) else ""
        title = f"{region_name}" if country_name == "" else f"{region_name}, {country_name}"

    fig.update_layout(
        title = title,
        template = "simple_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=.01
        ),
        yaxis = dict(title="EUR"),
        yaxis2 = dict(title="Number"),
        font_family=config.font,
        title_font_family=config.font,
        paper_bgcolor=config.paper_bgcolor,
        plot_bgcolor=config.plot_bgcolor,
    )
        
    return fig