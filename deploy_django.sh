echo "############################################"
echo "#############  Nginx Setup  ################"
echo "############################################"
echo 

# Exit Virtual Environment if any
deactivate

# Update Debian/Ubuntu
sudo apt update -y

# Install nginx
sudo apt install -y nginx

# Enable Firewall
sudo ufw enable
sudo ufw app list

# Enable Nginx in Firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow 'Nginx HTTP'
sudo ufw allow 'Nginx HTTPS'

sudo ufw status
sudo systemctl status nginx

echo "###########  Nginx Setup Completed ###########"
echo
# Create and Enter into Virtual Environment
sudo apt install -y virtualenv
virtualenv venv
source venv/bin/activate
echo
echo ######################################
echo ##########  Gunicorn Setup  ##########
echo ######################################
echo 

# install gunicorn
sudo apt install -y python3-pip
pip3 install gunicorn
deactivate

# Create Gunicorn Service
read -p "Username > " username
read -p "Project name > " project_name
read -p "Gunicorn Port > " gunicorn_port

sudo systemctl stop gunicorn
sudo mkdir /var/log/gunicorn
sudo echo "[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=$username
Group=www-data
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/gunicorn --access-logfile - --workers 3 --bind 0.0.0.0:$gunicorn_port $project_name.wsgi:application

[Install]" > temp.txt
sudo mv temp.txt /etc/systemd/system/gunicorn.service

echo ###########  Gunicorn Service Created ###########
echo 
echo ###########  Enabling Gunicorn Service ###########
echo
sudo systemctl start gunicorn; sudo systemctl enable gunicorn
sudo systemctl status gunicorn
#sudo journalctl -u gunicorn
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
echo
echo "####################################################################"
echo "###########  Configure Nginix to Proxy Pass to Gunicorn  ###########"
echo "####################################################################"
echo
read -p "Server name or IP adddress > " server_name
sudo rm -f /etc/nginx/sites-enabled/$project_name
echo "server {
    listen 80;
    server_name $server_name;

    location / {
        proxy_pass http://localhost:$gunicorn_port;
    }
}" > /etc/nginx/sites-available/$project_name

echo "##########  Creating Symlink for Nginx Sites  ##########"
sudo ln -s /etc/nginx/sites-available/$project_name /etc/nginx/sites-enabled/$project_name
echo "##########  Testing Nginx  ##########"
sudo nginx -t
echo "##########  Restarting Nginx  ##########"
sudo systemctl restart nginx



