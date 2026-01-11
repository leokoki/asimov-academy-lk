from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import dash
from app import *
 
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template

app = dash.Dash(__name__)
server = app.server

df_data = pd.read_csv(r"./Cursos/Dashboards Interativos com Python/4. Layouts profissionais com DBC/supermarket_sales.csv")
df_data["Date"] = pd.to_datetime(df_data["Date"])

# =========== Layout ============== #
app.layout = html.Div(children=[
                        html.H5("Cidades:"),
                            ])

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)