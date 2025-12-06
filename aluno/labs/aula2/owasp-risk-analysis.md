# CareOps+ – Análise Inicial de Riscos (OWASP Top 10)

Este documento apresenta uma avaliação preliminar dos riscos de segurança do sistema CareOps+, relacionando cada categoria do OWASP Top 10 (2021) com possíveis impactos na aplicação, além de sugerir técnicas de teste baseadas no NIST SP 800-115.

---

## Análise de Riscos (A01-A10)

### A01:2021 – Broken Access Control
* **Vulnerabilidade Típica:** Insecure Direct Object References (IDOR).
* **Impacto Técnico:** Permite manipulação de parâmetros (ex: IDs na URL) para acessar recursos sem autorização.
* **Impacto de Negócio:** Violação crítica de privacidade (LGPD/HIPAA), permitindo que pacientes visualizem prontuários de terceiros.
* **Exemplo CareOps+:** Alterar `GET /api/prontuario/1001` para `1002` e visualizar exames de outro paciente.

### A02:2021 – Cryptographic Failures
* **Vulnerabilidade Típica:** Armazenamento de senhas ou dados de saúde (PHI) em texto plano ou com algoritmos obsoletos (MD5).
* **Impacto Técnico:** Exposição imediata de dados sensíveis em caso de vazamento de banco (SQL Dump).
* **Impacto de Negócio:** Perda massiva de reputação e multas severas por vazamento de dados médicos sensíveis.
* **Exemplo CareOps+:** Banco de dados armazenando CPFs e diagnósticos sem criptografia em repouso (*Encryption at Rest*).

### A03:2021 – Injection
* **Vulnerabilidade Típica:** SQL Injection (SQLi) em campos de busca ou login.
* **Impacto Técnico:** Execução não autorizada de comandos no BD, possibilitando exfiltração ou destruição de tabelas.
* **Impacto de Negócio:** Risco à vida dos pacientes por possível alteração maliciosa de dosagens ou históricos clínicos.
* **Exemplo CareOps+:** Input de busca de médicos aceitando `' OR '1'='1`, retornando todos os usuários do sistema.

### A04:2021 – Insecure Design
* **Vulnerabilidade Típica:** Falta de *Rate Limiting* (limitação de taxa) em APIs críticas.
* **Impacto Técnico:** Suscetibilidade a ataques de negação de serviço (DoS) e força bruta automatizada.
* **Impacto de Negócio:** Indisponibilidade da plataforma de agendamento em horários de pico ou crises sanitárias.
* **Exemplo CareOps+:** Bot agendando 500 consultas por minuto, bloqueando a agenda real de médicos.

### A05:2021 – Security Misconfiguration
* **Vulnerabilidade Típica:** Mensagens de erro verbosas (Stack Traces) ou configurações padrão (default) ativas.
* **Impacto Técnico:** Vazamento de detalhes da infraestrutura que facilitam a exploração por atacantes.
* **Impacto de Negócio:** Facilitação de invasões que poderiam ser evitadas com *hardening* básico.
* **Exemplo CareOps+:** Servidor de produção exibindo erros detalhados do .NET/Java com caminhos de pastas internos.

### A06:2021 – Vulnerable and Outdated Components
* **Vulnerabilidade Típica:** Uso de bibliotecas de terceiros com CVEs (vulnerabilidades) conhecidas e não corrigidas.
* **Impacto Técnico:** Possibilidade de Execução Remota de Código (RCE) via exploração de componentes legados.
* **Impacto de Negócio:** Porta de entrada para Ransomware, sequestrando dados hospitalares.
* **Exemplo CareOps+:** Uso de versão desatualizada do *Log4j* ou *jQuery* no portal do paciente.

### A07:2021 – Identification and Authentication Failures
* **Vulnerabilidade Típica:** Permissão de senhas fracas e ausência de Múltiplo Fator de Autenticação (MFA).
* **Impacto Técnico:** Facilitação de ataques de *Credential Stuffing* e sequestro de sessões.
* **Impacto de Negócio:** Acesso indevido a contas de médicos, permitindo prescrições fraudulentas em nome de terceiros.
* **Exemplo CareOps+:** Sistema permitindo cadastro de senha "123456" para contas administrativas.

### A08:2021 – Software and Data Integrity Failures
* **Vulnerabilidade Típica:** Desserialização insegura ou falha na verificação de integridade de atualizações (CI/CD).
* **Impacto Técnico:** Injeção de código malicioso diretamente no fluxo de execução da aplicação.
* **Impacto de Negócio:** Comprometimento da cadeia de suprimentos de software (*Supply Chain Attack*).
* **Exemplo CareOps+:** Pipeline CI/CD baixando dependências npm/pip sem verificar assinatura ou hash.

### A09:2021 – Security Logging and Monitoring Failures
* **Vulnerabilidade Típica:** Falta de logs para eventos críticos (login falho, acesso a dados sensíveis).
* **Impacto Técnico:** Cegueira operacional; impossibilidade de detectar ataques em tempo real ou fazer forense.
* **Impacto de Negócio:** Incapacidade de notificar a ANPD/pacientes sobre a extensão real de um vazamento.
* **Exemplo CareOps+:** Ausência de registros de auditoria quando um usuário exporta grandes volumes de dados de pacientes.

### A10:2021 – Server-Side Request Forgery (SSRF)
* **Vulnerabilidade Típica:** Servidor buscando recursos externos baseados em URLs fornecidas pelo usuário sem validação.
* **Impacto Técnico:** Acesso a serviços internos não expostos, metadados de nuvem ou varredura de rede interna.
* **Impacto de Negócio:** Exposição de infraestrutura interna hospitalar segregada (ex: dispositivos IoT médicos).
* **Exemplo CareOps+:** Funcionalidade de "Upload por URL" usada para acessar `http://localhost/admin` ou metadados AWS.

---

## Técnicas de Teste Recomendadas (NIST SP 800-115)

Baseado nas seções 2 e 3 do NIST SP 800-115, as seguintes técnicas são essenciais para o ciclo de vida do CareOps+:

### 1. Review de Código Fonte (Source Code Review)
Análise manual ou automatizada (SAST) do código para encontrar falhas antes da compilação.
* **Relevância no SDLC:** Permite a implementação do *Shift Left*, corrigindo vulnerabilidades na fase de desenvolvimento (Pull Request), onde o custo de correção é menor.

### 2. Escaneamento de Vulnerabilidades (Vulnerability Scanning)
Uso de ferramentas para identificar hosts, portas abertas e CVEs em sistemas e dependências.
* **Relevância no SDLC:** Garante monitoramento contínuo da infraestrutura e bibliotecas, ideal para pipelines automatizados (DevSecOps) identificarem componentes desatualizados rapidamente.

### 3. Teste de Intrusão (Penetration Testing)
Simulação de ataques reais para validar a eficácia dos controles de segurança existentes.
* **Relevância no SDLC:** Atua como um "Quality Gate" final antes de grandes lançamentos, identificando falhas de lógica de negócio complexas que scanners automáticos não detectam.