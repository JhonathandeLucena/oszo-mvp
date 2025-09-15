# OSZO Digital Health - Sistema de Saúde Digital

## Visão Geral

O OSZO Digital Health é uma plataforma completa de saúde digital que conecta pacientes e profissionais de saúde na Zona Oeste do Rio de Janeiro. O sistema oferece consultas presenciais e telemedicina em uma plataforma integrada.

## Funcionalidades Principais

- 🔐 **Autenticação segura** - Login para pacientes e administradores
- 📅 **Agendamento de consultas** - Sistema completo de agendamento em 5 etapas
- 👨‍⚕️ **Gestão de médicos** - Cadastro e gerenciamento de profissionais
- 📋 **Histórico médico** - Armazenamento e visualização de documentos médicos
- 🔔 **Notificações** - Sistema de alertas e lembretes
- 💬 **Teleconsulta** - Integração com Google Meet
- 🎯 **Central de suporte** - FAQ, tutoriais e acessibilidade

## Tecnologias Utilizadas

### Backend
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados
- **Flask-CORS** - Suporte a CORS

### Frontend
- **React** - Biblioteca JavaScript
- **Vite** - Build tool
- **Tailwind CSS** - Framework CSS
- **Shadcn/UI** - Componentes UI
- **Lucide React** - Ícones

## Estrutura do Projeto

```
oszo-digital-health/
├── src/
│   ├── models/          # Modelos ORM (User, Medico, Consulta, etc.)
│   ├── routes/          # Rotas da API Flask
│   └── components/      # Componentes React
├── scripts/             # Scripts auxiliares
├── static/              # Arquivos estáticos (build do React)
├── database/            # Banco de dados SQLite
├── main.py              # Aplicação Flask principal
├── package.json         # Dependências Node.js
└── requirements.txt     # Dependências Python
```

## Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- npm ou yarn

### 1. Clonar o repositório
```bash
git clone <repository-url>
cd oszo-digital-health
```

### 2. Configurar Backend (Flask)
```bash
# Instalar dependências Python
pip install flask flask-cors sqlalchemy

# Configurar banco de dados
python populate_db.py
```

### 3. Configurar Frontend (React)
```bash
# Instalar dependências Node.js
npm install

# Build do frontend
npm run build

# Copiar arquivos para pasta static
cp -r dist/* static/
```

### 4. Executar o sistema
```bash
python main.py
```

O sistema estará disponível em `http://localhost:5000`

## Credenciais de Teste

### Usuário Paciente
- **Email**: joao@email.com
- **Senha**: 2o02!aKPmS{N

### Usuário Administrador
- **Email**: admin@oszo.com.br
- **Senha**: admin123

## API Endpoints

### Autenticação
- `POST /api/login` - Login de usuário
- `POST /api/logout` - Logout de usuário

### Usuários
- `GET /api/users` - Listar usuários
- `POST /api/users` - Criar usuário
- `GET /api/users/{id}` - Obter usuário específico

### Médicos
- `GET /api/medicos` - Listar médicos
- `POST /api/medicos` - Criar médico
- `GET /api/medicos/{id}` - Obter médico específico

### Consultas
- `GET /api/consultas` - Listar consultas
- `POST /api/consultas` - Criar consulta
- `GET /api/consultas/{id}` - Obter consulta específica

### Scripts Auxiliares
- `POST /api/scripts/cadastrar_pessoa` - Cadastrar pessoa
- `POST /api/scripts/gerar_slots` - Gerar slots de horários
- `POST /api/scripts/bloquear_slot` - Bloquear slot
- `POST /api/scripts/adicionar_link_meet` - Adicionar link Google Meet

## Deployment

### Opção 1: Deployment Local
```bash
# Executar em modo produção
python main.py
```

### Opção 2: Deployment com Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install flask flask-cors sqlalchemy
RUN python populate_db.py

EXPOSE 5000
CMD ["python", "main.py"]
```

### Opção 3: Deployment em Cloud
O sistema está configurado para deployment em plataformas como:
- Heroku
- AWS
- Google Cloud Platform
- DigitalOcean

## Configurações de Produção

### Variáveis de Ambiente
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export DATABASE_URL=your-database-url
```

### Configurações de Segurança
- Alterar `SECRET_KEY` em produção
- Configurar HTTPS
- Implementar rate limiting
- Configurar backup do banco de dados

## Monitoramento e Logs

O sistema gera logs em `flask_server.log` para monitoramento de:
- Requisições HTTP
- Erros de aplicação
- Operações de banco de dados

## Suporte e Manutenção

### Backup do Banco de Dados
```bash
cp database/app.db database/backup_$(date +%Y%m%d).db
```

### Atualização do Sistema
```bash
# Atualizar dependências
pip install -r requirements.txt --upgrade
npm update

# Rebuild frontend
npm run build
cp -r dist/* static/
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contato

- **Email**: suporte@oszo.com.br
- **Telefone**: (11) 3000-0000
- **Website**: https://oszo.com.br

---

**OSZO Digital Health** - Sua saúde em primeiro lugar 💙

