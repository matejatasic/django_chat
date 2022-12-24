sudo apt update

sudo apt -y install python3-pip

# install postgresql
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt -y install postgresql libpq-dev

# setup database
sudo systemctl start postgresql.service
sudo su postgres -c "psql -c \"CREATE ROLE vagrant SUPERUSER LOGIN PASSWORD 'vagrant'\" "
sudo su postgres -c "createdb django_chat_db"

# pip installs
pip3 install django
pip3 install -r /vagrant/django_chat/requirements.txt
