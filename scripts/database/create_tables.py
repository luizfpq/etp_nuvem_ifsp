import pymysql
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

def create_table_itens_contratacoes():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            create_table_query = """
                CREATE TABLE itens_contratacoes (
                    idCompra VARCHAR(255),
                    idCompraItem VARCHAR(255) PRIMARY KEY,
                    idContratacaoPNCP VARCHAR(255),
                    unidadeOrgaoCodigoUnidade VARCHAR(255),
                    orgaoEntidadeCnpj VARCHAR(14),
                    numeroItemPncp INTEGER,
                    numeroItemCompra INTEGER,
                    numeroGrupo INTEGER,
                    descricaoResumida TEXT,
                    materialOuServico VARCHAR(1),
                    materialOuServicoNome VARCHAR(50),
                    codigoClasse INTEGER,
                    codigoGrupo INTEGER,
                    codItemCatalogo INTEGER,
                    descricaodetalhada TEXT,
                    unidadeMedida VARCHAR(50),
                    orcamentoSigiloso BOOLEAN,
                    itemCategoriaIdPncp INTEGER,
                    itemCategoriaNome VARCHAR(255),
                    criterioJulgamentoIdPncp INTEGER,
                    criterioJulgamentoNome VARCHAR(255),
                    situacaoCompraItem VARCHAR(10),
                    situacaoCompraItemNome VARCHAR(255),
                    tipoBeneficio VARCHAR(10),
                    tipoBeneficioNome VARCHAR(255),
                    incentivoProdutivoBasico BOOLEAN,
                    quantidade INTEGER,
                    valorUnitarioEstimado NUMERIC(18, 2),
                    valorTotal NUMERIC(18, 2),
                    temResultado BOOLEAN,
                    codFornecedor VARCHAR(14),
                    nomeFornecedor VARCHAR(255),
                    quantidadeResultado INTEGER,
                    valorUnitarioResultado NUMERIC(18, 2),
                    valorTotalResultado NUMERIC(18, 2),
                    dataInclusaoPncp TIMESTAMP,
                    dataAtualizacaoPncp TIMESTAMP,
                    dataResultado TIMESTAMP,
                    margemPreferenciaNormal BOOLEAN,
                    percentualMargemPreferenciaNormal NUMERIC(5, 2),
                    margemPreferenciaAdicional BOOLEAN,
                    percentualMargemPreferenciaAdicional NUMERIC(5, 2),
                    codigoNCM VARCHAR(255),
                    descricaoNCM TEXT,
                    numeroControlePNCPCompra VARCHAR(255)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            cursor.execute(create_table_query)
        connection.commit()
        print("Tabela 'itens_contratacoes' criada com sucesso!")
    finally:
        connection.close()

def create_table_compras_pncp():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS compras_pncp (
                idCompra VARCHAR(50) PRIMARY KEY,
                numeroControlePNCP VARCHAR(100),
                anoCompraPncp INT,
                sequencialCompraPncp INT,
                orgaoEntidadeCnpj VARCHAR(14),
                orgaoSubrogadoCnpj VARCHAR(14),
                codigoOrgao INT,
                orgaoEntidadeRazaoSocial VARCHAR(255),
                orgaoSubrogadoRazaoSocial VARCHAR(255),
                orgaoEntidadeEsferaId CHAR(1),
                orgaoSubrogadoEsferaId CHAR(1),
                orgaoEntidadePoderId CHAR(1),
                orgaoSubrogadoPoderId CHAR(1),
                unidadeOrgaoCodigoUnidade VARCHAR(20),
                unidadeSubrogadaCodigoUnidade VARCHAR(20),
                unidadeOrgaoNomeUnidade VARCHAR(255),
                unidadeSubrogadaNomeUnidade VARCHAR(255),
                unidadeOrgaoUfSigla CHAR(2),
                unidadeSubrogadaUfSigla CHAR(2),
                unidadeOrgaoMunicipioNome VARCHAR(100),
                unidade_subrogada_municipio_nome VARCHAR(100),
                unidadeOrgaoCodigoIbge INT,
                unidadeSubrogadaCodigoIbge INT,
                numeroCompra VARCHAR(20),
                modalidadeIdPncp INT,
                codigoModalidade INT,
                modalidadeNome VARCHAR(100),
                srp BOOLEAN,
                modoDisputaIdPncp INT,
                codigoModoDisputa INT,
                amparoLegalCodigoPncp INT,
                amparoLegalNome VARCHAR(255),
                amparoLegalDescricao TEXT,
                informacaoComplementar TEXT,
                processo VARCHAR(50),
                objetoCompra TEXT,
                existeResultado BOOLEAN,
                orcamentoSigilosoCodigo INT,
                orcamentoSigilosoDescricao VARCHAR(100),
                situacaoCompraIdPncp INT,
                situacaoCompraNomePncp VARCHAR(100),
                tipoInstrumentoConvocatorioCodigoPncp INT,
                tipoInstrumentoConvocatorioNome VARCHAR(100),
                modoDisputaNomePncp VARCHAR(50),
                valorTotalEstimado DECIMAL(15,2),
                valorTotalHomologado DECIMAL(15,2),
                dataInclusaoPncp DATETIME,
                dataAtualizacaoPncp DATETIME,
                dataPublicacaoPncp DATETIME,
                dataAberturaPropostaPncp DATETIME,
                dataEncerramentoPropostaPncp DATETIME,
                contratacaoExcluida BOOLEAN
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            cursor.execute(create_table_query)
        connection.commit()
        print("Tabela 'compras_pncp' criada com sucesso!")
    finally:
        connection.close()

def create_table_uasg():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            create_query = """
            CREATE TABLE IF NOT EXISTS uasg (
                codigoOrgao INT PRIMARY KEY,
                nomeOrgao VARCHAR(255),
                nomeMnemonicoOrgao VARCHAR(50),
                cnpjCpfOrgao VARCHAR(14),
                codigoOrgaoVinculado INT,
                cnpjCpfOrgaoVinculado VARCHAR(14),
                nomeOrgaoVinculado VARCHAR(255),
                codigoOrgaoSuperior INT,
                cnpjCpfOrgaoSuperior VARCHAR(14),
                nomeOrgaoSuperior VARCHAR(255),
                codigoTipoAdministracao INT,
                nomeTipoAdministracao VARCHAR(100),
                poder CHAR(1),
                esfera CHAR(1),
                usoSisg BOOLEAN,
                statusOrgao BOOLEAN,
                dataHoraMovimento DATETIME
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            cursor.execute(create_query)
        connection.commit()
        print("Tabela 'uasg' criada com sucesso!")
    finally:
        connection.close()

if __name__ == "__main__":
    create_table_compras_pncp()
    create_table_uasg()
    create_table_itens_contratacoes()
