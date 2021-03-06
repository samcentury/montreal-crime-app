import dash
from dash.dcc.Graph import Graph
from dash.html.Hr import Hr
from dash_bootstrap_components._components.CardBody import CardBody
from dash_bootstrap_components._components.Checklist import Checklist
import pandas as pd
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from datetime import date
from bs4 import BeautifulSoup
import requests

# === MAPBOX TOKEN ============
token = "pk.eyJ1Ijoic2FtY2VudHVyeSIsImEiOiJja3UzOG1odDg0OHQ0MndwaWl4cWdtODdlIn0.9QJ11EVq4dWOoJACwf_Sgw"


# === USING REQUESTS AND THE BEAUTIFULSOUP LIBRARY TO RETRIEVE THE CSV FILE ONLINE =====
downloadUrl = "https://donnees.montreal.ca/ville-de-montreal/actes-criminels"
source = requests.get(downloadUrl).text
soup = BeautifulSoup(source, "html.parser")
table = soup.find("table")
children = table.findChildren("a")
downloadLink = children[1].get("href")


# === INITIALIZING APP ===============
app = dash.Dash(__name__)

# ======= APP SERVER ==============
server = app.server

# = ===== CALLING DATA SETS =================
df_pop = pd.read_csv(
    "interventionscitoyendo_pop.csv", encoding="ISO-8859-1", dtype="unicode"
)  # for per capita analysis if interested
df = pd.read_csv(downloadLink, encoding="ISO-8859-1", dtype="unicode")

# ==== DATA TGRANSFORMATION TO ADD A YEAR COLUMN ==================
df1 = df
df1.dropna(inplace=True)
df1["year"] = pd.to_datetime(df1["DATE"])
df1["year"] = pd.DatetimeIndex(df1["year"]).year

# ==== DATA TRANSFORMATION TO ADD A YEAR_MONTH COLUMN ====
df1.DATE = pd.to_datetime(df1.DATE)
df1["year_month"] = df1.DATE.apply(lambda x: date(year=x.year, month=x.month, day=1))
df1["Year"] = df1.DATE.apply(lambda x: x.year)
df1["Month"] = df1.DATE.apply(lambda x: x.strftime("%b"))

# CHANGING PDQ TO POSTE TO CONNECT THE TWO DATASETS
df1["Poste"] = df1["PDQ"]
dff = pd.merge(df1, df_pop, on="Poste", how="left")

# ====== SETTING UP AN EMPTY TABLE FOR MERGING LATER ======= this is to enable KPI cards that would otherwise have empty values, to have a 0 value
table_empty = pd.DataFrame(
    {
        "CATEGORIE": [
            "Infractions entrainant la mort",
            "Introduction",
            "M??fait",
            "Vol dans / sur v??hicule ?? moteur",
            "Vol de v??hicule ?? moteur",
            "Vols qualifi??s",
        ],
        "DATE": [0, 0, 0, 0, 0, 0],
    }
)

# DEFINING APP LAYOUT
app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H1(
                        "Statistiques d'interventions polici??res ?? Montr??al",
                        className="text-center",
                    ),
                    width=12,
                )
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.Span(
                                        "Introductions",
                                        id="intro-target",
                                        style={
                                            "textDecoration": "underline",
                                            "cursor": "pointer",
                                        },
                                    ),
                                ),
                                dbc.Tooltip(
                                    "Introduction : introduction par effraction dans un ??tablissement public ou une r??sidence priv??e, vol d???arme ?? feu dans une r??sidence",
                                    target="intro-target",
                                ),
                                dbc.CardBody([html.H4(id="intro")]),
                            ],
                            style={"width": "16rem"},
                        )
                    ],
                    width={"size": 2},
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.Span(
                                        "Vols qualifi??s",
                                        id="volq-target",
                                        style={
                                            "textDecoration": "underline",
                                            "cursor": "pointer",
                                        },
                                    ),
                                ),
                                dbc.Tooltip(
                                    "Vol qualifi?? : Vol accompagn?? de violence de commerce, institution financi??re, personne, sac ?? main, v??hicule blind??, v??hicule, arme ?? feu, et tous autres types de vols qualifi??s",
                                    target="volq-target",
                                ),
                                dbc.CardBody([html.H4(id="vol-q")]),
                            ],
                            style={"width": "16rem"},
                        )
                    ],
                    width={"size": 2},
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.Span("Vol dans / sur v??hicule ?? moteur"),
                                    id="volm-target",
                                    style={
                                        "textDecoration": "underline",
                                        "cursor": "pointer",
                                    },
                                ),
                                dbc.Tooltip(
                                    "Vol dans / sur v??hicule ?? moteur : vol du contenu d???un v??hicule ?? moteur (voiture, camion, motocyclette, etc.) ou d???une pi??ce de v??hicule (roue, parechoc, etc.)",
                                    target="volm-target",
                                ),
                                dbc.CardBody([html.H4(id="vol-moteur")]),
                            ],
                            style={"width": "16rem"},
                        )
                    ],
                    width={"size": 2},
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.Span(
                                        "M??faits",
                                        id="mefaits-target",
                                        style={
                                            "textDecoration": "underline",
                                            "cursor": "pointer",
                                        },
                                    ),
                                ),
                                dbc.Tooltip(
                                    "M??fait : Graffiti et dommage de biens religieux, de v??hicule ou dommage g??n??ral et tous autres types de m??faits",
                                    target="mefaits-target",
                                ),
                                dbc.CardBody([html.H4(id="mefaits")]),
                            ],
                            style={"width": "16rem"},
                        )
                    ],
                    width={"size": 2},
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.Span(
                                        "Vol de v??hicule ?? moteur",
                                        id="volv-target",
                                        style={
                                            "textDecoration": "underline",
                                            "cursor": "pointer",
                                        },
                                    ),
                                ),
                                dbc.Tooltip(
                                    "Vol de v??hicule ?? moteur : vol de voiture, camion, motocyclette, motoneige tracteur avec ou sans remorque, v??hicule de construction ou de ferme, tout-terrain",
                                    target="volv-target",
                                ),
                                dbc.CardBody([html.H4(id="vol-auto")]),
                            ],
                            style={"width": "16rem"},
                        )
                    ],
                    width={"size": 2},
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.Span(
                                        "Infractions entrainant la mort",
                                        id="mort-target",
                                        style={
                                            "textDecoration": "underline",
                                            "cursor": "pointer",
                                        },
                                    ),
                                ),
                                dbc.Tooltip(
                                    "Infraction entra??nant la mort : Meurtre au premier degr??, meurtre au deuxi??me degr??, homicide involontaire, infanticide, n??gligence criminelle, et tous autres types d???infractions entra??nant la mort",
                                    target="mort-target",
                                ),
                                dbc.CardBody([html.H4(id="mort")]),
                            ],
                            style={"width": "18rem"},
                        )
                    ],
                    width={"size": 2},
                ),
            ]
        ),
        html.Br(),
        # ========== CONTROLS PANEL ===================================
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Arrondissement(s)"),
                                        dcc.Dropdown(
                                            id="hood-dd",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in df_pop["Quartier"].unique()
                                            ],
                                            placeholder="Quartier",
                                            multi=True,
                                            value=["Centre-ville (Ville-Marie Ouest), parc du Mont-Royal"],
                                            style={
                                                "backgroundColor": "rgba(52,51,50,255)",
                                                "color": "rgba(52,51,50,255)",
                                            },
                                        ),
                                    ]
                                ),
                                dbc.CardBody(
                                    [
                                        html.H5("Chronologie"),
                                        dcc.RangeSlider(
                                            id="slider",
                                            min=2015,
                                            max=2021,
                                            # marks = {'{}'.format(i) : '{}'.format(i) for i in sorted(dff.year_month.unique())},
                                            marks={
                                                2015: "2015",
                                                2016: "2016",
                                                2017: "2017",
                                                2018: "2018",
                                                2019: "2019",
                                                2020: "2020",
                                                2021: "2021",
                                            },
                                            dots=True,
                                            step=1,
                                            value=[2015, 2021],
                                            updatemode="drag",
                                        ),
                                    ]
                                ),
                                dbc.CardBody(
                                    [
                                        html.H5("Quart"),
                                        dcc.Checklist(
                                            id="quart-check",
                                            options=[
                                                {
                                                    "label": " jour (entre 8h01 et 16h00)",
                                                    "value": "jour",
                                                },
                                                {
                                                    "label": " soir (entre 16h01 et minuit)",
                                                    "value": "soir",
                                                },
                                                {
                                                    "label": " nuit (entre 00h01 et 8h00)",
                                                    "value": "nuit",
                                                },
                                            ],
                                            value=["jour", "soir", "nuit"],
                                            labelStyle={
                                                "display": "block",
                                                "font-size": "large",
                                            },
                                        ),
                                    ]
                                ),
                                dbc.CardBody(
                                    [
                                        html.H5("Infraction"),
                                        dcc.Dropdown(
                                            id="crime-dd",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in dff["CATEGORIE"].unique()
                                            ],
                                            value=[
                                                "Introduction",
                                                "Vols qualifi??s",
                                                "Vol dans / sur v??hicule ?? moteur",
                                                "M??fait",
                                                "Vol de v??hicule ?? moteur",
                                                "Infractions entrainant la mort",
                                            ],
                                            multi=True,
                                            style={
                                                "backgroundColor": "rgba(52,51,50,255)",
                                                "color": "rgba(52,51,50,255)",
                                            },
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ],
                    width={"size": 4},
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H5(
                                            "Chronologie des infractions compar??es ?? la moyenne de Montr??al"
                                        ),
                                        dcc.Graph(id="line-chart"),
                                    ]
                                )
                            ]
                        )
                    ],
                    width={"size": 8},
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H5("Distribution des infractions"),
                                        dcc.Graph(id="pie-chart"),
                                    ]
                                )
                            ]
                        )
                    ],
                    width={"size": 4},
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H5("Carte de la ville"),
                                        dcc.Graph(id="map"),
                                    ]
                                )
                            ]
                        )
                    ],
                    width={"size": 8},
                ),
            ]
        ),
    ],
    fluid=True,
)

# ===================CALLBACKS===================================

# ====== STATS CARDS ============================================

# === INTRODUCTION =============================================
@app.callback(
    Output("intro", "children"),
    Input("hood-dd", "value"),
    Input("slider", "value"),
    Input("quart-check", "value"),
    Input("crime-dd", "value"),
)
def update_card(chosen_hood, chosen_years, chosen_quart, chosen_crime):
    if not (chosen_hood or chosen_years or chosen_quart or chosen_crime):
        return 0
    dfff = dff[
        dff["Quartier"].isin(chosen_hood)
        & dff["QUART"].isin(chosen_quart)
        & dff["CATEGORIE"].isin(chosen_crime)
        & (dff.Year >= int(chosen_years[0]))
        & (dff.Year <= int(chosen_years[1]))
    ]
    table = pd.pivot_table(dfff, values="DATE", index="CATEGORIE", aggfunc="count")
    table1 = table.reset_index()
    table01 = table_empty.merge(table1, how="left", on="CATEGORIE")
    table01["Count"] = table01["DATE_x"] + table01["DATE_y"].fillna(0)
    table02 = table01.drop(columns=["DATE_x", "DATE_y"])
    table02 = table02.loc[table02["CATEGORIE"] == "Introduction"]
    return table02["Count"]


# === VOLS QUALIFIES =============================================
@app.callback(
    Output("vol-q", "children"),
    Input("hood-dd", "value"),
    Input("slider", "value"),
    Input("quart-check", "value"),
    Input("crime-dd", "value"),
)
def update_card(chosen_hood, chosen_years, chosen_quart, chosen_crime):
    if not (chosen_hood or chosen_years or chosen_quart or chosen_crime):
        return 0
    dfff = dff[
        dff["Quartier"].isin(chosen_hood)
        & dff["QUART"].isin(chosen_quart)
        & dff["CATEGORIE"].isin(chosen_crime)
        & (dff.Year >= int(chosen_years[0]))
        & (dff.Year <= int(chosen_years[1]))
    ]
    table = pd.pivot_table(dfff, values="DATE", index="CATEGORIE", aggfunc="count")
    table1 = table.reset_index()
    table01 = table_empty.merge(table1, how="left", on="CATEGORIE")
    table01["Count"] = table01["DATE_x"] + table01["DATE_y"].fillna(0)
    table02 = table01.drop(columns=["DATE_x", "DATE_y"])
    table02 = table02.loc[table02["CATEGORIE"] == "Vols qualifi??s"]
    return table02["Count"]


# === VOLS DANS / SUR UN VEHICULE A MOTEUR =======================
@app.callback(
    Output("vol-moteur", "children"),
    Input("hood-dd", "value"),
    Input("slider", "value"),
    Input("quart-check", "value"),
    Input("crime-dd", "value"),
)
def update_card(chosen_hood, chosen_years, chosen_quart, chosen_crime):
    if not (chosen_hood or chosen_years or chosen_quart or chosen_crime):
        return 0
    dfff = dff[
        dff["Quartier"].isin(chosen_hood)
        & dff["QUART"].isin(chosen_quart)
        & dff["CATEGORIE"].isin(chosen_crime)
        & (dff.Year >= int(chosen_years[0]))
        & (dff.Year <= int(chosen_years[1]))
    ]
    table = pd.pivot_table(dfff, values="DATE", index="CATEGORIE", aggfunc="count")
    table1 = table.reset_index()
    table01 = table_empty.merge(table1, how="left", on="CATEGORIE")
    table01["Count"] = table01["DATE_x"] + table01["DATE_y"].fillna(0)
    table02 = table01.drop(columns=["DATE_x", "DATE_y"])
    table02 = table02.loc[table02["CATEGORIE"] == "Vol dans / sur v??hicule ?? moteur"]
    return table02["Count"]


# === MEFAITS =============================================
@app.callback(
    Output("mefaits", "children"),
    Input("hood-dd", "value"),
    Input("slider", "value"),
    Input("quart-check", "value"),
    Input("crime-dd", "value"),
)
def update_card(chosen_hood, chosen_years, chosen_quart, chosen_crime):
    if not (chosen_hood or chosen_years or chosen_quart or chosen_crime):
        return 0
    dfff = dff[
        dff["Quartier"].isin(chosen_hood)
        & dff["QUART"].isin(chosen_quart)
        & dff["CATEGORIE"].isin(chosen_crime)
        & (dff.Year >= int(chosen_years[0]))
        & (dff.Year <= int(chosen_years[1]))
    ]
    table = pd.pivot_table(dfff, values="DATE", index="CATEGORIE", aggfunc="count")
    table1 = table.reset_index()
    table01 = table_empty.merge(table1, how="left", on="CATEGORIE")
    table01["Count"] = table01["DATE_x"] + table01["DATE_y"].fillna(0)
    table02 = table01.drop(columns=["DATE_x", "DATE_y"])
    table02 = table02.loc[table02["CATEGORIE"] == "M??fait"]
    return table02["Count"]


# === VOL DE VEHICULE A MOTEUR ======================================
@app.callback(
    Output("vol-auto", "children"),
    Input("hood-dd", "value"),
    Input("slider", "value"),
    Input("quart-check", "value"),
    Input("crime-dd", "value"),
)
def update_card(chosen_hood, chosen_years, chosen_quart, chosen_crime):
    if not (chosen_hood or chosen_years or chosen_quart or chosen_crime):
        return 0
    dfff = dff[
        dff["Quartier"].isin(chosen_hood)
        & dff["QUART"].isin(chosen_quart)
        & dff["CATEGORIE"].isin(chosen_crime)
        & (dff.Year >= int(chosen_years[0]))
        & (dff.Year <= int(chosen_years[1]))
    ]
    table = pd.pivot_table(dfff, values="DATE", index="CATEGORIE", aggfunc="count")
    table1 = table.reset_index()
    table01 = table_empty.merge(table1, how="left", on="CATEGORIE")
    table01["Count"] = table01["DATE_x"] + table01["DATE_y"].fillna(0)
    table02 = table01.drop(columns=["DATE_x", "DATE_y"])
    table02 = table02.loc[table02["CATEGORIE"] == "Vol de v??hicule ?? moteur"]
    return table02["Count"]


# === INFRACTION ENTRAINANT A LA MORT=================================
@app.callback(
    Output("mort", "children"),
    Input("hood-dd", "value"),
    Input("slider", "value"),
    Input("quart-check", "value"),
    Input("crime-dd", "value"),
)
def update_card(chosen_hood, chosen_years, chosen_quart, chosen_crime):
    if not (chosen_hood or chosen_years or chosen_quart or chosen_crime):
        return dash.no_update,
    dfff = dff[
        dff["Quartier"].isin(chosen_hood)
        & dff["QUART"].isin(chosen_quart)
        & dff["CATEGORIE"].isin(chosen_crime)
        & (dff.Year >= int(chosen_years[0]))
        & (dff.Year <= int(chosen_years[1]))
    ]
    table = pd.pivot_table(dfff, values="DATE", index="CATEGORIE", aggfunc="count")
    if len(table) ==  0:
        return 0
    table1 = table.reset_index()
    table01 = table_empty.merge(table1, how="left", on="CATEGORIE")
    table01["Count"] = table01["DATE_x"] + table01["DATE_y"].fillna(0)
    table02 = table01.drop(columns=["DATE_x", "DATE_y"])
    table02 = table02.loc[table02["CATEGORIE"] == "Infractions entrainant la mort"]
    return table02["Count"]


# ============ GRAPHS ==========================================
# ========== LINE CHART =====================
@app.callback(
    Output("line-chart", "figure"),
    Input("hood-dd", "value"),
    Input("slider", "value"),
    Input("quart-check", "value"),
    Input("crime-dd", "value"),
)
def update_card(chosen_hood, chosen_years, chosen_quart, chosen_crime):
    if not (chosen_hood or chosen_years or chosen_quart or chosen_crime):
        return dash.no_update
    dfff = dff[
        dff["Quartier"].isin(chosen_hood)
        & dff["QUART"].isin(chosen_quart)
        & dff["CATEGORIE"].isin(chosen_crime)
        & (dff.Year >= int(chosen_years[0]))
        & (dff.Year <= int(chosen_years[1]))
    ]
    dfff_table = dff[
        dff["QUART"].isin(chosen_quart)
        & dff["CATEGORIE"].isin(chosen_crime)
        & (dff.Year >= (chosen_years[0]))
        & (dff.Year <= (chosen_years[1]))
    ]
    table = pd.pivot_table(
        dfff, values="QUART", index="year_month", columns="Quartier", aggfunc="count"
    )
    table_av = pd.pivot_table(
        dfff_table,
        values="DATE",
        index="year_month",
        columns="Quartier",
        aggfunc="count",
    )
    table_av = table_av.mean(axis=1)
    table.insert(0, "Moyenne", table_av)
    fig = px.line(
        table, color_discrete_sequence=px.colors.sequential.Aggrnyl, line_shape="spline"
    )
    fig.update_layout(
        paper_bgcolor="rgba(52,51,50,255)", plot_bgcolor="rgba(52,51,50,255)"
    ),
    fig.update_layout(legend_x=0, legend_y=1)
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(family="Courier", size=12, color="black"),
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2,
        ),
        xaxis=dict(
            showgrid=False,
            ticks="outside",
            tickfont=dict(family="Arial", size=12, color="rgb(105, 224, 213)"),
        ),
        yaxis=dict(
            showgrid=False,
            ticks="outside",
            tickfont=dict(family="Arial", size=12, color="rgb(105, 224, 213)"),
        ),
        height=500,
    )

    return fig


# ========== PIE CHART ============
@app.callback(
    Output("pie-chart", "figure"),
    Input("hood-dd", "value"),
    Input("slider", "value"),
    Input("quart-check", "value"),
    Input("crime-dd", "value"),
)
def update_card(chosen_hood, chosen_years, chosen_quart, chosen_crime):
    if not (chosen_hood or chosen_years or chosen_quart or chosen_crime):
        return dash.no_update
    dfff = dff[
        dff["Quartier"].isin(chosen_hood)
        & dff["QUART"].isin(chosen_quart)
        & dff["CATEGORIE"].isin(chosen_crime)
        & (dff.Year >= int(chosen_years[0]))
        & (dff.Year <= int(chosen_years[1]))
    ]
    fig = px.pie(
        dfff,
        names="CATEGORIE",
        hole=0.5,
        color_discrete_sequence=px.colors.sequential.Aggrnyl,
    )
    fig.update_layout(
        paper_bgcolor="rgba(52,51,50,255)", plot_bgcolor="rgba(52,51,50,255)"
    ),
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            traceorder="reversed",
            title_font_family="Times New Roman",
            font=dict(
                family="Courier",
                size=12,
                color="black",
            ),
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2,
        ),
        font=dict(family="Courier", size=12, color="rgb(105, 224, 213)"),
    ),
    fig.update_traces(textposition="outside", textinfo="value+percent")
    return fig


# =============== MAP ===================================
@app.callback(
    Output("map", "figure"),
    Input("hood-dd", "value"),
    Input("slider", "value"),
    Input("quart-check", "value"),
    Input("crime-dd", "value"),
)
def update_card(chosen_hood, chosen_years, chosen_quart, chosen_crime):
    if not (chosen_hood or chosen_years or chosen_quart or chosen_crime):
        return dash.no_update
    dfff = dff[
        dff["Quartier"].isin(chosen_hood)
        & dff["QUART"].isin(chosen_quart)
        & dff["CATEGORIE"].isin(chosen_crime)
        & (dff.Year >= int(chosen_years[0]))
        & (dff.Year <= int(chosen_years[1]))
    ]
    fig = px.scatter_mapbox(
        dfff,
        lat="LATITUDE",
        lon="LONGITUDE",
        center=dict(lat=45.511833, lon=-73.622806),
        zoom=9.5,
        color_discrete_sequence=px.colors.sequential.Aggrnyl,
        color="CATEGORIE",
        hover_name="CATEGORIE",
        hover_data=["DATE"],
    )
    fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}),
    fig.update_layout(
        legend=dict(
            x=0,
            y=1,
            traceorder="reversed",
            title_font_family="Times New Roman",
            font=dict(
                family="Courier",
                size=12,
                color="black",
            ),
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2,
        )
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
