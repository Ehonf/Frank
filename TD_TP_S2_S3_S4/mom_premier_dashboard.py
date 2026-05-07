# --- ÉTAPE 1 : IMPORTER LES BIBLIOTHÈQUES ---
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# --- ÉTAPE 2 : CHARGER LES DONNÉES ---
# Gapminder contient des données sur les pays (PIB, espérance de vie, population)
df = px.data.gapminder()

# On garde uniquement les pays d'Afrique
df_afrique = df[df['continent'] == 'Africa']

# On récupère la liste des pays africains
liste_pays = sorted(df_afrique['country'].unique())

# --- ÉTAPE 3 : CRÉER L'APPLICATION ---
app = dash.Dash(__name__)

# --- ÉTAPE 4 : CONSTRUIRE L'INTERFACE (LAYOUT) ---
app.layout = html.Div([

    # Titre principal
    html.H1(
        "🌍 Mon premier dashboard africain",
        style={
            'textAlign': 'center', 'color': 'white', 'backgroundColor': '#1abc9c',
            'padding': '20px'
        }
    ),

    # Menu déroulant pour choisir un pays
    html.Label("Choisissez un pays :"),
    dcc.Dropdown(
        id='selection-pays',
        options=[{'label': pays, 'value': pays} for pays in liste_pays],
        value='Senegal'  # Valeur par défaut
    ),

    # Graphique 1 : Évolution de l'espérance de vie
    dcc.Graph(id='graphique-esperance-vie'),

    html.Br(),

    html.Label("Choisissez une année :"),

    dcc.Slider(
        id='slider-annee',
        min=df_afrique['year'].min(),
        max=df_afrique['year'].max(),
        step=5,
        value=df_afrique['year'].max(),
        marks={str(year): str(year) for year in df_afrique['year'].unique()}
    ),

    # Graphique 2 : Carte de l'Afrique
    dcc.Graph(id='carte-afrique'),

    dcc.Graph(id='graphique-scatter')
],
    style={
        'backgroundColor': '#ecf0f1', 'padding': '30px'
    }
)


# --- ÉTAPE 5 : AJOUTER L'INTERACTIVITÉ (CALLBACKS) ---

# Callback pour le graphique en courbe
@app.callback(
    Output('graphique-esperance-vie', 'figure'),
    Input('selection-pays', 'value')
)
def mettre_a_jour_courbe(pays_choisi):
    # Filtrer les données pour le pays choisi
    donnees_pays = df_afrique[df_afrique['country'] == pays_choisi]

    # Créer le graphique
    fig = px.line(donnees_pays,
                  x='year',
                  y='lifeExp',
                  title=f'Espérance de vie au {pays_choisi}')

    return fig


# Callback pour la carte
@app.callback(
    Output('carte-afrique', 'figure'),
    Input('selection-pays', 'value')  # Même input, mais on pourrait en ajouter
)
def mettre_a_jour_carte(annee_choisie):
    # On prend l'année la plus récente
    annee_recente = df_afrique['year'].max()
    donnees_annee = df_afrique[df_afrique['year'] == annee_recente]
    donnees_annee = df_afrique[df_afrique['year'] == annee_choisie]

    # Créer la carte
    fig = px.choropleth(donnees_annee,
                        locations='iso_alpha',
                        color='lifeExp',
                        hover_name='country',
                        title=f"Espérance de vie en Afrique ({annee_choisie})",
                        color_continuous_scale='Viridis')

    # Zoomer sur l'Afrique
    fig.update_geos(scope='africa')

    return fig

@app.callback(
    Output('graphique-scatter', 'figure'),
    Input('slider-annee', 'value')
)
def mettre_a_jour_scatter(annee_choisie):
    donnees = df_afrique[df_afrique['year'] == annee_choisie]

    fig = px.scatter(
        donnees,
        x='gdpPercap',
        y='lifeExp',
        size='pop',
        color='country',
        hover_name='country',
        log_x=True,
        title=f"PIB vs Espérance de vie ({annee_choisie})"
    )

    return fig


# --- ÉTAPE 6 : LANCER L'APPLICATION ---
if __name__ == '__main__':
    app.run(debug=True)