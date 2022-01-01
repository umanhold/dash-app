# libraries

from dash import dash, dcc, html, Input, Output, dash_table, State
import dash_bootstrap_components as dbc
import pandas as pd
from dash_extensions import Download

from python.data import Data
from python.charts import line_chart
from settings.config import config

# load data
data = Data()
df = data.process_data()

# app instance
app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
app.title = config.app_title

# server
server = app.server

# options
region_options = {region: df[(df.region == region)].country.unique() for region in df.region.unique()}
region_options.update({"World": [country for country in df.country.unique() if country != ""]})
unit_options = {unit: unit for unit in df.unit.unique()}


def filter_df(df, selected_region, selected_country, selected_unit, selected_year):

    # no unit selected
    if selected_unit == []:
        filtered = pd.DataFrame()

    else:
        # no country selected
        if selected_country in ["", None]:

            # region
            mask = (
                    (df.region == selected_region)
                    & (df.unit.isin(selected_unit))
                    & (df.year.between(selected_year[0], selected_year[1]))
            )
            group = ["year", "region", "unit"]
            filtered = df[mask].groupby(group)["value"].sum().reset_index()

        # country selected
        else:
            mask = (
                    (df.country == selected_country)
                    & (df.unit.isin(selected_unit))
                    & (df.year.between(selected_year[0], selected_year[1]))
            )
            filtered = df[mask]

    return filtered


# layout
app.layout = dbc.Container([

    html.Br(), html.Br(),

    dbc.Row([
        dbc.Col([], width=1),

        dbc.Col(
            html.H3(
                "My dashboard",
            )
        )

    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([], width=1),
        dbc.Col(
            html.H5(
                "This dashboard present random numbers and says absolutely nothing about anything.",
            )
        )
    ]),

    html.Br(), html.Br(),

    html.Div(id="output-panel"),

    dbc.Row([

        dbc.Col([], width=1),

        dbc.Col([

            # regions
            html.H5("Region"),
            dbc.RadioItems(
                id="region-radio",
                options=[{"label": r, "value": r} for r in region_options.keys()],
                value=list(region_options)[0]
            ),
            html.Br(),

            # country 
            html.H5("Country"),
            dcc.Dropdown(
                id="country-dropdown",
                placeholder="Select a country"
            ),
            html.Br(),

            # units
            html.H5("Unit"),
            dbc.Checklist(
                options=[{"label": u, "value": u} for u in unit_options.keys()],
                value=list(unit_options),
                id="unit-checklist",
                labelStyle={'display': 'inline-block'}
            )

        ], width=2),

        dbc.Col([

            # figure
            dcc.Graph(id="line-chart")

        ], width=6),

        dbc.Col([

            # table
            html.Div(id="table")

        ], width=3)
    ]),

    dbc.Row([
        dbc.Col([], width=3),
        dbc.Col([

            # year
            dcc.RangeSlider(
                id="year-range-slider",
                min=df.year.min(),
                max=df.year.max(),
                value=[df.year.min(), df.year.max()],
                marks={str(y): str(y) for y in df.sort_values(by="year").year.unique()},
                step=5,
                pushable=2
            )

        ], width=6)

        #dbc.Col([
        #    html.Div([
        #        dbc.Button("Download", id="btn-download-xlsx"),
        #        Download(id="download-xlsx")
        #    ])
        #])
    ]),

    html.Br(), html.Br(),

    dbc.Row([
        dbc.Col([], width=1),
        dbc.Col([
            html.Footer(
                "This is my private property. \
                Any violation of the copyright is followed by immediate punishment."
            )
        ], width="auto")
    ])
], id="container-body")


@app.callback(
    Output("country-dropdown", "options"),
    Input("region-radio", "value"))
def set_country_options(selected_region):
    return [{"label": i, "value": i} for i in region_options[selected_region]]


@app.callback(
    Output("country-dropdown", "value"),
    Input("country-dropdown", "options"))
def set_country_value(selected_country):
    return ""


@app.callback(
    Output("line-chart", "figure"),
    [
        Input("region-radio", "value"),
        Input("country-dropdown", "value"),
        Input("unit-checklist", "value"),
        Input("year-range-slider", "value")
    ]
)
def update_line_chart(selected_region, selected_country, selected_unit, selected_year):
    return line_chart(filter_df(df, selected_region, selected_country, selected_unit, selected_year))


@app.callback(
    Output("output-panel", "children"),
    [
        Input("region-radio", "value"),
        Input("country-dropdown", "value"),
        Input("year-range-slider", "value")
    ]
)
def update_panel(selected_region, selected_country, selected_year):
    # no country selected
    if selected_country in ["", None]:

        # region
        mask = (
                (df.region == selected_region)
                & (df.year.between(selected_year[0], selected_year[1]))
        )
        group = ["year", "region", "unit"]
        filtered = df[mask].groupby(group)["value"].sum().reset_index()

    # country selected
    else:
        mask = (
                (df.country == selected_country)
                & (df.year.between(selected_year[0], selected_year[1]))
        )
        filtered = df[mask]

    def transform(df, unit):
        return "{:,.0f}".format(df[df.unit == unit].value.sum() / 10 ** 3)

    total = {f"{unit}": transform(filtered, unit) for unit in filtered.unit.unique()}

    panel = dbc.Row([

        dbc.Col([], width=3),

        dbc.Col([
            dbc.Card(
                [f"Total Cars: {total['cars']}"]
            )
        ], width=2),

        dbc.Col([
            dbc.Card(
                [f"Total Units: {total['units']}"]
            )
        ], width=2),

        dbc.Col([
            dbc.Card(
                [f"Total Euro: {total['euro']}"]
            )
        ], width=2)
    ])

    return panel


@app.callback(
    Output("table", "children"),
    [
        Input("region-radio", "value"),
        Input("country-dropdown", "value"),
        Input("unit-checklist", "value"),
        Input("year-range-slider", "value")
    ]
)
def update_table(selected_region, selected_country, selected_unit, selected_year):
    filtered = filter_df(df, selected_region, selected_country, selected_unit, selected_year)
    filtered_copy = filtered.copy()
    filtered_copy["value"] = filtered_copy["value"].apply(lambda x: "{:,.0f}".format(x))
    filtered = filtered_copy[["year", "unit", "value"]]

    return dash_table.DataTable(
        data=filtered.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in filtered.columns],
        page_size=15,
        sort_action="native",
        sort_mode="multi",
    )