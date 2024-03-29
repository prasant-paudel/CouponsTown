# Take User Input
read -p "Username > " username
read -p "Project name > " project_name
read -p "Gunicorn Port > " gunicorn_port
read -p "Server Name (Domain Name) > " server_name
read -p "Server IP Address > " ip_address


echo "############################################"
echo "#############  Nginx Setup  ################"
echo "############################################"
echo 

# Exit Virtual Environment if any
deactivate

sudo apt update -y
sudo apt install -y nginx python virtualenv python3-pip

# Install nginx


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
virtualenv venv
sleep 1
source venv/bin/activate
# Create symlink for python3 in venv
ln -s /usr/bin/python3 $(pwd)/venv/bin/python3
echo
echo "######################################"
echo "##########  Gunicorn Setup  ##########"
echo "######################################"
echo 

# install gunicorn
pip3 install gunicorn
# Install dependencies
pip3 install -r requirements.txt
deactivate
# create gunicorn symlink in venv
ls -s /home/$username/.local/bin/gunicorn venv/bin/gunicorn

# Create Gunicorn Service
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
Restart=on-failure

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
sudo rm -f /etc/nginx/sites-enabled/*
echo "server{
	listen 443 ssl;
	server_name $server_name;
	
	ssl_certificate $(pwd)/ssl/certificate.pem;
	ssl_certificate_key $(pwd)/ssl/private_key.pem;
	
	location /media/media/ {
		autoindex on;
		alias $(pwd)/media/;
	}
	
	location /static/ {
		autoindex on;
		alias $(pwd)/$project_name/static/;
	}
	
	location /robots.txt {
		alias $(pwd)/$project_name/static/robots.txt;
	}

	location /sitemap.xml {
		alias $(pwd)/$project_name/static/sitemap.xml;
	}

	location /OneSignalSDKUpdaterWorker.js {
		alias $(pwd)/$project_name/static/js/onesignal/OneSignalSDKUpdaterWorker.js;
	}
	location /OneSignalSDKWorker.js {
		alias $(pwd)/$project_name/static/js/onesignal/OneSignalSDKWorker.js;
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
echo "##########  Creating Symlink for Nginx Sites  ##########"
sudo ln -s /etc/nginx/sites-available/$project_name /etc/nginx/sites-enabled/$project_name
echo
echo "#############################################################"
echo "##########  Configuring Certbot and Nginx for SSL  ##########"
echo "#############################################################"
sudo apt-get install -y software-properties-common
sudo add-apt-repository universe
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install -y certbot python3-certbot-nginx
echo
echo "##########  Testing Nginx  ##########"
sudo nginx -t
echo
echo "##########  Restarting Nginx  ##########"
sudo systemctl restart nginx
sudo systemctl status nginx
echo 
echo "###############################################################"
echo "##########  Creating CouponsTown Development Server  ##########"
echo "###############################################################"
echo "[Unit]
Description=CouponsTown API Daemon
After=network.target

[Service]
User=$username
Group=www-data
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/python3 manage.py runserver 0.0.0.0:8000 --settings \"couponstown.settings.development\"
Restart=on-failure

[Install]
WantedBy=multi-user.target" > temp.txt
sudo mv temp.txt /etc/systemd/system/couponstown.service
echo "[Unit]
Description=CouponsTown API Daemon
After=network.target

[Service]
User=$username
Group=www-data
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/python3 manage.py runserver 0.0.0.0:8006 --settings \"couponstown.settings.development\"
Restart=on-failure

[Install]
WantedBy=multi-user.target" > temp.txt
sudo mv temp.txt /etc/systemd/system/couponstown6.service
echo "[Unit]
Description=CouponsTown API Daemon
After=network.target

[Service]
User=$username
Group=www-data
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/python3 manage.py runserver 0.0.0.0:8007 --settings \"couponstown.settings.development\"
Restart=on-failure

[Install]
WantedBy=multi-user.target" > temp.txt
sudo mv temp.txt /etc/systemd/system/couponstown7.service
echo "[Unit]
Description=CouponsTown API Daemon
After=network.target

[Service]
User=$username
Group=www-data
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/python3 manage.py runserver 0.0.0.0:8008 --settings \"couponstown.settings.development\"
Restart=on-failure

[Install]
WantedBy=multi-user.target" > temp.txt
sudo mv temp.txt /etc/systemd/system/couponstown8.service
echo "[Unit]
Description=CouponsTown API Daemon
After=network.target

[Service]
User=$username
Group=www-data
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/python3 manage.py runserver 0.0.0.0:8009 --settings \"couponstown.settings.development\"
Restart=on-failure

[Install]
WantedBy=multi-user.target" > temp.txt
sudo mv temp.txt /etc/systemd/system/couponstown9.service
echo "[Unit]
Description=CouponsTown API Daemon
After=network.target

[Service]
User=$username
Group=www-data
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/python3 manage.py runserver 0.0.0.0:8010 --settings \"couponstown.settings.development\"
Restart=on-failure

[Install]
WantedBy=multi-user.target" > temp.txt
sudo mv temp.txt /etc/systemd/system/couponstown10.service
echo "[Unit]
Description=CouponsTown API Daemon
After=network.target

[Service]
User=$username
Group=www-data
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/python3 manage.py runserver 0.0.0.0:8011 --settings \"couponstown.settings.development\"
Restart=on-failure

[Install]
WantedBy=multi-user.target" > temp.txt
sudo mv temp.txt /etc/systemd/system/couponstown11.service

sudo systemctl start couponstown couponstown6 couponstown7 couponstown8 couponstown9 couponstown10 couponstown11
sudo systemctl enable couponstown couponstown6 couponstown7 couponstown8 couponstown9 couponstown10 couponstown11
sudo systemctl daemon-reload couponstown6 couponstown7 couponstown8 couponstown9 couponstown10 couponstown11
sudo systemctl restart couponstown couponstown6 couponstown7 couponstown8 couponstown9 couponstown10 couponstown11
sudo systecmtl status couponstown couponstown6 couponstown7 couponstown8 couponstown9 couponstown10 couponstown11
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
Restart=on-failure

[Install]
WantedBy=multi-user.target" > temp.txt
sudo mv temp.txt /etc/systemd/system/couponstown_updater.service
sudo systemctl start couponstown_updater
sudo systemctl enable couponstown_updater
sudo systemctl daemon-reload
sudo systemctl restart couponstown_updater
sudo systemctl status couponstown_updater


