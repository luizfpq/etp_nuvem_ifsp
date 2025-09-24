# Os domínios de dados do Portal Nacional de Contratações Públicas (PNCP) podem ser consultados em:  
[https://pncp.gov.br/app/entidades-dominio](https://pncp.gov.br/app/entidades-dominio)


------
## Modalidade da Contratação
    referência: codigoOrgao


| Código | Nome                          | Descrição                                                                                                                                                                                                 | Ativo |
|--------|-------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
| 1      | Leilão - Eletrônico           |                                                                                                                                                                                                           | Sim   |
| 2      | Diálogo Competitivo           |                                                                                                                                                                                                           | Sim   |
| 3      | Concurso                      |                                                                                                                                                                                                           | Sim   |
| 4      | Concorrência - Eletrônica     |                                                                                                                                                                                                           | Sim   |
| 5      | Concorrência - Presencial     |                                                                                                                                                                                                           | Sim   |
| 6      | Pregão - Eletrônico           |                                                                                                                                                                                                           | Sim   |
| 7      | Pregão - Presencial           |                                                                                                                                                                                                           | Sim   |
| 8      | Dispensa                      |                                                                                                                                                                                                           | Sim   |
| 9      | Inexigibilidade               |                                                                                                                                                                                                           | Sim   |
| 10     | Manifestação de Interesse     |                                                                                                                                                                                                           | Sim   |
| 11     | Pré-qualificação              |                                                                                                                                                                                                           | Sim   |
| 12     | Credenciamento                |                                                                                                                                                                                                           | Sim   |
| 13     | Leilão - Presencial           | Modalidade de licitação realizada sob a forma presencial para alienação de bens imóveis ou de bens móveis inservíveis ou legalmente apreendidos a quem oferecer o maior lance                                 | Sim   |
| 14     | Inaplicabilidade da Licitação | Situação em que, por especificidades da legislação ou natureza da atividade, não se exige o processo licitatório. Refere-se aos casos em que a lei determina que a licitação não é aplicável, seja pela natureza única do objeto ou pela impossibilidade de competição. | Sim   |



## Queries

    MariaDB 1

    select 
        orgaoEntidadeRazaoSocial, unidadeOrgaoCodigoUnidade, unidadeOrgaoNomeUnidade, modalidadeNome, sum(valorTotalEstimado), sum(valorTotalHomologado)
    from 
        vw_compras_left_uasg where objetoCompra like "%nuvem%" or      informacaoComplementar like "%nuvem"
    group by 
        orgaoEntidadeRazaoSocial asc;


    MariaDB 2

    SELECT
    orgaoEntidadeRazaoSocial,
    unidadeOrgaoCodigoUnidade,
    unidadeOrgaoNomeUnidade,
    modalidadeNome,
    SUM(valorTotalEstimado) AS somaValorTotalEstimado,
    SUM(valorTotalHomologado) AS somaValorTotalHomologado
FROM
    vw_compras_left_uasg
WHERE
    objetoCompra LIKE "%nuvem%"
    OR informacaoComplementar LIKE "%nuvem%"
GROUP BY
    orgaoEntidadeRazaoSocial,
    unidadeOrgaoCodigoUnidade,
    unidadeOrgaoNomeUnidade,
    modalidadeNome
ORDER BY
    orgaoEntidadeRazaoSocial ASC,
    modalidadeNome ASC;
