# Relatório de Análise: OSZO Digital Health

## 1. Introdução

Este relatório apresenta uma análise detalhada do projeto OSZO Digital Health, com base nos arquivos fornecidos em um pacote ZIP. O objetivo é compreender a estrutura da aplicação, as tecnologias utilizadas, as funcionalidades implementadas e as atualizações recentes.




## 2. Visão Geral do Projeto

A OSZO Digital Health é uma plataforma completa de saúde digital que oferece uma experiência integrada para pacientes gerenciarem sua saúde, com funcionalidades de teleconsultas, agendamentos online e acesso ao histórico médico. O projeto foi desenvolvido como um MVP (Minimum Viable Product) para demonstração das funcionalidades da plataforma.

### Acesso à Aplicação

**URL de Produção:** `https://9yhyi3cpj11o.manus.space`

**Credenciais de Teste:**
- **Email:** `joao@email.com`
- **Senha:** `2o02!aKPmS{N` (atualizada)

## 3. Arquitetura e Tecnologias

A aplicação segue uma arquitetura cliente-servidor, com um frontend desenvolvido em React e um backend em Flask.

### Frontend (React)

- **Framework:** React 18 com TypeScript
- **Build Tool:** Vite
- **Estilização:** Tailwind CSS
- **Componentes:** Shadcn/ui
- **Roteamento:** React Router DOM
- **Ícones:** Lucide React

### Backend (Flask)

- **Framework:** Flask (Python)
- **ORM:** SQLAlchemy
- **Banco de Dados:** SQLite (para desenvolvimento e demonstração)
- **CORS:** Flask-CORS

## 4. Modelagem de Dados

As principais entidades do banco de dados incluem:

- **User (Usuário/Paciente):** id, name, email, cpf, avatar, password, user_type, created_at.
- **Medico:** id, name, specialty, rating, price, image, crm, created_at.
- **Consulta:** id, type, specialty, medico_id, paciente_id, data, hora, status, observacoes, created_at, updated_at.
- **DocumentoMedico:** id, title, type, paciente_id, medico_nome, consulta_id, file_path, file_url, descricao, data_documento, created_at.
- **Notificacao:** id, usuario_id, type, title, message, read, data_agendamento, created_at.

## 5. APIs Implementadas

A aplicação expõe uma API RESTful com os seguintes endpoints principais:

- `GET, POST /api/users`
- `GET, POST /api/medicos`
- `GET, POST, PUT, DELETE /api/consultas`
- `GET, POST /api/documentos`
- `GET, PUT /api/notificacoes`
- `GET /api/health` (health check)

## 6. Funcionalidades Implementadas

As funcionalidades principais da plataforma incluem:

- **Landing Page:** Apresentação da plataforma e serviços.
- **Sistema de Autenticação:** Login com email/CPF e senha, interface responsiva, validação de formulários.
- **Dashboard Principal (Home):** Visão geral, acesso rápido a funcionalidades, próximas consultas.
- **Agendamento de Consultas:** Fluxo completo em 5 etapas (tipo, especialidade, médico, data, horário).
- **Confirmação de Consulta:** Resumo do agendamento, informações do médico e paciente.
- **Interface de Teleconsulta:** Simulação de videochamada, chat, controles de áudio/vídeo, timer.
- **Histórico Médico:** Visualização de documentos por categoria, filtros, busca, download.
- **Sistema de Notificações:** Notificações categorizadas, marcação de lidas/não lidas.
- **Central de Suporte:** FAQ interativo, chat de suporte, formulário de solicitação.

## 7. Atualizações Recentes (Baseado em `OSZO Digital Health - Resumo das Atualizações.md`)

As atualizações mais recentes focaram em redesenhar a página de login e a landing page para corresponder a um novo design.

### Landing Page (Index.jsx)
- **Título:** Atualizado para "Saúde Digital Acessível"
- **Texto:** Focado em conectar usuários a profissionais da Zona Oeste do Rio de Janeiro.

### Página de Login (Login.jsx)
- **Layout Redesenhado:** Lado esquerdo com informações e ilustração, lado direito com formulário.
- **Lado Esquerdo (azul):** Título "Saúde Digital Acessível", texto explicativo, ícones de benefícios (Seguro, Cuidado, Família), ilustração de telemedicina.
- **Formulário Atualizado:** Abas para Paciente, Administrador, Criar Conta. Campos para Email ou CPF, Senha. Opção de login por SMS.
- **Credenciais de Teste:** Senha atualizada para `2o02!aKPmS{N`.

### Alterações Técnicas
- Atualização de `Index.jsx` e `Login.jsx`.
- Implementação de layout responsivo com Tailwind CSS.
- Atualização da senha de teste em `populate_db.py`.

## 8. Considerações Finais

O projeto OSZO Digital Health demonstra uma aplicação web robusta com um conjunto abrangente de funcionalidades para gestão de saúde digital. A arquitetura modular e o uso de tecnologias modernas (React, Flask, Tailwind CSS) indicam um desenvolvimento focado em escalabilidade e manutenibilidade. As recentes atualizações mostram um esforço contínuo para melhorar a experiência do usuário e a conformidade com o design.





# Análise Detalhada do Modelo de Dados e Propostas de Implementação

## 1. Modelo de Dados do Excel/CSV (Base Oficial do MVP)

Com base no `OSZO_Prompt_Final.txt` e na análise do `OSZO_MVP_Final.xlsx`, as seguintes entidades e campos são definidos como a "base oficial do MVP":

### 1.1. Cadastro_Unificado
- **Campos:** ID, Nome, Email, CPF, Telefone, Idade, Especialidade, CRM, Unidade, Disponibilidade, FamilyID, Tipo, Função/Admin
- **Observações:** Esta tabela unifica pacientes, profissionais e colaboradores. `Especialidade`, `CRM`, `Unidade`, `Disponibilidade` são específicos para profissionais. `FamilyID` e `Tipo` (Paciente/Profissional/Colaborador) são para todos. `Função/Admin` indica o papel administrativo.

### 1.2. Agenda_Profissional
- **Campos:** ProfissionalID, DiaSemana, Inicio, Fim, TipoAtendimento
- **Observações:** Define as janelas fixas de atendimento dos profissionais.

### 1.3. Slots_Gerados
- **Campos:** SlotID, ProfissionalID, Data, HoraInicio, HoraFim, TipoAtendimento, Status, PacienteID, ConsultaID
- **Observações:** Representa blocos de 30 minutos gerados automaticamente a partir da `Agenda_Profissional`. `Status` indica se está disponível ou agendado. `PacienteID` e `ConsultaID` são preenchidos quando o slot é agendado.

### 1.4. Consultas_Ajustada
- **Campos:** ConsultaID, PacienteID, ProfissionalID, SlotID, TipoAtendimento, Status, LinkMeet, Unidade, Observacoes
- **Observações:** Vincula paciente, profissional e slot. `LinkMeet` para consultas online e `Unidade` para presenciais.

### 1.5. Historico_Medico
- **Campos:** ID, ConsultaID, PacienteID, ProfissionalID, Data, Tipo, Evolução/Resumo, Prescrição
- **Observações:** Registros escritos de evolução clínica.

### 1.6. Laudos
- **Campos:** ID, ConsultaID, PacienteID, ProfissionalID, TipoExame, Data, LaudoTexto, Arquivo (PDF/Imagem)
- **Observações:** Laudos com texto e referência a um arquivo (PDF/Imagem).

## 2. Modelo de Dados ORM (SQLAlchemy) Existente

Com base nos arquivos Python (`user.py`, `medico.py`, `consulta.py`, `documento_medico.py`, `notificacao.py`) do projeto, as seguintes entidades são definidas:

### 2.1. User
- **Campos:** id, name, email, cpf, avatar, password, user_type (paciente ou administrador), created_at
- **Observações:** Corresponde parcialmente ao `Cadastro_Unificado` para pacientes e administradores. Não inclui `Telefone`, `Idade`, `FamilyID`, `Especialidade`, `CRM`, `Unidade`, `Disponibilidade` do `Cadastro_Unificado`.

### 2.2. Medico
- **Campos:** id, name, specialty, rating, price, image, crm, created_at
- **Observações:** Corresponde aos profissionais no `Cadastro_Unificado`. Não inclui `Telefone`, `Idade`, `Unidade`, `Disponibilidade`.

### 2.3. HorarioDisponivel (associado a Medico)
- **Campos:** id, medico_id, data, hora_inicio, hora_fim, disponivel
- **Observações:** Esta tabela não foi explicitamente mencionada no prompt do Excel/CSV, mas é crucial para a gestão de slots. É o equivalente funcional de `Slots_Gerados` e `Agenda_Profissional` combinados, mas com uma estrutura mais simplificada.

### 2.4. Consulta
- **Campos:** id, type, specialty, medico_id, paciente_id, data, hora, status, observacoes, created_at, updated_at
- **Observações:** Corresponde a `Consultas_Ajustada`. Faltam os campos `SlotID`, `LinkMeet` e `Unidade` que estão no Excel/CSV.

### 2.5. DocumentoMedico
- **Campos:** id, title, type, paciente_id, medico_nome, consulta_id, file_path, file_url, descricao, data_documento, created_at
- **Observações:** Corresponde a `Laudos` e `Historico_Medico`. O campo `type` (exame, receita, relatório) abrange os tipos de documentos. O campo `file_path` e `file_url` são para o arquivo. `descricao` é o `LaudoTexto` ou `Evolução/Resumo`.

### 2.6. Notificacao
- **Campos:** id, usuario_id, type, title, message, read, data_agendamento, created_at
- **Observações:** Não há uma tabela correspondente no modelo Excel/CSV, mas é uma funcionalidade implementada no sistema.

## 3. Inconsistências e Discrepâncias Identificadas

### 3.1. Unificação de Entidades
- **`Cadastro_Unificado` (Excel/CSV) vs. `User` e `Medico` (ORM):** O modelo ORM separa `User` (pacientes/administradores) e `Medico`. O `Cadastro_Unificado` do Excel/CSV tenta consolidar todos, o que pode levar a campos nulos para diferentes tipos de usuários (ex: `Especialidade` e `CRM` para pacientes). A separação no ORM é mais granular e tipicamente melhor para um banco de dados relacional.

### 3.2. Campos Faltantes no ORM (em relação ao Excel/CSV)
- **`User` (ORM):** Faltam `Telefone`, `Idade`, `FamilyID` do `Cadastro_Unificado`.
- **`Medico` (ORM):** Faltam `Telefone`, `Idade`, `Unidade`, `Disponibilidade` do `Cadastro_Unificado`.
- **`Consulta` (ORM):** Faltam `SlotID`, `LinkMeet` e `Unidade` do `Consultas_Ajustada`. O `LinkMeet` e `Unidade` são cruciais para diferenciar consultas online/presenciais conforme as regras do prompt.

### 3.3. Entidades Faltantes no Excel/CSV (em relação ao ORM)
- **`HorarioDisponivel` (ORM):** Não há uma tabela direta no Excel/CSV, mas a lógica de `Agenda_Profissional` e `Slots_Gerados` se traduz nesta entidade no ORM. A `HorarioDisponivel` é uma representação mais dinâmica dos slots.
- **`Notificacao` (ORM):** Não há uma tabela correspondente no modelo Excel/CSV, indicando que esta é uma funcionalidade adicional implementada no sistema.

### 3.4. Ambiguidade e Detalhes
- **`TipoAtendimento` em `Agenda_Profissional` e `Slots_Gerados` (Excel/CSV):** O ORM `HorarioDisponivel` não tem um campo `TipoAtendimento` explícito, o que pode dificultar a geração de slots específicos para online/presencial se essa informação não for inferida ou adicionada.
- **`DocumentoMedico` (ORM) vs. `Historico_Medico` e `Laudos` (Excel/CSV):** O ORM `DocumentoMedico` unifica `Historico_Medico` e `Laudos`. O campo `type` (exame, receita, relatório) e `descricao` (para texto) e `file_path`/`file_url` (para arquivos) permitem essa unificação, o que é uma boa prática de normalização.

## 4. Recomendações para Consistência

Para garantir a consistência entre o modelo de dados do Excel/CSV (base oficial) e o ORM (SQLAlchemy), as seguintes ações são recomendadas:

1.  **Atualizar Modelos ORM `User` e `Medico`:** Adicionar os campos `Telefone`, `Idade`, `FamilyID` (para `User`) e `Unidade`, `Disponibilidade` (para `Medico`) que estão presentes no `Cadastro_Unificado` do Excel/CSV.
2.  **Atualizar Modelo ORM `Consulta`:** Adicionar os campos `SlotID`, `LinkMeet` e `Unidade`. O `LinkMeet` e `Unidade` são essenciais para as regras de negócio de consultas online/presenciais.
3.  **Refinar `HorarioDisponivel`:** Considerar adicionar um campo `tipo_atendimento` (online/presencial) para alinhar com `Agenda_Profissional` e `Slots_Gerados` do Excel/CSV, ou garantir que essa lógica seja tratada na geração dos slots.
4.  **Mapeamento de `Função/Admin`:** O campo `Função/Admin` do `Cadastro_Unificado` precisa ser mapeado para `user_type` em `User` e, para profissionais, talvez um campo `role` em `Medico` ou uma tabela de junção para papéis.

## 5. Propostas de Scripts para Funcionalidades Solicitadas

Com base nas inconsistências identificadas e nas funcionalidades solicitadas no prompt, as seguintes propostas de scripts são apresentadas para garantir a aderência à "base oficial do MVP" (Excel/CSV) e a funcionalidade do sistema.

### 5.1. Script para Cadastro Unificado de Pessoas (`cadastro_pessoas.py`)

**Objetivo:** Criar um script que permita o cadastro de pacientes, profissionais e colaboradores de forma unificada, refletindo a estrutura do `Cadastro_Unificado` do Excel/CSV, mas persistindo os dados nas tabelas `User` e `Medico` do ORM, conforme o `user_type`.

**Abordagem:**
1.  **Entrada de Dados:** O script receberá dados de uma pessoa (Nome, Email, CPF, Telefone, Idade, Tipo (Paciente/Profissional/Colaborador), Função/Admin, Especialidade, CRM, Unidade, Disponibilidade, FamilyID).
2.  **Lógica de Persistência:**
    *   Se `Tipo` for 'Paciente' ou 'Colaborador' (com `Função/Admin` = 'admin'), os dados serão inseridos na tabela `User`.
    *   Se `Tipo` for 'Profissional', os dados serão inseridos na tabela `Medico`. Campos como `Telefone`, `Idade`, `Unidade`, `Disponibilidade` deverão ser adicionados ao modelo `Medico` se ainda não existirem.
    *   A `password` será gerada ou solicitada, e o `user_type` em `User` será definido como 'paciente' ou 'administrador' com base em `Função/Admin`.
3.  **Validação:** Garantir que campos obrigatórios sejam preenchidos e que `CPF`/`Email` sejam únicos.

**Impacto no ORM:** Requer a adição de campos como `telefone`, `idade` ao modelo `User` e `telefone`, `unidade`, `disponibilidade` ao modelo `Medico` para manter a paridade com o `Cadastro_Unificado`.

### 5.2. Script para Geração Automática de Slots (`gerar_slots.py`)

**Objetivo:** Gerar automaticamente blocos de 30 minutos (`Slots_Gerados`) para cada profissional, com base em sua `Agenda_Profissional` (Excel/CSV), e persistir esses slots na tabela `HorarioDisponivel` do ORM.

**Abordagem:**
1.  **Leitura da Agenda:** O script lerá a `Agenda_Profissional` (ou um modelo ORM equivalente) para cada profissional, obtendo `DiaSemana`, `Inicio`, `Fim` e `TipoAtendimento`.
2.  **Geração de Slots:** Para cada entrada na agenda, o script iterará em intervalos de 30 minutos entre `Inicio` e `Fim`.
3.  **Persistência:** Cada slot gerado será inserido na tabela `HorarioDisponivel`, com `medico_id`, `data`, `hora_inicio`, `hora_fim` e `disponivel=True`. Um campo `tipo_atendimento` pode ser adicionado a `HorarioDisponivel` para refletir o `TipoAtendimento` da agenda.
4.  **Considerações:** O script precisará de uma data de início e fim para a geração dos slots (ex: gerar slots para as próximas 4 semanas).

**Impacto no ORM:** Requer a adição de um campo `tipo_atendimento` ao modelo `HorarioDisponivel` para alinhar com a granularidade do Excel/CSV.

### 5.3. Script para Bloqueio de Slots Ocupados (`bloquear_slots.py`)

**Objetivo:** Atualizar o `Status` de um slot para 'Agendado' (ou `disponivel=False` no ORM) quando uma consulta é agendada, e preencher `PacienteID` e `ConsultaID` no slot correspondente.

**Abordagem:**
1.  **Integração com Agendamento:** Este script será uma função ou parte do processo de criação de uma `Consulta`.
2.  **Atualização do Slot:** Após a criação bem-sucedida de uma `Consulta`, o script identificará o `SlotID` correspondente na tabela `Slots_Gerados` (ou `HorarioDisponivel` no ORM) e atualizará seu `Status` para 'Agendado' (`disponivel=False`), preenchendo `PacienteID` e `ConsultaID`.
3.  **Reversão:** Em caso de cancelamento de consulta, o script deverá reverter o `Status` do slot para 'Disponível' (`disponivel=True`).

**Impacto no ORM:** O modelo `Consulta` já tem `medico_id` e `paciente_id`. O `HorarioDisponivel` já tem `disponivel`. Seria necessário adicionar `paciente_id` e `consulta_id` ao `HorarioDisponivel` para espelhar `Slots_Gerados`.

### 5.4. Script para Inclusão de Link Meet em Consultas Online (`adicionar_link_meet.py`)

**Objetivo:** Permitir que médicos ou colaboradores adicionem o `LinkMeet` a consultas online na tabela `Consultas_Ajustada` (ou `Consulta` no ORM).

**Abordagem:**
1.  **Interface:** Pode ser uma função de API (`PUT /api/consultas/<id>/add_link_meet`) ou uma interface administrativa no frontend.
2.  **Atualização:** O script receberá o `ConsultaID` e o `LinkMeet` e atualizará o campo `LinkMeet` na tabela `Consulta`.
3.  **Validação:** Garantir que a consulta seja do `TipoAtendimento` 'online' antes de adicionar o link.

**Impacto no ORM:** Requer a adição do campo `link_meet` ao modelo `Consulta` para alinhar com o `Consultas_Ajustada` do Excel/CSV.

Essas propostas visam fechar as lacunas entre os modelos de dados e implementar as funcionalidades essenciais, mantendo a flexibilidade para futuras evoluções.

