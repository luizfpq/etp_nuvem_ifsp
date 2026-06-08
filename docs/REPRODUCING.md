# Instruções de Reprodução

Este documento descreve como reproduzir integralmente os resultados do estudo.

## Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Conexão à internet (API PNCP é pública, sem autenticação)
- LaTeX (para compilar o artigo): texlive-full ou equivalente

## 1. Ambiente

```bash
git clone https://github.com/luizfpq/etp_nuvem_ifsp.git
cd etp_nuvem_ifsp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Coleta de Dados

O script `src/coletar_pncp.py` coleta dados diretamente da API REST do PNCP.

### Coletar apenas contratações relacionadas a nuvem

```bash
python src/coletar_pncp.py \
  --ano-inicio 2022 \
  --ano-fim 2026 \
  --output data/contratacoes_mec_nuvem.csv
```

### Coletar todas as contratações do MEC (para análise de proporção)

```bash
python src/coletar_pncp.py \
  --ano-inicio 2022 \
  --ano-fim 2026 \
  --todas \
  --output data/contratacoes_mec_todas.csv
```

### Parâmetros

| Parâmetro | Descrição | Padrão |
|---|---|---|
| `--ano-inicio` | Ano inicial da coleta | 2022 |
| `--ano-fim` | Ano final da coleta | Ano corrente |
| `--output` | Caminho do arquivo CSV de saída | `data/contratacoes_mec.csv` |
| `--todas` | Salva todas as contratações (não só nuvem) | Desativado |

### Tempo estimado

A coleta completa (2022-2026, todas as modalidades) leva de 4 a 8 horas dependendo da latência da API. A API do PNCP não requer autenticação, mas impõe tamanho mínimo de página (10) e aceita no máximo 50 resultados por request.

### Termos de busca para "nuvem"

O script classifica como relacionado a nuvem qualquer processo cujo campo `objetoCompra` ou `informacaoComplementar` contenha ao menos um dos seguintes termos (case-insensitive):

```
nuvem, cloud, aws, azure, gcp, google cloud, iaas, paas, saas,
hosting, hospedagem, datacenter virtual, microsoft 365, office 365,
oracle cloud, oci, servidor virtual, vps, armazenamento em nuvem,
backup em nuvem
```

## 3. Dados de Entrada

### Lista de autarquias do MEC

O arquivo `data/uasgs_raw_data.json` contém a lista de 195 autarquias vinculadas ao MEC, obtida via API de dados abertos (endpoint `consultarOrgao` com `cnpjCpfOrgaoVinculado=00394445000101`).

Para atualizar essa lista:

```bash
python scripts/legacy/get_uasg.py
mv uasgs_raw_data.json data/
```

## 4. API PNCP — Referência

- Base URL: `https://pncp.gov.br/api/consulta/v1`
- Endpoint de contratações: `GET /contratacoes/publicacao`
- Parâmetros obrigatórios: `dataInicial`, `dataFinal`, `codigoModalidadeContratacao`
- Paginação: `pagina` (1-indexed), `tamanhoPagina` (10, 20 ou 50)
- Sem autenticação
- Rate limit: não documentado oficialmente; o script usa delay de 1s entre requests

### Modalidades

| Código | Nome |
|---|---|
| 4 | Concorrência Eletrônica |
| 5 | Concorrência Presencial |
| 6 | Pregão Eletrônico |
| 7 | Pregão Presencial |
| 8 | Dispensa |
| 9 | Inexigibilidade |
| 12 | Credenciamento |

## 5. Compilar o Artigo

```bash
cd paper/
# Baixar template SBC (se ainda não tiver)
# wget https://www.sbc.org.br/documentos-da-sbc/category/169-templates-para-artigos-e-capitulos-de-livros
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## 6. Notas sobre Reprodutibilidade

- Os dados do PNCP são dinâmicos: novos processos são publicados continuamente. Resultados exatos dependem da data da coleta.
- O arquivo CSV gerado inclui coluna `data_publicacao` que permite filtrar por período.
- Os dados brutos de coletas anteriores (formato JSON por CNPJ/ano/modalidade) estão preservados em `data/raw/contratacoes_json/` para referência.
- Scripts da versão anterior do projeto estão em `scripts/legacy/` e usam uma API diferente (`dadosabertos.compras.gov.br`). O script atual (`src/coletar_pncp.py`) usa a API oficial `pncp.gov.br/api/consulta/v1`.

## 7. Ética e Dados

- Todos os dados são públicos, disponibilizados pelo Governo Federal via PNCP (art. 174, Lei 14.133/2021)
- Nenhum dado pessoal é coletado ou processado
- Dispensado de apreciação por comitê de ética (Res. CNS 510/2016, art. 1, par. único, incisos II e III)
