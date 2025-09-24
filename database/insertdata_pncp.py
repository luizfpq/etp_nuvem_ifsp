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
    if dt_str is None:
        return None
    try:
        # Remove milissegundos se presentes e ajusta fuso
        dt_str = dt_str.split('.')[0]  # Remove parte após milissegundos
        if 'T' in dt_str:
            return datetime.fromisoformat(dt_str)
        else:
            return None
    except ValueError:
        return None

def insert_compras_from_json(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            insert_query = """
            INSERT INTO compras_pncp (
                idCompra, numeroControlePNCP, anoCompraPncp, sequencialCompraPncp,
                orgaoEntidadeCnpj, orgaoSubrogadoCnpj, codigoOrgao, orgaoEntidadeRazaoSocial,
                orgaoSubrogadoRazaoSocial, orgaoEntidadeEsferaId, orgaoSubrogadoEsferaId,
                orgaoEntidadePoderId, orgaoSubrogadoPoderId, unidadeOrgaoCodigoUnidade,
                unidadeSubrogadaCodigoUnidade, unidadeOrgaoNomeUnidade, unidadeSubrogadaNomeUnidade,
                unidadeOrgaoUfSigla, unidadeSubrogadaUfSigla, unidadeOrgaoMunicipioNome,
                unidade_subrogada_municipio_nome, unidadeOrgaoCodigoIbge, unidadeSubrogadaCodigoIbge,
                numeroCompra, modalidadeIdPncp, codigoModalidade, modalidadeNome, srp,
                modoDisputaIdPncp, codigoModoDisputa, amparoLegalCodigoPncp, amparoLegalNome,
                amparoLegalDescricao, informacaoComplementar, processo, objetoCompra,
                existeResultado, orcamentoSigilosoCodigo, orcamentoSigilosoDescricao,
                situacaoCompraIdPncp, situacaoCompraNomePncp, tipoInstrumentoConvocatorioCodigoPncp,
                tipoInstrumentoConvocatorioNome, modoDisputaNomePncp, valorTotalEstimado,
                valorTotalHomologado, dataInclusaoPncp, dataAtualizacaoPncp, dataPublicacaoPncp,
                dataAberturaPropostaPncp, dataEncerramentoPropostaPncp, contratacaoExcluida
            ) VALUES (
                %(idCompra)s, %(numeroControlePNCP)s, %(anoCompraPncp)s, %(sequencialCompraPncp)s,
                %(orgaoEntidadeCnpj)s, %(orgaoSubrogadoCnpj)s, %(codigoOrgao)s, %(orgaoEntidadeRazaoSocial)s,
                %(orgaoSubrogadoRazaoSocial)s, %(orgaoEntidadeEsferaId)s, %(orgaoSubrogadoEsferaId)s,
                %(orgaoEntidadePoderId)s, %(orgaoSubrogadoPoderId)s, %(unidadeOrgaoCodigoUnidade)s,
                %(unidadeSubrogadaCodigoUnidade)s, %(unidadeOrgaoNomeUnidade)s, %(unidadeSubrogadaNomeUnidade)s,
                %(unidadeOrgaoUfSigla)s, %(unidadeSubrogadaUfSigla)s, %(unidadeOrgaoMunicipioNome)s,
                %(unidade_subrogada_municipio_nome)s, %(unidadeOrgaoCodigoIbge)s, %(unidadeSubrogadaCodigoIbge)s,
                %(numeroCompra)s, %(modalidadeIdPncp)s, %(codigoModalidade)s, %(modalidadeNome)s, %(srp)s,
                %(modoDisputaIdPncp)s, %(codigoModoDisputa)s, %(amparoLegalCodigoPncp)s, %(amparoLegalNome)s,
                %(amparoLegalDescricao)s, %(informacaoComplementar)s, %(processo)s, %(objetoCompra)s,
                %(existeResultado)s, %(orcamentoSigilosoCodigo)s, %(orcamentoSigilosoDescricao)s,
                %(situacaoCompraIdPncp)s, %(situacaoCompraNomePncp)s, %(tipoInstrumentoConvocatorioCodigoPncp)s,
                %(tipoInstrumentoConvocatorioNome)s, %(modoDisputaNomePncp)s, %(valorTotalEstimado)s,
                %(valorTotalHomologado)s, %(dataInclusaoPncp)s, %(dataAtualizacaoPncp)s, %(dataPublicacaoPncp)s,
                %(dataAberturaPropostaPncp)s, %(dataEncerramentoPropostaPncp)s, %(contratacaoExcluida)s
            ) ON DUPLICATE KEY UPDATE
                numeroControlePNCP = VALUES(numeroControlePNCP),
                anoCompraPncp = VALUES(anoCompraPncp),
                sequencialCompraPncp = VALUES(sequencialCompraPncp);
            """

            for item in data:
                # Converter campos de data
                for date_field in [
                    'dataInclusaoPncp', 'dataAtualizacaoPncp', 'dataPublicacaoPncp',
                    'dataAberturaPropostaPncp', 'dataEncerramentoPropostaPncp'
                ]:
                    if item[date_field]:
                        item[date_field] = parse_datetime(item[date_field])

                # Converter booleanos para 0/1 (compatível com MariaDB)
                for bool_field in ['srp', 'existeResultado', 'contratacaoExcluida']:
                    item[bool_field] = 1 if item[bool_field] else 0

                cursor.execute(insert_query, item)

        connection.commit()
        print(f"{len(data)} registros inseridos/atualizados com sucesso!")
    finally:
        connection.close()

if __name__ == "__main__":
    insert_compras_from_json('/home/quirino/Documentos/github/etp_nuvem_ifsp/contratacoes_geral/geral_2021_6_raw.json')