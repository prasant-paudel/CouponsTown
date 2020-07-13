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

# Enable Nginx and some other ports in Firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow 'Nginx HTTP'
sudo ufw allow 'Nginx HTTPS'
sudo ufw allow 'OpenSSH'
sudo ufw allow 8000/tcp

sudo ufw status

echo "###########  Nginx Setup Completed ###########"
echo
# Create and Enter into Virtual Environment
sudo apt install -y python virtualenv
virtualenv venv
sleep 1
source venv/bin/activate
echo
echo "######################################"
echo "##########  Gunicorn Setup  ##########"
echo "######################################"
echo 

# install gunicorn
sudo apt install -y python3-pip
pip3 install gunicorn
#ls -s /usr/local/bin/gunicorn venv/bin/gunicorn
pip3 install -r requirements.txt
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
Group=root
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/gunicorn --access-logfile - --workers 3 --bind 0.0.0.0:$gunicorn_port $project_name.wsgi:application

[Install]" > temp.txt
sudo mv temp.txt /etc/systemd/system/gunicorn.service

echo "###########  Gunicorn Service Created ###########"
echo 
echo "###########  Enabling Gunicorn Service ###########"
echo
sudo systemctl start gunicorn; 
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl restart gunicorn
sudo systemctl status gunicorn
echo
echo "####################################################################"
echo "###########  Configure Nginix to Proxy Pass to Gunicorn  ###########"
echo "####################################################################"
echo
read -p "Server name or IP adddress > " server_name
sudo rm -f /etc/nginx/sites-enabled/default
sudo rm -f /etc/nginx/sites-enabled/$project_name
echo "server{
	listen 443 ssl;
	server_name $server_name;
	
	ssl_certificate /etc/letsencrypt/live/$server_name/fullchain.pem;
	ssl_certificate_key /etc/letsencrypt/live/$server_name/privkey.pem;
	
	location /media/media/ {
		autoindex on;
		alias $(pwd)/media/;
	}
	
	location /static/ {
		autoindex on;
		alias $(pwd)/static/;
	}
	
	location /robots.txt {
		alias $(pwd)/static/robots.txt;
	}

	location /sitemap.xml {
		alias $(pwd)/static/sitemap.xml;
	}

	location / {
		proxy_pass http://localhost:$gunicorn_port;
	}
}

server {
	listen 80;
	server_name $server_name, www.$server_name;
	return 301 https://couponstown.me\$request_uri;
}

server {
	listen 443;
	server_name www.$server_name;
	return 301 https://couponstown.me\$request_uri;
}" > temp_site1
sudo mv temp_site1 /etc/nginx/sites-available/$project_name
rm -f temp_site1
echo "#############################################################"
echo "##########  Configuring Certbot and Nginx for SSL  ##########"
echo "#############################################################"
sudo apt-get install -y software-properties-common
sudo add-apt-repository universe
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install -y certbot python3-certbot-nginx
echo
echo "##########  Creating Symlink for Nginx Sites  ##########"
sudo ln -s /etc/nginx/sites-available/$project_name /etc/nginx/sites-enabled/$project_name
echo
echo "##########  Testing Nginx  ##########"
sudo nginx -t
echo
echo "##########  Restarting Nginx  ##########"
sudo systemctl restart nginx
sudo systemctl status nginx
echo 
echo "#######################################################"
echo "##########  Creating CouponsTown API Server  ##########"
echo "#######################################################"
echo "[Unit]
Description=CouponsTown API Daemon
After=network.target

[Service]
User=$username
Group=www-data
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/python3 manage.py runserver 0.0.0.0:8000

[Install]
WantedBy=multi-user.target" > temp.txt
sudo mv temp.txt /etc/systemd/system/couponstown.service
sudo systemctl start couponstown
sudo systemctl enable couponstown
sudo systemctl daemon-reload
sudo systemctl restart couponstown
sudo systecmtl status couponstown
echo 
echo "#####################################################################"
echo "##########  Creating CouponsTown Schedule Updater Service  ##########"
echo "#####################################################################"
echo "[Unit]
Description=CouponsTown Schedule Updater Daemon
After=network.target

[Service]
User=$username
Group=www-data
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/python3 schedule_update.py

[Install]
WantedBy=multi-user.target" > temp.txt
sudo mv temp.txt /etc/systemd/system/couponstown_updater.service
sudo systemctl start couponstown_updater
sudo systemctl enable couponstown_updater
sudo systemctl daemon-reload
sudo systemctl restart couponstown_updater
sudo systemctl status couponstown_updater


