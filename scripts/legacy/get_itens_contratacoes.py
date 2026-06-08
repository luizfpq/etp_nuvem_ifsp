import os
import requests
import json
import time
import threading
import queue
import pymysql.cursors
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configuração do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT')),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Configurações para a API
BASE_URL = "https://dadosabertos.compras.gov.br/modulo-contratacoes/2.1_consultarItensContratacoes_PNCP_14133_Id"
HEADERS = {"Accept": "application/json"}
TIMEOUT = 180
MAX_RETRIES = 3

# Cria uma fila para as tarefas e um lock para o banco de dados
id_compra_queue = queue.Queue()
db_lock = threading.Lock()

def get_all_id_compras():
    """
    Busca todos os idCompra da tabela compras_pncp.
    """
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # Seleciona apenas idCompra que não foram processados ou estão ausentes
            query = """
            SELECT idCompra FROM compras_pncp
            WHERE idCompra NOT IN (SELECT DISTINCT idCompra FROM itens_contratacoes)
            """
            cursor.execute(query)
            result = cursor.fetchall()
            return [row['idCompra'] for row in result]
    finally:
        connection.close()

def insert_itens_contratacoes(data):
    """
    Insere os dados dos itens de contratação na tabela itens_contratacoes.
    Usa um lock para garantir que a inserção seja thread-safe.
    """
    if not data:
        return
        
    with db_lock:
        connection = pymysql.connect(**DB_CONFIG)
        try:
            with connection.cursor() as cursor:
                for item in data:
                    try:
                        sql = """
                        INSERT INTO itens_contratacoes (
                            idCompra, idCompraItem, idContratacaoPNCP, unidadeOrgaoCodigoUnidade, 
                            orgaoEntidadeCnpj, numeroItemPncp, numeroItemCompra, numeroGrupo, 
                            descricaoResumida, materialOuServico, materialOuServicoNome, 
                            codigoClasse, codigoGrupo, codItemCatalogo, descricaodetalhada, 
                            unidadeMedida, orcamentoSigiloso, itemCategoriaIdPncp, itemCategoriaNome, 
                            criterioJulgamentoIdPncp, criterioJulgamentoNome, situacaoCompraItem, 
                            situacaoCompraItemNome, tipoBeneficio, tipoBeneficioNome, 
                            incentivoProdutivoBasico, quantidade, valorUnitarioEstimado, 
                            valorTotal, temResultado, codFornecedor, nomeFornecedor, 
                            quantidadeResultado, valorUnitarioResultado, valorTotalResultado, 
                            dataInclusaoPncp, dataAtualizacaoPncp, dataResultado, 
                            margemPreferenciaNormal, percentualMargemPreferenciaNormal, 
                            margemPreferenciaAdicional, percentualMargemPreferenciaAdicional, 
                            codigoNCM, descricaoNCM, numeroControlePNCPCompra
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            idCompra = VALUES(idCompra),
                            idContratacaoPNCP = VALUES(idContratacaoPNCP),
                            dataAtualizacaoPncp = VALUES(dataAtualizacaoPncp);
                        """
                        cursor.execute(sql, (
                            item.get('idCompra'), item.get('idCompraItem'), item.get('idContratacaoPNCP'), 
                            item.get('unidadeOrgaoCodigoUnidade'), item.get('orgaoEntidadeCnpj'), 
                            item.get('numeroItemPncp'), item.get('numeroItemCompra'), item.get('numeroGrupo'), 
                            item.get('descricaoResumida'), item.get('materialOuServico'), 
                            item.get('materialOuServicoNome'), item.get('codigoClasse'), 
                            item.get('codigoGrupo'), item.get('codItemCatalogo'), item.get('descricaodetalhada'), 
                            item.get('unidadeMedida'), item.get('orcamentoSigiloso'), item.get('itemCategoriaIdPncp'), 
                            item.get('itemCategoriaNome'), item.get('criterioJulgamentoIdPncp'), 
                            item.get('criterioJulgamentoNome'), item.get('situacaoCompraItem'), 
                            item.get('situacaoCompraItemNome'), item.get('tipoBeneficio'), 
                            item.get('tipoBeneficioNome'), item.get('incentivoProdutivoBasico'), 
                            item.get('quantidade'), item.get('valorUnitarioEstimado'), 
                            item.get('valorTotal'), item.get('temResultado'), item.get('codFornecedor'), 
                            item.get('nomeFornecedor'), item.get('quantidadeResultado'), 
                            item.get('valorUnitarioResultado'), item.get('valorTotalResultado'), 
                            item.get('dataInclusaoPncp'), item.get('dataAtualizacaoPncp'), 
                            item.get('dataResultado'), item.get('margemPreferenciaNormal'), 
                            item.get('percentualMargemPreferenciaNormal'), 
                            item.get('margemPreferenciaAdicional'), 
                            item.get('percentualMargemPreferenciaAdicional'), 
                            item.get('codigoNCM'), item.get('descricaoNCM'), item.get('numeroControlePNCPCompra')
                        ))
                    except Exception as e:
                        print(f"Erro ao inserir item {item.get('idCompraItem')}: {e}")
                
            connection.commit()
            print(f"  -> {len(data)} itens inseridos ou atualizados com sucesso.")
        finally:
            connection.close()


def worker():
    """
    Função de trabalhador para o pool de threads.
    Pega um idCompra da fila e o processa.
    """
    while True:
        try:
            id_compra = id_compra_queue.get(timeout=1)
        except queue.Empty:
            break

        print(f"Processando idCompra: {id_compra}")
        
        retries = 0
        success = False
        while retries < MAX_RETRIES and not success:
            try:
                params = {"tipo": "idCompra", "codigo": id_compra}
                response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=TIMEOUT)
                response.raise_for_status()
                data = response.json()
                
                if data.get('resultado'):
                    insert_itens_contratacoes(data['resultado'])
                else:
                    print(f"  Aviso: Nenhum item encontrado para o idCompra {id_compra}")
                
                success = True
            
            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout) as e:
                retries += 1
                print(f"  Aviso: Erro de timeout para {id_compra} ({e}). Tentativa {retries}/{MAX_RETRIES}...")
                time.sleep(10)
            except requests.exceptions.RequestException as e:
                print(f"  Erro HTTP para {id_compra}: {e}")
                break
            except json.JSONDecodeError as e:
                print(f"  Erro ao decodificar JSON para {id_compra}: {e}")
                break
            except Exception as e:
                print(f"  Erro inesperado para {id_compra}: {e}")
                break
        
        if not success:
            print(f"  Falha ao processar {id_compra} após {MAX_RETRIES} tentativas. Pulando.")
            
        id_compra_queue.task_done()
        time.sleep(1) # Pequena pausa entre as requisições para evitar sobrecarga

def main():
    """
    Função principal para orquestrar o processo.
    """
    id_compras = get_all_id_compras()
    if not id_compras:
        print("Nenhum novo idCompra encontrado para processar. Finalizando.")
        return

    print(f"Encontrados {len(id_compras)} idCompra para processar.")

    # Adiciona os IDs na fila
    for id_compra in id_compras:
        id_compra_queue.put(id_compra)
    
    threads = []
    num_threads = 2 # Defina o número de threads desejado
    
    for i in range(num_threads):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads.append(t)
    
    id_compra_queue.join()
    
    print("\nProcessamento de todos os idCompra concluído.")
    
if __name__ == "__main__":
    main()