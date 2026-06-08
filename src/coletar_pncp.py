"""
coletar_pncp.py — Coleta de contratações do PNCP (API v1) para autarquias do MEC.

Estratégia: itera por modalidade + janela temporal mensal, filtra client-side
pelos CNPJs das autarquias vinculadas ao MEC. Salva CSV consolidado.

Uso:
    python coletar_pncp.py [--ano-inicio 2022] [--ano-fim 2026] [--output data/contratacoes_mec.csv]
"""

import argparse
import csv
import json
import time
from datetime import date, timedelta
from pathlib import Path

import requests

BASE_URL = "https://pncp.gov.br/api/consulta/v1"
MODALIDADES = [4, 5, 6, 7, 8, 9, 12]  # Concorrência, Pregão, Dispensa, Inexigibilidade, Credenciamento
PAGE_SIZE = 50
DELAY = 1.0  # segundos entre requests

TERMOS_NUVEM = [
    "nuvem", "cloud", "aws", "azure", "gcp", "google cloud",
    "iaas", "paas", "saas", "hosting", "hospedagem",
    "datacenter virtual", "microsoft 365", "office 365",
    "oracle cloud", "oci", "servidor virtual", "vps",
    "armazenamento em nuvem", "backup em nuvem",
]

CAMPOS_CSV = [
    "cnpj_orgao", "razao_social", "esfera", "poder",
    "uf", "municipio", "unidade", "codigo_unidade",
    "ano_compra", "sequencial", "numero_compra", "processo",
    "modalidade_id", "modalidade_nome", "modo_disputa",
    "objeto_compra", "informacao_complementar",
    "amparo_legal_nome", "amparo_legal_descricao",
    "valor_estimado", "valor_homologado",
    "situacao", "srp",
    "data_publicacao", "data_abertura", "data_encerramento",
    "numero_controle_pncp", "fontes_orcamentarias",
    "match_nuvem",
]


def carregar_cnpjs_mec(path: str = "data/uasgs_raw_data.json") -> set:
    """Carrega lista de CNPJs das autarquias do MEC."""
    with open(path, "r", encoding="utf-8") as f:
        uasgs = json.load(f)
    return {u.get("cnpjCpfOrgao", "").replace(".", "").replace("/", "").replace("-", "") for u in uasgs if u.get("cnpjCpfOrgao")}


def gerar_janelas_mensais(ano_inicio: int, ano_fim: int):
    """Gera pares (data_inicio, data_fim) por mês."""
    d = date(ano_inicio, 1, 1)
    fim = min(date(ano_fim, 12, 31), date.today())
    while d <= fim:
        proximo_mes = (d.replace(day=28) + timedelta(days=4)).replace(day=1)
        ultimo_dia = min(proximo_mes - timedelta(days=1), fim)
        yield d.strftime("%Y%m%d"), ultimo_dia.strftime("%Y%m%d")
        d = proximo_mes


def buscar_pagina(modalidade: int, data_ini: str, data_fim: str, pagina: int) -> dict | None:
    """Faz uma requisição paginada ao PNCP."""
    params = {
        "dataInicial": data_ini,
        "dataFinal": data_fim,
        "codigoModalidadeContratacao": modalidade,
        "pagina": pagina,
        "tamanhoPagina": PAGE_SIZE,
    }
    for tentativa in range(3):
        try:
            r = requests.get(f"{BASE_URL}/contratacoes/publicacao", params=params, timeout=60)
            if r.status_code == 200:
                return r.json()
            if r.status_code == 429:
                time.sleep(10)
                continue
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"  [ERRO] tentativa {tentativa+1}: {e}")
            time.sleep(5)
    return None


def extrair_registro(item: dict) -> dict:
    """Extrai campos planos de um registro da API."""
    orgao = item.get("orgaoEntidade", {})
    unidade = item.get("unidadeOrgao", {})
    amparo = item.get("amparoLegal", {})
    fontes = item.get("fontesOrcamentarias", [])

    texto = f"{item.get('objetoCompra', '')} {item.get('informacaoComplementar', '')}".lower()
    match = [t for t in TERMOS_NUVEM if t in texto]

    return {
        "cnpj_orgao": orgao.get("cnpj", ""),
        "razao_social": orgao.get("razaoSocial", ""),
        "esfera": orgao.get("esferaId", ""),
        "poder": orgao.get("poderId", ""),
        "uf": unidade.get("ufSigla", ""),
        "municipio": unidade.get("municipioNome", ""),
        "unidade": unidade.get("nomeUnidade", ""),
        "codigo_unidade": unidade.get("codigoUnidade", ""),
        "ano_compra": item.get("anoCompra", ""),
        "sequencial": item.get("sequencialCompra", ""),
        "numero_compra": item.get("numeroCompra", ""),
        "processo": item.get("processo", ""),
        "modalidade_id": item.get("modalidadeId", ""),
        "modalidade_nome": item.get("modalidadeNome", ""),
        "modo_disputa": item.get("modoDisputaNome", ""),
        "objeto_compra": item.get("objetoCompra", ""),
        "informacao_complementar": item.get("informacaoComplementar", ""),
        "amparo_legal_nome": amparo.get("nome", ""),
        "amparo_legal_descricao": amparo.get("descricao", ""),
        "valor_estimado": item.get("valorTotalEstimado", ""),
        "valor_homologado": item.get("valorTotalHomologado", ""),
        "situacao": item.get("situacaoCompraNome", ""),
        "srp": item.get("srp", ""),
        "data_publicacao": item.get("dataPublicacaoPncp", ""),
        "data_abertura": item.get("dataAberturaProposta", ""),
        "data_encerramento": item.get("dataEncerramentoProposta", ""),
        "numero_controle_pncp": item.get("numeroControlePNCP", ""),
        "fontes_orcamentarias": "; ".join(f.get("nome", "") for f in fontes),
        "match_nuvem": "; ".join(match) if match else "",
    }


def main():
    parser = argparse.ArgumentParser(description="Coleta contratações PNCP — autarquias MEC")
    parser.add_argument("--ano-inicio", type=int, default=2022)
    parser.add_argument("--ano-fim", type=int, default=date.today().year)
    parser.add_argument("--output", type=str, default="data/contratacoes_mec.csv")
    parser.add_argument("--todas", action="store_true", help="Salva TODAS as contratações do MEC, não só nuvem")
    args = parser.parse_args()

    cnpjs_mec = carregar_cnpjs_mec()
    print(f"CNPJs do MEC carregados: {len(cnpjs_mec)}")

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    total = 0
    nuvem = 0

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS_CSV)
        writer.writeheader()

        for modalidade in MODALIDADES:
            for data_ini, data_fim in gerar_janelas_mensais(args.ano_inicio, args.ano_fim):
                pagina = 1
                total_paginas = 1

                while pagina <= total_paginas:
                    resp = buscar_pagina(modalidade, data_ini, data_fim, pagina)
                    if not resp:
                        break

                    if pagina == 1:
                        total_paginas = resp.get("totalPaginas", 0)
                        if total_paginas == 0:
                            break

                    for item in resp.get("data", []):
                        cnpj = item.get("orgaoEntidade", {}).get("cnpj", "")
                        if cnpj not in cnpjs_mec:
                            continue

                        registro = extrair_registro(item)
                        total += 1

                        if registro["match_nuvem"]:
                            nuvem += 1

                        if args.todas or registro["match_nuvem"]:
                            writer.writerow(registro)

                    pagina += 1
                    time.sleep(DELAY)

                # Log de progresso
                if total_paginas > 0:
                    print(f"  mod={modalidade} periodo={data_ini}-{data_fim} paginas={total_paginas} mec_total={total} nuvem={nuvem}")

    print(f"\nColeta finalizada. Total MEC: {total} | Com termo nuvem: {nuvem}")
    print(f"Arquivo: {args.output}")


if __name__ == "__main__":
    main()
