import os
import requests
import json
import time
from datetime import datetime

def fetch_and_save_contratacoes(uasg_code, year, modalidade_code, base_url, headers, timeout=60):
    """
    Fetches contracting data for a specific UASG, year, and modality from the API,
    handling pagination, and saves it to a JSON file.
    """
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    # For the current year, use today's date as the end date
    if year == datetime.now().year:
        end_date = datetime.now().strftime("%Y-%m-%d")

    params = {
        "cnpjCpfOrgao": uasg_code,
        "dataPublicacaoPncpInicial": start_date,
        "dataPublicacaoPncpFinal": end_date,
        "codigoModalidade": modalidade_code,
        "tamanhoPagina": 100,
        "pagina": 1
    }

    all_results = []
    total_pages = 1

    print(f"Buscando contratações para o órgão {uasg_code} no ano {year}, modalidade {modalidade_code}...")

    while params["pagina"] <= total_pages:
        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=timeout)
            print(response.url)
            response.raise_for_status()
            data = response.json()
            
            if data:
                if params["pagina"] == 1:
                    total_pages = data.get("totalPaginas", 1)
                
                results = data.get("resultado", [])
                all_results.extend(results)
                
                print(f"  Página {params['pagina']} de {total_pages} obtida. Total de contratações: {len(all_results)}")
                
                params["pagina"] += 1
                time.sleep(1) # Delay between pages
            else:
                print(f"  Sem dados para o órgão {uasg_code} no ano {year}, modalidade {modalidade_code}.")
                break

        except requests.exceptions.RequestException as e:
            print(f"  Erro ao acessar a API para o órgão {uasg_code} no ano {year}: {e}")
            break
        except json.JSONDecodeError as e:
            print(f"  Erro ao decodificar JSON para o órgão {uasg_code} no ano {year}: {e}")
            break
    
    if all_results:
        output_dir = "contratacoes"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        file_name = f"{uasg_code}_{year}_{modalidade_code}_raw.json"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=4)
        print(f"  Dados salvos em {file_path}")

def main():
    """
    Main function to orchestrate the fetching of contracting data.
    """
    uasg_data_file = "uasgs_raw_data.json"
    if not os.path.exists(uasg_data_file):
        print(f"Erro: O arquivo '{uasg_data_file}' não foi encontrado.")
        print("Por favor, execute o script de obtenção de UASGs primeiro.")
        return

    with open(uasg_data_file, 'r', encoding='utf-8') as f:
        uasgs_list = json.load(f)
    
    if not uasgs_list:
        print("Erro: O arquivo de dados das UASGs está vazio.")
        return

    base_url = "https://dadosabertos.compras.gov.br/modulo-contratacoes/1_consultarContratacoes_PNCP_14133"
    headers = {"Accept": "application/json"}
    
    current_year = datetime.now().year
    years_to_fetch = range(current_year - 1, current_year + 1) # varia os anos a partir do atual
    modalidade_codes = range(1, 15) # Codes from 1 to 14
    #modalidade_codes = [6, 8, 9, 11, 12] # Read dominios.md

    print(f"\nIniciando a busca por contratações para {len(uasgs_list)} órgãos nos anos de {min(years_to_fetch)} a {max(years_to_fetch)} para as modalidades de {min(modalidade_codes)} a {max(modalidade_codes)}.")
    
    for orgao in uasgs_list:
        uasg_code = orgao.get("cnpjCpfOrgao")
        if uasg_code:
            for year in years_to_fetch:
                for modalidade in modalidade_codes:
                    fetch_and_save_contratacoes(uasg_code, year, modalidade, base_url, headers)
                    time.sleep(2) # Delay between different UASG/Year/Modality combinations

if __name__ == "__main__":
    main()
