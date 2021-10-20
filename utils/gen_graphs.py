from utils.miscellaneous import MONTHS_IN_PT
import dash_core_components as dcc
import dash_html_components as html


def gen_graph_imports_exports(imports, exports, prod='Geral'):
    div = html.Div([html.Div(children=u'Gráfico de movimentação por produto', style={
        'textAlign': 'center',
        'color': "#7FDBFF"
    }),
                    html.Div(
                        dcc.Graph(
                            figure={
                                'data': [
                                    {'x': MONTHS_IN_PT, 'y': imports, 'type': 'bar', 'name': u'Importações'},
                                    {'x': MONTHS_IN_PT, 'y': exports, 'type': 'bar', 'name': u'Exportações'},
                                ],
                                'layout': {
                                    'title': u'Total de Movimentações para ' + prod
                                }
                            }
                        )
                    )
                    ])
    return div
