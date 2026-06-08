# Panorama das Contratações de Serviços de Computação em Nuvem nas Autarquias Federais do Ministério da Educação

Repositório de dados, código e artigo referentes ao estudo exploratório-descritivo sobre as práticas de contratação de serviços de computação em nuvem pelas autarquias federais vinculadas ao Ministério da Educação (MEC), com base em dados públicos do Portal Nacional de Contratações Públicas (PNCP).

## Estrutura do Repositório

```
.
├── src/                        # Script principal de coleta (API PNCP v1)
│   └── coletar_pncp.py
├── scripts/                    # Scripts auxiliares e versão anterior
│   ├── database/               # Criação de tabelas e ingestão
│   ├── get_contratacoes_*.py   # Coleta legada (Compras.gov.br)
│   └── get_uasg.py             # Atualização da lista de autarquias
├── data/                       # Dados
│   ├── uasgs_raw_data.json     # Lista de 196 CNPJs das autarquias MEC
│   └── raw/                    # Dados brutos de coletas anteriores (JSON)
├── relatorio/                  # Artigo LaTeX (template SBC)
│   ├── main.tex
│   ├── references.bib
│   └── sbc-template.sty
├── docs/                       # Documentação complementar
│   └── REPRODUCING.md          # Instruções de reprodução
├── requirements.txt            # Dependências Python
├── .gitignore
├── LICENSE
└── README.md
```

## Requisitos

- Python 3.10+
- `pip install -r requirements.txt`
- Conexão à internet (API PNCP pública, sem autenticação)
- texlive-full (para compilar o relatório)

## Uso Rápido

```bash
git clone git@github.com:luizfpq/etp_nuvem_ifsp.git
cd etp_nuvem_ifsp
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Coletar contratações de nuvem (2022-2026)
python src/coletar_pncp.py --ano-inicio 2022 --output data/contratacoes_mec_nuvem.csv

# Coletar TODAS (para análise de proporção)
python src/coletar_pncp.py --ano-inicio 2022 --todas --output data/contratacoes_mec_todas.csv
```

Consulte [docs/REPRODUCING.md](docs/REPRODUCING.md) para instruções detalhadas.

## Fonte de Dados

API REST do PNCP (Portal Nacional de Contratações Públicas), conforme art. 174 da Lei 14.133/2021. Todos os dados são públicos, sem autenticação.

- Base URL: `https://pncp.gov.br/api/consulta/v1`
- Recorte: 196 autarquias vinculadas ao MEC (universidades, IFs, fundações)

## Autores

- Luiz Fernando Postingel Quirino (IFSP/CCETI-DTI) — luiz.quirino@ifsp.edu.br

## Licença

Código: [MIT](LICENSE) | Dados e artigo: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## Citação

```bibtex
@article{quirino2026nuvem,
  author  = {Quirino, Luiz Fernando Postingel},
  title   = {Panorama das Contratações de Serviços de Computação em Nuvem nas Autarquias Federais do Ministério da Educação},
  year    = {2026},
  note    = {CCETI-DTI/IFSP. Repositório: https://github.com/luizfpq/etp_nuvem_ifsp}
}
```
