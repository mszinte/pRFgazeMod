# TO DO
# 1. fix error when not enough data to plot
# 2. deploy on hiroku
# 3. change style of text to adjust the figure
# 4. change alignment of rangeslider to a fixed location

# General imports
import json
import numpy as np
import pandas as pd
from dashboards import prf_dashboard

# Dash imports
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

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

# define threshold
rsqr_th, size_th, ecc_th = analysis_info['rsqr_th'], analysis_info['size_th'], analysis_info['ecc_th']
df = df_raw[(df_raw.rsq >= rsqr_th[0]) & (df_raw.rsq <= rsqr_th[1]) & 
        (df_raw['size'] >= size_th[0]) & (df_raw['size'] <= size_th[1]) & 
        (df_raw.ecc >= ecc_th[0]) & (df_raw.ecc <= ecc_th[1])]

# define figure
fig = prf_dashboard(df,analysis_info)

# Dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    dcc.Graph(id='prf_dashboard',
              figure=fig,
              config={'displayModeBar': False}),

    # r2 range slider
    html.Div(children=  [   dcc.Markdown("__R\u00b2__ &nbsp"),
                            dcc.Markdown(id='r2_slider_text'),
                            dcc.RangeSlider(id='r2_slider',
                                            min=0, max=1,step=0.05,
                                            value = [rsqr_th[0],rsqr_th[1]],
                                            updatemode='mouseup',
                                            marks={0:'0', 0.5:'0.5', 1:'1'})],
            style={ 'text-align':'right',
                    'display': "grid", 
                    'grid-template-columns': "15% 8% 40%",
                    'margin-top': 25}),
    # eccentricity range slider
    html.Div(children=  [   dcc.Markdown("__Eccentricity (dva)__"),
                            dcc.Markdown(id='ecc_slider_text'),
                            dcc.RangeSlider(id='ecc_slider',
                                            min=0, max=20,step=0.1,
                                            value = [ecc_th[0],ecc_th[1]],
                                            updatemode='mouseup',
                                            marks={0:'0',5:'5',10:'10',15:'15',20:'20'})],
            style={ 'display': "grid", 'text-align':'right',
                    'grid-template-columns': "15% 8% 40%",
                    'margin-top': 25}),

    # size range slider
    html.Div(children=  [   dcc.Markdown('__Size (dva)__'),
                            dcc.Markdown(id='size_slider_text'),
                            dcc.RangeSlider(id='size_slider',
                                            min=0, max=20,step=0.1,
                                            value = [size_th[0],size_th[1]],
                                            updatemode='mouseup',
                                            marks={0:'0',5:'5',10:'10',15:'15',20:'20'})],
             style={ 'display': "grid", 'text-align':'right',
                    'grid-template-columns': "15% 8% 40%",
                    'margin-top': 25}),
])

@app.callback(Output('r2_slider_text', 'children'),
              Output('ecc_slider_text', 'children'),
             Output('size_slider_text', 'children'),
             Output('prf_dashboard', 'figure'),
             Input('r2_slider', 'value'),
             Input('ecc_slider', 'value'),
             Input('size_slider', 'value'))

def update_dashboard(r2_slider_value, ecc_slider_value, size_slider_value):

    txt_r2 = '\[{} / {}\]'.format(r2_slider_value[0],r2_slider_value[1])
    txt_ecc = '\[{} / {}\]'.format(ecc_slider_value[0],ecc_slider_value[1])
    txt_size = '\[{} / {}\]'.format(size_slider_value[0],size_slider_value[1])

    df = df_raw[(df_raw.rsq >= r2_slider_value[0]) & (df_raw.rsq <= r2_slider_value[1]) & 
        (df_raw['size'] >= size_slider_value[0]) & (df_raw['size'] <= size_slider_value[1]) & 
        (df_raw.ecc >= ecc_slider_value[0]) & (df_raw.ecc <= ecc_slider_value[1])]
    fig = prf_dashboard(df,analysis_info)

    return [txt_r2,txt_ecc,txt_size,fig]


if __name__ == '__main__':
    app.run_server(debug=True,port=8855)
