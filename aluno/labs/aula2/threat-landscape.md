# Threat Landscape & Mapeamento de Controles (CareOps+)

Este documento resume ameaças atuais que afetam aplicações web e pipelines DevSecOps e mostra como elas se conectam ao contexto da aplicação **CareOps+**. Em seguida, cada ameaça é mapeada às práticas do **NIST SSDF** e do **OWASP SAMM**, deixando claro como Threat Intelligence vira decisão prática dentro do SDLC.

---

## Parte 1 – Identificação de Ameaças Relevantes

### 1. Envenenamento de Dependências (Supply Chain Attack)

- **Tipo:** Supply Chain Compromise / Open Source Vulnerability  
- **Descrição:**  
  Atacantes publicam pacotes maliciosos em repositórios públicos (npm, PyPI, etc.) com nomes muito parecidos com bibliotecas legítimas (typosquatting) ou comprometem mantenedores de projetos populares para inserir backdoors. Como as dependências são puxadas automaticamente pelo CI/CD, o código malicioso entra “pela porta da frente”. Em muitos casos, a equipe só descobre o problema depois de vazamento de dados ou comportamento estranho em produção.  
- **Exemplo CareOps+:**  
  O pipeline de build do portal de agendamento do CareOps+ baixa automaticamente uma biblioteca de formatação de datas adulterada. Durante o processamento de requisições, essa biblioteca coleta dados de pacientes e envia silenciosamente para um servidor externo controlado pelo atacante, sem alterar o funcionamento aparente do sistema.

---

### 2. Vazamento de Credenciais em Código (Hardcoded Secrets)

- **Tipo:** Credential Theft / CI/CD Compromise  
- **Descrição:**  
  É quando chaves de API, tokens de acesso à nuvem ou senhas de banco acabam indo parar dentro do repositório Git (em código, `.env`, scripts de teste, etc.). Bots de varredura monitoram repositórios públicos o tempo todo atrás desses segredos, e muitas vezes conseguem explorá-los em minutos. Mesmo em repositórios privados, um vazamento acidental (fork público, print, bug de permissão) pode expor credenciais críticas.  
- **Exemplo CareOps+:**  
  Uma chave de acesso AWS S3, com permissão de leitura e escrita, é deixada em um script de teste no repositório do CareOps+. Um atacante que encontra essa chave passa a listar e apagar backups de prontuários médicos, tentando forçar a organização a pagar resgate para restaurar os dados.

---

### 3. Ataques a APIs (Broken Object Level Authorization – BOLA)

- **Tipo:** Web Application Attack / Authorization Failure  
- **Descrição:**  
  Em BOLA, a API até autentica o usuário, mas não verifica direito se aquele recurso específico realmente pertence a ele. O atacante altera o identificador do objeto (por exemplo, de `/user/123` para `/user/124`) e consegue acessar ou modificar informações de outras pessoas. Esse tipo de falha é muito comum em APIs REST e GraphQL e está diretamente ligado a erros de lógica de autorização.  
- **Exemplo CareOps+:**  
  Um usuário logado no aplicativo móvel CareOps+ intercepta a requisição para `/api/pacientes/123/exames`, troca o ID para `/api/pacientes/124/exames` e, por falta de checagem robusta de permissão, consegue visualizar o histórico de exames de outro paciente.

---

### 4. Ransomware focado em Ambientes de CI/CD

- **Tipo:** Malware / Availability Attack  
- **Descrição:**  
  Grupos de ransomware modernos não miram apenas bancos de dados de produção, mas também servidores de build (Jenkins, GitLab CI, runners) e repositórios de código. Ao criptografar esses ambientes e apagar snapshots locais, eles paralisam o desenvolvimento, impedem deploys de correções e chantageiam a organização para liberar o código de volta. Muitas vezes, o ponto de entrada é um servidor desatualizado ou sem hardening.  
- **Exemplo CareOps+:**  
  Um servidor Jenkins desatualizado do CareOps+ é comprometido por uma vulnerabilidade conhecida. O atacante instala ransomware, criptografa todos os jobs, artefatos de build e parte dos repositórios espelhados, impedindo o time de entregar correções de segurança para hospitais parceiros até que uma restauração difícil (ou pagamento de resgate) seja feita.

---

### 5. Configuração Insegura de Nuvem (Cloud Misconfiguration)

- **Tipo:** Cloud Infrastructure Compromise  
- **Descrição:**  
  Serviços de nuvem mal configurados – buckets públicos, grupos de segurança com portas liberadas para “0.0.0.0/0”, credenciais com privilégios exagerados – abrem portas diretas para invasores. Muitas vezes não há uma vulnerabilidade de software, e sim “apenas” uma regra de firewall errada ou uma opção padrão perigosa que nunca foi revisada. Essa é hoje uma das principais causas de vazamentos em ambientes cloud.  
- **Exemplo CareOps+:**  
  O banco de dados de triagem do CareOps+ roda em um container Kubernetes cuja porta de administração foi exposta na internet sem restrição de IP. Um atacante faz varredura na nuvem, encontra a porta aberta e tenta senhas fracas, ganhando acesso à interface administrativa do banco e aos dados de triagem dos pacientes.

---

## Parte 2 – Mapeamento ao NIST SSDF

A seguir, cada ameaça é ligada a **uma prática do NIST SSDF** que ajuda a reduzir o risco ou o impacto.

### Ameaça 1: Envenenamento de Dependências

- **SSDF recomendado:** **PW.4 – Reutilizar software existente e bem protegido sempre que viável (Reuse Existing, Well-Secured Software When Feasible Instead of Duplicating Functionality)**  
- **Justificativa:**  
  PW.4 incentiva a adquirir e manter componentes de terceiros com segurança avaliada e política clara de uso, em vez de simplesmente “puxar qualquer pacote” do repositório público. No contexto do CareOps+, isso se traduz em critérios mínimos para escolher bibliotecas (reputação, manutenção ativa, histórico de CVEs) e no uso de SCA no pipeline para bloquear dependências maliciosas antes do build.

---

### Ameaça 2: Vazamento de Credenciais em Código

- **SSDF recomendado:** **PO.1 – Definir requisitos de segurança para o desenvolvimento de software (Define Security Requirements for Software Development)**  
- **Justificativa:**  
  PO.1 trata de definir, de forma organizacional, quais requisitos de segurança valem para todos os projetos. Um desses requisitos pode ser justamente “segredos nunca devem ser versionados no Git”, exigindo uso de secret managers, rotação de chaves e scanners de segredos no CI. Para o CareOps+, isso evita que chaves de S3, tokens de API e senhas de banco acabem em scripts e arquivos `.env` dentro do repositório.

---

### Ameaça 3: Ataques a APIs (BOLA)

- **SSDF recomendado:** **PW.7 – Revisar e/ou analisar código legível para identificar vulnerabilidades (Review and/or Analyze Human-Readable Code to Identify Vulnerabilities and Verify Compliance with Security Requirements)**  
- **Justificativa:**  
  BOLA é uma falha de lógica de autorização que muitas vezes só aparece quando alguém olha com carinho para o código. PW.7 recomenda revisões de código (manuais e com ferramentas) focadas em requisitos de segurança, como regras de autorização por recurso. No CareOps+, isso significa revisar endpoints da API pensando explicitamente: “este paciente realmente pode ver/alterar este objeto?”.

---

### Ameaça 4: Ransomware em Ambientes de CI/CD

- **SSDF recomendado:** **PO.5 – Implementar e manter ambientes seguros para desenvolvimento de software (Implement and Maintain Secure Environments for Software Development)**  
- **Justificativa:**  
  PO.5 foca na proteção dos ambientes de desenvolvimento, build, teste e distribuição. Para o CareOps+, isso inclui isolar servidores Jenkins, aplicar hardening e patching regular, usar autenticação forte, segmentar redes e garantir que existam cópias de segurança recuperáveis. Assim, mesmo que haja uma tentativa de ransomware, o impacto sobre o pipeline tende a ser menor e mais fácil de recuperar.

---

### Ameaça 5: Configuração Insegura de Nuvem

- **SSDF recomendado:** **PW.9 – Configurar o software com definições seguras por padrão (Configure Software to Have Secure Settings by Default)**  
- **Justificativa:**  
  PW.9 reforça a ideia de “secure by default”: serviços não devem nascer com portas administrativas expostas ou políticas de acesso muito permissivas. No CareOps+, isso se traduz em usar infraestrutura como código (IaC) com baselines seguros (por exemplo, banco só acessível via rede interna ou VPN, grupos de segurança restritos, encryption em repouso ativada) e revisões de configuração antes de liberar ambientes de nuvem.

---

## Parte 3 – Mapeamento ao OWASP SAMM

Agora, para cada ameaça, é selecionada uma prática adequada do **OWASP SAMM**.

### Ameaça 1: Envenenamento de Dependências

- **Prática SAMM:** **Implementation → Secure Build → Software Dependencies**  
- **Justificativa:**  
  A atividade de *Software Dependencies* trata de gerenciar dependências com segurança: inventariar bibliotecas usadas, acompanhar CVEs e automatizar bloqueios no pipeline. No CareOps+, isso significa que o build só deve prosseguir se as dependências do projeto forem conhecidas, monitoradas e livres de vulnerabilidades críticas ou pacotes suspeitos.

---

### Ameaça 2: Vazamento de Credenciais em Código

- **Prática SAMM:** **Implementation → Secure Deployment → Secret Management**  
- **Justificativa:**  
  O stream de *Secret Management* foca em proteger todo o ciclo de vida de segredos (criação, armazenamento, uso e rotação). Para a realidade do CareOps+, essa prática se traduz em tirar credenciais do código e de arquivos de configuração, armazená-las em cofres seguros, injetar segredos dinamicamente nos containers e auditar o acesso humano a eles.

---

### Ameaça 3: Ataques a APIs (BOLA)

- **Prática SAMM:** **Verification → Security Testing → Scalable Baseline Testing**  
- **Justificativa:**  
  Em *Security Testing* o objetivo é ter testes de segurança repetíveis e escaláveis (SAST, DAST, testes específicos de API) integrados ao SDLC. No caso de BOLA, isso pode incluir testes automatizados e manuais tentando trocar IDs de recursos, usar tokens de outros usuários ou forçar acessos não autorizados em endpoints sensíveis do CareOps+ antes do deploy em produção.

---

### Ameaça 4: Ransomware em Ambientes de CI/CD

- **Prática SAMM:** **Operations → Environment Management → Patching and Updating**  
- **Justificativa:**  
  O stream de *Patching and Updating* garante que componentes de infraestrutura (como Jenkins, Git servers, SO dos runners) estejam atualizados e com correções de segurança aplicadas. No CareOps+, isso reduz a superfície de ataque para ransomware explorando vulnerabilidades conhecidas em servidores de build e serviços auxiliares do pipeline.

---

### Ameaça 5: Configuração Insegura de Nuvem

- **Prática SAMM:** **Operations → Environment Management → Configuration Hardening**  
- **Justificativa:**  
  *Configuration Hardening* trata de definir e aplicar baselines de configuração segura para todos os componentes de tecnologia. Isso se encaixa diretamente em misconfiguração de nuvem: para o CareOps+, significa ter padrões claros para security groups, roles de acesso, configuração de bancos em Kubernetes e buckets de armazenamento, além de monitorar desvios em relação a esses padrões.

---

## Parte 4 – Conclusão

As práticas de **Threat Intelligence** mudam o pipeline DevSecOps de um modo “apagando incêndio” para um modo realmente preventivo. Quando a equipe acompanha relatórios de ameaças (Elastic, Trend/Forti, relatórios regionais de LATAM) e entende como os atacantes estão explorando supply chain, APIs e nuvem, ela passa a priorizar o backlog de segurança com base em risco real e não só em severidade técnica. Isso influencia a definição de requisitos (PO.1), o desenho de arquitetura e o que é obrigatório no CI/CD (por exemplo, SCA para dependências e scanners de segredos no código).  
Ao mesmo tempo, Threat Intelligence alimenta quais controles do SAMM fazem mais sentido investir agora – como Secure Build, Secret Management e Environment Management – e orienta quais tipos de testes automatizados e manuais precisam entrar no ciclo (por exemplo, cenários específicos de BOLA em APIs). No caso do CareOps+, cada aula e cada ajuste no pipeline ganha contexto: não é apenas “rodar uma ferramenta”, mas alinhar o SDLC com o que está acontecendo hoje no mundo de ataques reais, reduzindo a chance de falhas críticas chegarem até os pacientes e hospitais que dependem da aplicação.
