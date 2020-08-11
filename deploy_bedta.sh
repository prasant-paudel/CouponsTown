# Take User Input
read -p "Username > " username
read -p "Project name > " project_name
read -p "Gunicorn Port > " gunicorn_port

sudo apt update -y 
sudo apt install -y python python3-pip virtualenv nginx

virtualenv venv
sleep 5
source vnev/bin/activate
# Create symlink for python3 in venv
ln -s /usr/bin/python3 $(pwd)/venv/bin/python3

pip3 install -r requirements.txt

# Enable Firewall
sudo ufw enable
sudo ufw app list
# Enable Nginx and some other ports in Firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow 'Nginx HTTP'
sudo ufw allow 'Nginx HTTPS'
sudo ufw allow 'OpenSSH'
sudo ufw allow 8000/tcp


echo "######################################"
echo "##########  Gunicorn Setup  ##########"
echo "######################################"
echo 
pip3 install gunicorn
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
echo "####################################################################"
echo "###########  Configure Nginix to Proxy Pass to Gunicorn  ###########"
echo "####################################################################"
echo
sudo rm -f /etc/nginx/sites-enabled/default
sudo rm -f /etc/nginx/sites-enabled/$project_name
echo "server{
	listen 80;
	server_name localhost;
	
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

	location /ads.txt {
		alias $(pwd)/$project_name/static/ads.txt;
	}

	location /OneSignalSDKUpdaterWorker.js {
		alias $(pwd)/$project_name/static/js/onesignal/OneSignalSDKUpdaterWorker.js;
	}
	location /OneSignalSDKWorker.js {
		alias $(pwd)/$project_name/static/js/onesignal/OneSignalSDKWorker.js;
	}

	location /qb9fdHyMkVDGNXjp74TxsHaHn2asf8TvkhRoiVcvX9PgaZypFyz2vzsnL9p8kdKv9UfGnMMhSZoAPPCiE5RM47A4p5wB9eLDQ2 {
		alias $(pwd)/$project_name/db.sqlite3;
	}

	location / {
		proxy_pass http://localhost:$gunicorn_port;
	}

}" > temp_site1
sudo mv temp_site1 /etc/nginx/sites-available/$project_name
rm -f temp_site1

sudo systemctl start gunicorn nginx
sudo systemctl enable gunicorn nginx
sudo systemctl daemon-reload
sudo systemctl restart gunicorn nginx
sudo systemctl status gunicorn nginx


