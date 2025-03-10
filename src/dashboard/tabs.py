# src/dashboard/tabs.py
from dash import dcc, html
import dash_bootstrap_components as dbc
from numpy import *
from dataclasses import dataclass, asdict

display_vector_dropdown_options =[{'label': "-", 'value': ''}]

@dataclass
class Onglet:
    label: str
    value: str
    content: any
    def __init__(self, label="", value="", content=None):
        self.label=label
        self.value=value
        self.content=content

        ####### Création du modal
        new_manage_tab_modal = dbc.Modal(
            [
                dbc.ModalHeader(
                    [
                        html.Span(f"Gérer l'onglet {self.label}", style={'flex': '1'}),
                        
                        dbc.Button("X", id={'type': 'manage-tab-modal-close', 'index': self.value}, color="red", className="ml-auto", style={'fontSize': '1.5rem'}) 
                    ],
                    close_button=False,
                    style={'display': 'flex', 'alignItems': 'center'}
                ),
                dbc.ModalBody([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Nom de l'onglet : "),
                            ], width="auto"),
                            dbc.Col([
                                dbc.Input(
                                    id={'type': 'tab-name', 'index': self.value},
                                    type="text",
                                    value="",
                                    style={'marginBottom': '10px', 'with': '30%'},
                                ),
                            ], width="auto"),
                            dbc.Col([
                                dbc.Button(
                                    "✓", 
                                    id={'type': 'update-tab-name-button', 'index': self.value},
                                    color="success", 
                                    n_clicks=0,
                                    style={'marginBottom': '10px'}
                                ),
                            ], width="auto"),
                        ], align="center"),
                    ]),

                    html.Div([
                        dbc.Label("Grandeurs en axe X"),
                        dcc.Dropdown(
                            id={'type': 'display-dropdown', 'index': self.value},
                            options=display_vector_dropdown_options,
                            value=display_vector_dropdown_options[0]['value'] if display_vector_dropdown_options else None
                        )
                    ], className="mb-3"),
                ]),
            ],
            id={'type': 'manage-tab-modal', 'index': self.value},          #id={'type': 'tab-graph', 'index': tab_id}
            size="lg",
            is_open=False
        )

        ####### Création de l'onglet

        tab_content = html.Div([
            new_manage_tab_modal,
            html.Div([
                # dbc.Label("Gestion de l'onglet"),
                dbc.Button(
                    "Configuration onglet", 
                    id={'type': 'manage-tab-button', 'index': self.value},
                    color="primary", 
                    n_clicks=0,
                    style={'marginBottom': '10px'}
                ),
                dbc.Button(
                    "Supprimer cet onglet", 
                    id={'type': 'delete-tab-button', 'index': self.value},
                    color="danger", 
                    n_clicks=0,
                    style={'marginBottom': '10px'}
                ),
            ], className="mb-3"),
            
            dcc.Graph(
                id={'type': 'tab-graph', 'index': self.value},
                ),
        ], style={'padding': '20px'})

        self.content = tab_content

    

def generate_display_vector_dropdown_options(datas):
    """
    Parcourt la structure de 'datas' issue du fichier MATLAB et génère une liste d'options 
    pour un dropdown d'affichage. Pour chaque élément dans datas, si le champ 'main_display_vector' 
    existe, on extrait son contenu. On s'attend à ce que ce champ soit soit un tuple (name, units, …)
    soit un dictionnaire avec les clés 'name' et 'units'.
    
    Chaque option aura pour label "name (units)" et pour valeur le nom.
    
    Si aucune option n'est trouvée, retourne une option par défaut.
    """
    options = []
    seen = set()  # Pour éviter les doublons
    for data in datas:
        # Pour les données converties en dictionnaire
        if isinstance(data, dict) and 'main_display_vector' in data:
            mvec = data['main_display_vector']
            if isinstance(mvec, dict):
                if 'name' in mvec and 'units' in mvec:
                    name = mvec['name']
                    units = mvec['units']
                else:
                    continue
            # Sinon, si c'est un tuple ou une liste
            elif isinstance(mvec, (tuple, list)) and len(mvec) >= 2:
                name = mvec[0]
                units = mvec[1]
            else:
                continue
            
            # Éviter les doublons
            if name not in seen:
                options.append({'label': f"{name} ({units})", 'value': name})
                seen.add(name)
                
        # Si les données sont toujours sous forme de numpy record, on peut accéder via data.dtype.names
        elif hasattr(data, "dtype") and data.dtype.names and 'main_display_vector' in data.dtype.names:
            # Accès à la valeur du champ main_display_vector
            mvec = data['main_display_vector']
            # Ici, on suppose que mvec est un tuple du type (name, units, values)
            if isinstance(mvec, (tuple, list)) and len(mvec) >= 2:
                name = mvec[0]
                units = mvec[1]
                if name not in seen:
                    options.append({'label': f"{name} ({units})", 'value': name})
                    seen.add(name)
    if not options:
        options = [{'label': "Aucune option", 'value': ""}]
    return options