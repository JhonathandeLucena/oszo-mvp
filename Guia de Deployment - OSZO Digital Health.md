# Guia de Deployment - OSZO Digital Health

## Visão Geral

Este guia fornece instruções detalhadas para fazer o deployment do sistema OSZO Digital Health em diferentes ambientes e plataformas.

## Pré-requisitos

- Sistema testado e funcionando localmente
- Banco de dados populado com dados de teste
- Build do frontend React concluído
- Todas as dependências instaladas

## Deployment Local (Desenvolvimento)

### 1. Preparação
```bash
# Verificar se o sistema está funcionando
python main.py

# Testar no navegador
curl http://localhost:5000/api/health
```

### 2. Configuração de Produção
```bash
# Definir variáveis de ambiente
export FLASK_ENV=production
export SECRET_KEY="sua-chave-secreta-aqui"
```

## Deployment em Heroku

### 1. Preparar arquivos necessários

**Procfile**
```
web: python main.py
```

**runtime.txt**
```
python-3.11.0
```

### 2. Comandos de deployment
```bash
# Instalar Heroku CLI
# Fazer login no Heroku
heroku login

# Criar aplicação
heroku create oszo-digital-health

# Configurar variáveis de ambiente
heroku config:set SECRET_KEY="sua-chave-secreta"
heroku config:set FLASK_ENV=production

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## Deployment em AWS (EC2)

### 1. Configurar instância EC2
```bash
# Conectar à instância
ssh -i sua-chave.pem ubuntu@seu-ip-ec2

# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python e Node.js
sudo apt install python3 python3-pip nodejs npm -y
```

### 2. Configurar aplicação
```bash
# Clonar repositório
git clone seu-repositorio
cd oszo-digital-health

# Instalar dependências
pip3 install -r requirements.txt
npm install && npm run build

# Copiar build para static
cp -r dist/* static/

# Configurar como serviço systemd
sudo nano /etc/systemd/system/oszo.service
```

**Arquivo oszo.service**
```ini
[Unit]
Description=OSZO Digital Health
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/oszo-digital-health
Environment=PATH=/home/ubuntu/.local/bin
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 3. Iniciar serviço
```bash
sudo systemctl daemon-reload
sudo systemctl enable oszo
sudo systemctl start oszo
```

## Deployment em Google Cloud Platform

### 1. Preparar app.yaml
```yaml
runtime: python311

env_variables:
  SECRET_KEY: "sua-chave-secreta"
  FLASK_ENV: "production"

handlers:
- url: /static
  static_dir: static

- url: /.*
  script: auto
```

### 2. Deploy
```bash
# Instalar Google Cloud SDK
# Autenticar
gcloud auth login

# Configurar projeto
gcloud config set project seu-projeto-id

# Deploy
gcloud app deploy
```

## Deployment em DigitalOcean

### 1. Criar Droplet
- Escolher Ubuntu 22.04
- Configurar SSH keys
- Selecionar tamanho adequado

### 2. Configurar servidor
```bash
# Conectar ao droplet
ssh root@seu-ip-droplet

# Instalar dependências
apt update && apt upgrade -y
apt install python3 python3-pip nodejs npm nginx -y

# Configurar aplicação
git clone seu-repositorio
cd oszo-digital-health
pip3 install -r requirements.txt
npm install && npm run build
cp -r dist/* static/
```

### 3. Configurar Nginx
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/oszo-digital-health/static;
    }
}
```

## Deployment com Docker

### 1. Criar Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar Node.js
RUN apt-get update && apt-get install -y nodejs npm

# Copiar arquivos
COPY . .

# Instalar dependências Python
RUN pip install -r requirements.txt

# Instalar dependências Node.js e fazer build
RUN npm install && npm run build && cp -r dist/* static/

# Expor porta
EXPOSE 5000

# Comando de inicialização
CMD ["python", "main.py"]
```

### 2. Build e execução
```bash
# Build da imagem
docker build -t oszo-digital-health .

# Executar container
docker run -p 5000:5000 oszo-digital-health
```

### 3. Docker Compose
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=sua-chave-secreta
      - FLASK_ENV=production
    volumes:
      - ./database:/app/database
```

## Configurações de Segurança

### 1. HTTPS
```bash
# Instalar Certbot (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx

# Obter certificado SSL
sudo certbot --nginx -d seu-dominio.com
```

### 2. Firewall
```bash
# Configurar UFW
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 3. Backup Automático
```bash
# Criar script de backup
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp /path/to/database/app.db /path/to/backups/backup_$DATE.db

# Adicionar ao crontab
0 2 * * * /path/to/backup-script.sh
```

## Monitoramento

### 1. Logs
```bash
# Visualizar logs do sistema
sudo journalctl -u oszo -f

# Logs da aplicação
tail -f flask_server.log
```

### 2. Métricas
- CPU e memória
- Tempo de resposta
- Número de usuários ativos
- Erros de aplicação

## Troubleshooting

### Problemas Comuns

1. **Erro 500 - Internal Server Error**
   - Verificar logs da aplicação
   - Confirmar variáveis de ambiente
   - Verificar permissões de arquivo

2. **Banco de dados não encontrado**
   - Executar `python populate_db.py`
   - Verificar caminho do banco

3. **Frontend não carrega**
   - Verificar se o build foi copiado para static/
   - Confirmar configuração do servidor web

### Comandos Úteis
```bash
# Verificar status do serviço
sudo systemctl status oszo

# Reiniciar aplicação
sudo systemctl restart oszo

# Verificar logs
sudo journalctl -u oszo --since "1 hour ago"

# Testar conectividade
curl -I http://localhost:5000/api/health
```

## Manutenção

### Atualizações
1. Fazer backup do banco de dados
2. Testar em ambiente de desenvolvimento
3. Fazer deploy da nova versão
4. Verificar funcionamento
5. Rollback se necessário

### Backup e Restore
```bash
# Backup
cp database/app.db backups/app_$(date +%Y%m%d).db

# Restore
cp backups/app_20241215.db database/app.db
sudo systemctl restart oszo
```

---

**Nota**: Sempre teste o deployment em um ambiente de staging antes de fazer deploy em produção.

