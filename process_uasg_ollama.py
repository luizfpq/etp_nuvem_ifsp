import os  # Adicione esta linha
import json
import ollama

def is_federal_institution_ollama(text, model_name="phi3"):
    """
    Uses a local LLM via Ollama to check if the text mentions a federal
    university or institute.
    """
    prompt = f"""
    A descrição é de uma universidade federal ou de um instituto federal?
    Responda apenas 'SIM' ou 'NAO'.
    
    Descrição: {text}
    """
    
    try:
        response = ollama.chat(model=model_name, messages=[
            {
                'role': 'system',
                'content': 'Você é um assistente que identifica institutos federais e universidades federais, sendo focada nas autarquias do MEC. Responda apenas "SIM" ou "NAO".'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ])
        
        response_text = response['message']['content'].strip().upper()
        return 'SIM' in response_text

    except Exception as e:
        print(f"Erro ao chamar o Ollama para '{text}': {e}")
        return False

def main():
    """
    Main function to process UASG data with a local LLM.
    """
    file_path = "uasgs_raw_data.json"
    
    if not os.path.exists(file_path):
        print(f"Erro: O arquivo de dados '{file_path}' não foi encontrado. Execute o script 'get_uasg.py' primeiro.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        all_uasg_data = json.load(f)

    print(f"Processando {len(all_uasg_data)} órgãos com o Ollama...")
    federal_institutions = []
    
    for orgao in all_uasg_data:
        description = orgao.get('nomeOrgao')
        if description and is_federal_institution_ollama(description):
            uasg_code = orgao.get('codigoOrgao')
            federal_institutions.append({'uasg_code': uasg_code, 'description': description})
            print(f"Identificado: {uasg_code} - {description}")

    if federal_institutions:
        result_file = "uasgs_federais_ollama.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(federal_institutions, f, ensure_ascii=False, indent=4)
        print(f"\nResultados salvos em {result_file}.")
    else:
        print("Nenhuma universidade ou instituto federal foi encontrado.")

if __name__ == "__main__":
    main()