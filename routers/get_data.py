from flask import Blueprint, Response, request
import pandas as pd
import pathlib
import os
from config.environment import MAX_ROWS

get_data_router = Blueprint('data_router', __name__)

path = os.path.dirname(__file__)
# path = pathlib.Path(__file__)
# path = path.absolute().name

df_comex = pd.read_csv(path + '/../dados_projetos/f_comex.csv', delimiter=';')
df_sh2 = pd.read_excel(path + '/../dados_projetos/d_sh2.xlsx', engine='openpyxl')
df_via = pd.read_excel(path + '/../dados_projetos/d_via.xlsx', engine='openpyxl')
get_max_rows = lambda data, max_rows: data.head(int(max_rows)) if max_rows else data.head(MAX_ROWS)


@get_data_router.route('/data/comex_year', methods=['GET'])
def get_comex_data():
    args = request.args
    max_rows = args.get('max_rows')
    ano = args.get('ano')
    data = df_comex.loc[df_comex['ANO'].isin([ano])]
    data = get_max_rows(data, max_rows)

    return Response(
        data.to_json(),
        200)


@get_data_router.route('/data/comex', methods=['GET'])
def get_comex():
    args = request.args
    max_rows = args.get('max_rows')
    data = get_max_rows(df_comex, max_rows)

    return Response(
        data.to_json(),
        200)


@get_data_router.route('/data/comex_movimentacao', methods=['GET'])
def get_comex_data_type():
    args = request.args
    max_rows = args.get('max_rows')
    tipo = args.get('movimentacao')

    data = df_comex.loc[df_comex['MOVIMENTACAO'].isin([tipo])]
    # data = data.head(max_rows) if max_rows else data.head(MAX_ROWS)
    data = get_max_rows(data, max_rows)

    return Response(
        data.to_json(),
        200)


@get_data_router.route('/data/comex_product', methods=['GET'])
def get_comex_data_product():
    args = request.args
    max_rows = args.get('max_rows')
    cod_ncm = args.get('cod_ncm')

    data = df_comex.loc[df_comex['COD_NCM'].isin([cod_ncm])]
    data = get_max_rows(data, max_rows)

    return Response(
        data.to_json(),
        200)


@get_data_router.route('/data/sh2_ncm')
def get_sh2_ncm():
    args = request.args
    max_rows = args.get('max_rows')
    ncm = args.get('ncm')

    data = df_sh2.loc[df_sh2['COD_NCM'].isin([ncm])]
    data = get_max_rows(data, max_rows)

    return Response(
        data.to_json(),
        200
    )


@get_data_router.route('/data/sh2', methods=['GET'])
def get_sh2():
    args = request.args
    max_rows = args.get('max_rows')
    data = get_max_rows(df_sh2, max_rows)

    return Response(
        data.to_json(),
        200
    )


@get_data_router.route('/data/d_via', methods=['GET'])
def get_d_via():
    args = request.args
    max_rows = args.get('max_rows')
    data = get_max_rows(df_via, max_rows)

    return Response(
        data.to_json(),
        200
    )


if __name__ == '__main__':
    # dt = df_comex.loc[df_comex['ANO'].isin([2020])]
    dt = df_comex['ANO'].unique()
    print(dt)
