import json
import pymysql
from datetime import datetime
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT')),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def parse_datetime(dt_str):
    if not dt_str:
        return None
    try:
        if '.' in dt_str:
            dt_str = dt_str.split('.')[0]
        return datetime.fromisoformat(dt_str)
    except ValueError:
        return None

def insert_uasg_from_json(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            insert_query = """
            INSERT INTO uasg (
                codigoOrgao, nomeOrgao, nomeMnemonicoOrgao, cnpjCpfOrgao,
                codigoOrgaoVinculado, cnpjCpfOrgaoVinculado, nomeOrgaoVinculado,
                codigoOrgaoSuperior, cnpjCpfOrgaoSuperior, nomeOrgaoSuperior,
                codigoTipoAdministracao, nomeTipoAdministracao, poder, esfera,
                usoSisg, statusOrgao, dataHoraMovimento
            ) VALUES (
                %(codigoOrgao)s, %(nomeOrgao)s, %(nomeMnemonicoOrgao)s, %(cnpjCpfOrgao)s,
                %(codigoOrgaoVinculado)s, %(cnpjCpfOrgaoVinculado)s, %(nomeOrgaoVinculado)s,
                %(codigoOrgaoSuperior)s, %(cnpjCpfOrgaoSuperior)s, %(nomeOrgaoSuperior)s,
                %(codigoTipoAdministracao)s, %(nomeTipoAdministracao)s, %(poder)s, %(esfera)s,
                %(usoSisg)s, %(statusOrgao)s, %(dataHoraMovimento)s
            ) ON DUPLICATE KEY UPDATE
                nomeOrgao = VALUES(nomeOrgao),
                nomeMnemonicoOrgao = VALUES(nomeMnemonicoOrgao),
                cnpjCpfOrgao = VALUES(cnpjCpfOrgao);
            """

            for item in data:  # ←←← LINHA CORRIGIDA AQUI
                # Converter data
                item['dataHoraMovimento'] = parse_datetime(item.get('dataHoraMovimento'))

                # Converter booleanos para 0/1
                item['usoSisg'] = 1 if item.get('usoSisg') else 0
                item['statusOrgao'] = 1 if item.get('statusOrgao') else 0

                cursor.execute(insert_query, item)

        connection.commit()
        print(f"{len(data)} registros de UASG inseridos/atualizados com sucesso!")
    finally:
        connection.close()

if __name__ == "__main__":
    insert_uasg_from_json('/home/quirino/Documentos/github/etp_nuvem_ifsp/uasgs_raw_data.json')