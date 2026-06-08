# Panorama das Contratações de Serviços de Computação em Nuvem nas Autarquias Federais do Ministério da Educação

Repositório de dados, código e artigo referentes ao estudo exploratório-descritivo sobre as práticas de contratação de serviços de computação em nuvem pelas autarquias federais vinculadas ao Ministério da Educação (MEC), com base em dados públicos do Portal Nacional de Contratações Públicas (PNCP).

## Resumo

Este estudo analisa as contratações de serviços de computação em nuvem realizadas pelas autarquias federais vinculadas ao MEC (universidades, institutos federais e fundações), extraindo dados diretamente da API REST do PNCP. A pesquisa identifica padrões de modalidade de contratação, concentração de fornecedores, tipos de serviço (IaaS/PaaS/SaaS) e aderência ao marco normativo da Lei 14.133/2021.

## Estrutura do Repositório

```
.
├── src/                        # Código-fonte principal
│   └── coletar_pncp.py        # Script de coleta via API PNCP (v1)
├── data/                       # Dados
│   ├── uasgs_raw_data.json     # Lista de CNPJs das autarquias MEC
│   └── raw/                    # Dados brutos de coletas anteriores
├── paper/                      # Artigo LaTeX
│   ├── main.tex                # Fonte do artigo
│   ├── references.bib          # Referências bibliográficas
│   └── assets/                 # Figuras e tabelas
├── scripts/legacy/             # Scripts da versão anterior (preservados)
├── requirements.txt            # Dependências Python
├── REPRODUCING.md              # Instruções de reprodução completas
└── README.md                   # Este arquivo
```

## Requisitos

- Python 3.10+
- Dependências: `pip install -r requirements.txt`
- Acesso à internet (API PNCP é pública, sem autenticação)

## Uso Rápido

```bash
# Clonar o repositório
git clone https://github.com/luizfpq/etp_nuvem_ifsp.git
cd etp_nuvem_ifsp

# Instalar dependências
pip install -r requirements.txt

# Coletar contratações de nuvem (2022-2026)
python src/coletar_pncp.py --ano-inicio 2022 --output data/contratacoes_mec_nuvem.csv

# Coletar TODAS as contratações do MEC (para análise completa)
python src/coletar_pncp.py --ano-inicio 2022 --todas --output data/contratacoes_mec_todas.csv
```

Consulte [REPRODUCING.md](REPRODUCING.md) para instruções detalhadas de reprodução.

## Fonte de Dados

Os dados são coletados da API REST do PNCP (Portal Nacional de Contratações Públicas), conforme art. 174 da Lei 14.133/2021. Todos os dados são públicos. Não há necessidade de autenticação.

- Base URL: `https://pncp.gov.br/api/consulta/v1`
- Endpoint principal: `GET /contratacoes/publicacao`
- Recorte institucional: 195 autarquias vinculadas ao MEC (universidades federais, institutos federais, fundações)

## Autores

- Luiz Fernando Postingel Quirino (UFMS/IFSP) — luiz.quirino@ufms.br
- [Orientador a definir]

## Publicações Relacionadas

- Gonçalves, R. H. S., Santos, W. M., & Quirino, L. F. P. (2026). Detecção de Irregularidades em Contratações Públicas: Uma Abordagem com Machine Learning Baseada em Consenso entre Algoritmos. *REGRASP*, 11(1), 253-268.

## Licença

Este projeto é disponibilizado sob licença [MIT](LICENSE) para o código e [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) para os dados e o artigo.

## Citação

```bibtex
@article{quirino2026nuvem,
  author  = {Quirino, Luiz Fernando Postingel},
  title   = {Panorama das Contratações de Serviços de Computação em Nuvem nas Autarquias Federais do Ministério da Educação},
  year    = {2026},
  note    = {Em preparação. Repositório: https://github.com/luizfpq/etp_nuvem_ifsp}
}
```
