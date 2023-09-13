import math
import plotly
import dash_bootstrap_components as dbc
from dash import html, dcc
import dash
from django_plotly_dash import DjangoDash
from geopy.geocoders import ArcGIS
import plotly.graph_objects as go
import plotly.express as px
import multiprocessing
import re
import pandas as pd

class Mapa:
    def __init__(self, df, col):
        self.col = col
        self.df = df

    def criar_mapa(self):
        app = DjangoDash("mapa",
                add_bootstrap_links=True)

        app.layout = html.Div(
            dcc.Graph(id='mapa', figure=self.gerar_grafico()))
        return app
    
    def encontrar_coordenadas(self, x):
        nom = ArcGIS()
        coordenada = nom.geocode(x)
        if coordenada:
            return coordenada.latitude, coordenada.longitude
    
    def requisicao(self, df):
        df[['Latitude', 'Longitude']] = df[self.col].apply(lambda x: pd.Series(self.encontrar_coordenadas(x)))
        return df
    def gerar_grafico(self):
        df = self.requisicao(self.df)
        fig = go.Figure(go.Scattermapbox(
            lat=df['Latitude'],
            lon=df['Longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=15,
                color='rgb(0, 100, 58)',
                opacity=0.7
            ),
            text=df,
        ))

        # Configura o layout do mapa
        fig.update_layout(
            mapbox_style='open-street-map',
            mapbox_center_lon=0,
            margin={'r': 0, 't': 0, 'l': 0, 'b': 0}
        )
        # Obtém os valores mínimos e máximos de latitude e longitude
        lat_min, lat_max = df['Latitude'].min(), df['Latitude'].max()
        lon_min, lon_max = df['Longitude'].min(), df['Longitude'].max()
        
        # Calcula o centro do mapa
        center_lat = (lat_min + lat_max) / 2
        center_lon = (lon_min + lon_max) / 2
        # Calcula a extensão das coordenadas
        lat_extent = lat_max - lat_min
        lon_extent = lon_max - lon_min
        # Define o nível de zoom
        zoom_lat = math.log10(360 / lat_extent) / math.log10(2)
        zoom_lon = math.log10(360 / lon_extent) / math.log10(2)
        zoom = min(zoom_lat, zoom_lon)
            
        # Configura o layout do mapa com o zoom nas coordenadas marcadas
        fig.update_layout(
        mapbox={
            'center': {'lon': center_lon, 'lat': center_lat},
            'zoom': zoom
        }
    )
        return fig