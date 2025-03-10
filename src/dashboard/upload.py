# src/dashboard/upload.py
import tkinter as tk
from tkinter import filedialog

import base64
import io
import scipy.io as sio
import os
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import html
from .app import app
import dash
from data.importer import import_mat_file  # Importer la fonction
from config import __default_import_Path__

def tk_file_dialog(initialdir="."):
    """Ouvre une boîte de dialogue Tkinter pour sélectionner des fichiers .mat
    et retourne la liste des chemins complets sélectionnés."""
    root = tk.Tk()
    root.withdraw()  # Masquer la fenêtre principale
    file_paths = filedialog.askopenfilenames(
        title="Sélectionnez des fichiers .mat",
        initialdir=initialdir,
        filetypes=[("MATLAB Files", "*.mat")]
    )
    root.destroy()
    return list(file_paths)


@app.callback(
    [Output("imported-data-store", "data"),
     Output("imported-data-table", "data"),
     Output("upload-status", "children"),
     Output("last-dir-store", "data")],
    [Input("btn-import", "n_clicks"),
     Input("data-reload-item", "n_clicks")],
    [State("imported-data-store", "data"),
     State("last-dir-store", "data")]
)
def manage_data(n_clicks_upload, n_reload, current_data, last_dir):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    # Initialiser current_data et last_dir si nécessaire
    if current_data is None:
        current_data = []
    if last_dir is None or last_dir == "":
        last_dir = __default_import_Path__  # Par défaut, le répertoire courant

    messages = []
    
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    # Si le déclencheur est le bouton d'upload
    if trigger_id == "btn-import":
        file_paths = tk_file_dialog(initialdir=last_dir)  # Ouvre la boîte de dialogue Tkinter
        for path in file_paths:
            current_data, messages = import_mat_file(path, current_data, messages)
        # Mettre à jour le dernier dossier utilisé avec celui du premier fichier sélectionné
        new_last_dir = os.path.dirname(file_paths[0]) if file_paths else last_dir
    
    # Si le déclencheur est l'item de rechargement
    elif trigger_id == "data-reload-item":
        # TODO rechargement des fichiers précédemment chargés
        # if not n_reload or current_data is None:
        #     raise PreventUpdate
        # for item in current_data:
        #     path = item.get('filePath')
        #     file_name = item.get('fileName')
        #     try:
        #         if path is not None:
        #             mat_data = sio.loadmat(path, squeeze_me=True)
        #             if 'dataMap' in mat_data:
        #                 item['dataMap'] = mat_data['dataMap']
        #                 messages.append(f"{file_name} rechargé avec succès.")
        #             else:
        #                 messages.append(f"{file_name} ne contient plus 'dataMap'.")
        #         else:
        #             messages.append(f"Aucun chemin enregistré pour {file_name}.")
        #     except Exception as e:
        #         messages.append(f"Erreur lors du rechargement de {file_name}: {str(e)}")
        new_last_dir = last_dir
    else:
        raise PreventUpdate

    # Mettre à jour la table pour afficher le nom et le chemin de chaque fichier importé
    table_data = [{'fileName': item['fileName'], 'chemin': item.get('filePath', '')} for item in current_data]
    return current_data, table_data, html.Ul([html.Li(msg) for msg in messages]), new_last_dir