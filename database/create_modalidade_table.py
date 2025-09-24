# database/create_modalidade_table.py
import pymysql
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()

# Configuração segura da porta
db_port = os.getenv('DB_PORT', '3306')
try:
    db_port = int(db_port)
except ValueError:
    raise ValueError("DB_PORT no .env deve ser um número inteiro (ex: 3306)")

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': db_port,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Dados de referência das modalidades
MODALIDADES = [
    (1, 'Leilão - Eletrônico', ''),
    (2, 'Diálogo Competitivo', ''),
    (3, 'Concurso', ''),
    (4, 'Concorrência - Eletrônica', ''),
    (5, 'Concorrência - Presencial', ''),
    (6, 'Pregão - Eletrônico', ''),
    (7, 'Pregão - Presencial', ''),
    (8, 'Dispensa', ''),
    (9, 'Inexigibilidade', ''),
    (10, 'Manifestação de Interesse', ''),
    (11, 'Pré-qualificação', ''),
    (12, 'Credenciamento', ''),
    (13, 'Leilão - Presencial', 'Modalidade de licitação realizada sob a forma presencial para alienação de bens imóveis ou de bens móveis inservíveis ou legalmente apreendidos a quem oferecer o maior lance'),
    (14, 'Inaplicabilidade da Licitação', 'Situação em que, por especificidades da legislação ou natureza da atividade, não se exige o processo licitatório. Refere-se aos casos em que a lei determina que a licitação não é aplicável, seja pela natureza única do objeto ou pela impossibilidade de competição.')
]

def create_and_populate_modalidade_table():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 1. Criar tabela
            create_table_query = """
            CREATE TABLE IF NOT EXISTS modalidade_contratacao (
                codigo INT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                descricao TEXT,
                ativo BOOLEAN NOT NULL DEFAULT TRUE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            cursor.execute(create_table_query)

            # 2. Inserir ou atualizar dados
            insert_query = """
            INSERT INTO modalidade_contratacao (codigo, nome, descricao, ativo)
            VALUES (%s, %s, %s, TRUE)
            ON DUPLICATE KEY UPDATE
                nome = VALUES(nome),
                descricao = VALUES(descricao),
                ativo = VALUES(ativo);
            """
            cursor.executemany(insert_query, MODALIDADES)

        connection.commit()
        print(f"Tabela 'modalidade_contratacao' criada e populada com {len(MODALIDADES)} registros!")
    finally:
        connection.close()

if __name__ == "__main__":
    create_and_populate_modalidade_table()