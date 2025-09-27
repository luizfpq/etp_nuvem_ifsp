import requests
import json
import time

def fetch_all_pages_data(base_url):
    """
    Busca todos os dados retornados(considerando a paginação) do endpoint e gera um arquivo json.
    """
    all_results = []
    page_number = 1
    total_pages = 1  # Start with 1 to enter the loop

    while page_number <= total_pages:
        url = f"{base_url}&pagina={page_number}"
        print(f"Buscando página {page_number} de {total_pages}...")

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Update total_pages from the first response
            if page_number == 1:
                total_pages = data.get('totalPaginas', 1)

            results = data.get('resultado', [])
            all_results.extend(results)
            
            print(f"Página {page_number} obtida com sucesso. Total de resultados até agora: {len(all_results)}")
            
            page_number += 1
            time.sleep(1)  # Adiciona um pequeno atraso para não sobrecarregar o servidor
        
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a URL {url}: {e}")
            break
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON da URL {url}: {e}")
            break
    
    return all_results

def main():
    base_url = "https://dadosabertos.compras.gov.br/modulo-uasg/2_consultarOrgao?pagina=1&cnpjCpfOrgaoVinculado=00394445000101&statusOrgao=true"
    print("Iniciando a requisição para a URL e processando o JSON...")
    
    all_uasg_data = fetch_all_pages_data(base_url)

    if all_uasg_data:
        file_path = "uasgs_raw_data.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(all_uasg_data, f, ensure_ascii=False, indent=4)
        print(f"\nDados de {len(all_uasg_data)} UASGs salvos em {file_path}")
    else:
        print("Não foi possível obter os dados da API.")

if __name__ == "__main__":
    main()