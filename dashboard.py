import json
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from routers.get_data import df_comex, df_sh2, df_via
from config.environment import MAX_ROWS
import pandas as pd
import plotly.express as px
from utils.do_requests import get_request

app = dash.Dash()
colors = {
    'background': '#FFFFFF',
    'text': '#7FDBFF'
}
filter_opt = None
df_output = None

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Visualizacao',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='Dash: Site simples para visualizacao de dados.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Div(children='Selecione o filtro'),
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Ano', 'value': 'ANO'},
            {'label': 'Movimentacao', 'value': 'MOVIMENTACAO'},
            {'label': 'Produto', 'value': 'COD_NCM'}
        ],
        value='ANO',
        # multi=True
    ),
    html.Div(id='dd-output-container'),
    # Generate pie chart
    dcc.Graph(
        figure=px.pie(df_comex, 'COD_VIA', 'COD_VIA', title='Porcentagem de uso de vias', )
    ),
])

pd.options.mode.chained_assignment = None  # default='warn'


def calc_total_import_export(df):
    months = df['MES'].unique()
    months.sort()
    imports = []
    exports = []
    for m in months:
        df_month = df.loc[df['MES'] == m]
        df_temp = df_month.loc[df_month['MOVIMENTACAO'].isin(['Exportação'])]
        exports.append(len(df_temp.index))
        df_temp = df_month.loc[df_month['MOVIMENTACAO'].isin(['Importação'])]
        imports.append(len(df_temp.index))
    return imports, exports


def dashboard():
    global app
    return app


@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def dropdown_callback(value):
    global filter_opt
    # df_comex = get_request('/data/comex')

    x = df_comex[value].unique()
    if value == 'COD_NCM':
        x = df_sh2['NO_NCM_POR'].unique()
    filter_opt = value
    return html.Div([
        dcc.Dropdown(
            id='dropdown-1',
            options=[
                {'label': i, 'value': i} for i in x
            ],
            value=x[0],
            # multi=True
        ),
        html.Div(id='dd-output-filter')
    ])


@app.callback(
    Output('dd-output-filter', 'children'),
    Input('dropdown-1', 'value'),
    prevent_initial_call=True,
)
def get_filter(opt):
    global df_output
    from utils.gen_graphs import gen_graph_imports_exports

    div = html.Div()

    # Filter by product
    if filter_opt == 'COD_NCM':
        # Uncomment to use API
        # response = get_request("/data/sh2")
        # df_dict = response.json()
        # df = pd.DataFrame.from_dict(df_dict)
        df = df_sh2

        df_temp = df.loc[df['NO_NCM_POR'] == opt]
        cod_ncm = df_temp['COD_NCM']
        df_output = df_comex.loc[df_comex[filter_opt].isin(cod_ncm)]
        # Get total of import and export
        imports, exports = calc_total_import_export(df_output)
        div = gen_graph_imports_exports(imports, exports, opt)

    else:
        # Calcs the overall imports exports
        df_output = df_comex.loc[df_comex[filter_opt].isin([opt])]
        imports, exports = calc_total_import_export(df_output)
        div = gen_graph_imports_exports(imports, exports)

    # Update cod_via to a string
    # TODO: very slow. We need to otimize it
    # for i in df_via.index:
    #     df_comex['COD_VIA'].replace({df_via.at[i, 'CO_VIA']: df_via.at[i, 'NO_VIA']}, inplace=True)

    return html.Table(className="table", children=[
        html.Thead(
            html.Tr([html.Th(col) for col in df_output.columns]),
        ),
        html.Tbody([
            html.Tr([
                html.Td(df_output.iloc[i][col]) for col in df_output.columns
            ]) for i in range(min(len(df_output), MAX_ROWS))
        ]),
        div,
    ])


@app.callback(
    Output('download-text', 'data'),
    Input('btn-download-txt', 'n_clicks'),
    prevent_initial_call=True,
)
def download(n_clicks):
    return dict(content=open('results.csv', 'r').read(), filename='results.csv')


if __name__ == '__main__':
    app = dashboard()
    app.run_server()
