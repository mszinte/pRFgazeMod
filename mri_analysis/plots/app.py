# General imports
import json
import numpy as np
import pandas as pd
from dashboards import prf_dashboard

# Dash imports
import dash
import dash_core_components as dcc
import dash_html_components as html

# Get inputs
subject = 'sub-001'
task = 'GazeCenterFS'
preproc = 'fmriprep_dct_pca'

# Define analysis parameters
with open('mri_analysis/settings.json') as f:
    json_s = f.read()
    analysis_info = json.loads(json_s)

# create/load dataframe
# df_name = create_dataframe(subject=subject, task=task, preproc=preproc,analysis_info=analysis_info)
df_name = '/Users/martinszinte/disks/meso_S/data/pRFgazeMod/pp_data/sub-001/gauss/pandas/sub-001_GazeCenterFS_fmriprep_dct_pca.gz'
df_raw = pd.read_csv(df_name)

# thresholds
rsqr_th, size_th, ecc_th = analysis_info['rsqr_th'], analysis_info['size_th'], analysis_info['ecc_th']
df = df_raw[(df_raw.rsq >= rsqr_th) & 
        (df_raw['size'] >= size_th[0]) & (df_raw['size'] <= size_th[1]) & 
        (df_raw.ecc >= ecc_th[0]) & (df_raw.ecc <= ecc_th[1])]

# define figure
fig = prf_dashboard(df,analysis_info)

# Dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    
    dcc.Graph(
        id='prf_dashboard',
        figure=fig,
        config={'displayModeBar': False})
])

if __name__ == '__main__':
    app.run_server(debug=True)

# useless comment