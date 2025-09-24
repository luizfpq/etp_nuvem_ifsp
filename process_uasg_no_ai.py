import json

# Caminho para o arquivo principal
INPUT_FILE = "uasgs_raw_data.json"
OUTPUT_FILE = "autarquias_mec.json"

def filtrar_autarquias_mec():
    # palavras-chave para identificação
    palavras_chave = [
        "UNIVERSIDADE FEDERAL",
        "INSTITUTO FEDERAL",
        "ESCOLA TÉCNICA FEDERAL",
        "ESCOLA AGROTÉCNICA FEDERAL",
        "COLÉGIO PEDRO II"
    ]
    
    resultado = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        dados = json.load(f)

        for orgao in dados:
            nome = (orgao.get("nomeOrgao") or "").upper()
            tipo = (orgao.get("nomeTipoAdministracao") or "").upper()
            vinculo = (orgao.get("nomeOrgaoVinculado") or "").upper()

            if (any(pk in nome for pk in palavras_chave)
                and "MINISTERIO DA EDUCACAO" in vinculo
                and tipo == "AUTARQUIA"):
                
                resultado.append({
                    "codigoOrgao": orgao.get("codigoOrgao"),
                    "nomeOrgao": orgao.get("nomeOrgao"),
                    "sigla": orgao.get("nomeMnemonicoOrgao"),
                    "cnpj": orgao.get("cnpjCpfOrgao"),
                    "tipo": "Autarquia Federal de Educação",
                    "orgaoVinculado": orgao.get("nomeOrgaoVinculado")
                })
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(resultado, out, ensure_ascii=False, indent=2)
    
    print(f"Extração concluída. {len(resultado)} órgãos salvos em {OUTPUT_FILE}.")

if __name__ == "__main__":
    filtrar_autarquias_mec()
