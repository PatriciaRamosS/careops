O relatório deve conter uma análise inicial dos riscos OWASP Top 10 aplicados ao sistema fictício CareOps+. É uma análise prévia, antes de fazer os ataques reais das aulas seguintes.

Exemplo: 

# CareOps+ – Análise Inicial de Riscos (OWASP Top 10)

Este documento apresenta uma avaliação preliminar dos riscos de segurança do sistema CareOps+, relacionando cada categoria do OWASP Top 10 com possíveis impactos na
aplicação.

## A01 – Broken Access Control
- Risco: acesso indevido a dados de pacientes.
- Possíveis áreas afetadas: /patients, /patient/{id}, prontuários.
- Impacto: vazamento de dados sensíveis; violação de LGPD/HIPAA.
- Mitigação inicial: RBAC, ABAC e validação de ID no backend.

## A02 – Cryptographic Failures
(...)