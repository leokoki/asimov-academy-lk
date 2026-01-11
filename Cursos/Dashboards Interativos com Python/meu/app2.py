import dash
from dash import html,dcc
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(id="div1",
    children=[
        html.H1("Hello Dash",id="h1"),
        html.H1("Dash: Um framework web para Python"),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)