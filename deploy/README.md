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

# adiciona no dev local o bare remoto para o bare da vm
git remote add app_bare voluntiers:~/app_bare ou git remote add app_bare <username@ipdavm>:~/app_bare 
git push app_bare <branch>

# pulla o bare para o repo na vm
cd ~/app_repo
git pull origin <branch>

# criando o venv
python3.9 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
pip install psycopg2
pip install gunicorn

 