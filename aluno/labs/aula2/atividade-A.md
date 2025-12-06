# Atividade Assíncrona A - Reflexões Técnicas

## Respostas às Questões de Reflexão

### 1. Qual categoria do OWASP Top 10 você considera mais crítica para aplicações de saúde? Justifique.
**A01:2021 – Broken Access Control**.
Embora a injeção de código seja grave, no contexto de saúde (*Healthcare*), a privacidade é o ativo mais valioso. Falhas de controle de acesso (como IDOR) que permitem a visualização horizontal de dados (um paciente acessando dados de outro) violam diretamente a LGPD e a confiança no sistema. Diferente de uma queda de sistema (Disponibilidade), a quebra de Confidencialidade de dados médicos é irreversível e gera os maiores danos legais e reputacionais para a instituição.

### 2. Qual técnica do NIST 800-115 faz mais sentido para detectar falhas precocemente (Shift Left)?
**Review de Código Fonte (Source Code Security Analysis)**.
Esta técnica é a essência do *Shift Left*. Ao utilizar ferramentas de SAST (*Static Application Security Testing*) ou revisões por pares focadas em segurança durante o *commit* ou *Pull Request*, impedimos que o código vulnerável chegue aos ambientes de teste ou produção. É a abordagem mais proativa e econômica, pois resolve a "causa raiz" (o código mal escrito) antes que ela se torne um risco implantado.

### 3. Qual elemento do CareOps+ você acredita que merece atenção imediata em termos de risco?
**A API de Integração e seus mecanismos de Autenticação/Autorização**.
Como o CareOps+ centraliza dados de pacientes, médicos e possivelmente dispositivos IoT, sua API é o vetor de ataque mais atrativo. Se a API não implementar validação rigorosa de tokens (ex: JWT) e verificação de escopo em cada endpoint, ela se torna um "ponto único de falha". A atenção imediata deve ser em garantir que **todo** pedido à API seja autenticado e, crucialmente, autorizado para o recurso específico solicitado.