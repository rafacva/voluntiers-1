# Instalando as dependências 
sudo apt update -y
sudo apt upgrade -y
sudo apt autoremove -y
sudo apt install build-essential -y
sudo apt install python3.9 python3.9-venv python3.9-dev -y
sudo apt install nginx -y
sudo apt install certbot python3-certbot-nginx -y
sudo apt install postgresql postgresql-contrib -y
sudo apt install libpq-dev -y
sudo apt install git

# Postgres
sudo -u postgres psql
CREATE ROLE usuario WITH LOGIN SUPERUSER CREATEDB CREATEROLE PASSWORD 'senha';
CREATE DATABASE basededados WITH OWNER usuario;
GRANT ALL PRIVILEGES ON DATABASE basededados TO usuario;
\q
sudo systemctl restart postgresql

# repo bare
mkdir -p ~/app_bare
cd ~/app_bare
git init --bare
cd ~

# repo
mkdir -p ~/app_repo
cd ~/app_repo
git init
git remote add origin ~/app_bare
git add . && git commit -m 'Initial'
cd ~

# adiciona remoto
git remote add app_bare voluntiers:~/app_bare
git push app_bare <branch>