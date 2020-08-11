# Create Backend Services
read -p "Username > " username
read -p "Project name > " project_name

ports="8002 8003 8004 8005"

for port in $ports
do
    echo "########### Creating Load Balancer $port ###########"
    sudo echo "[Unit]
    Description=Load Balancer Daemon $port
    After=network.target

    [Service]
    User=$username
    Group=root
    WorkingDirectory=$(pwd)
    ExecStart=$(pwd)/venv/bin/gunicorn --access-logfile - --workers 3 --bind 0.0.0.0:$port $project_name.wsgi:application
    Restart=on-failure

    [Install]" > temp.txt
    sudo mv temp.txt /etc/systemd/system/load_balancer$port.service
    echo "########### Created Load Balancer $port ###########"

    sudo systemctl start load_balancer$port.service
    sudo systemctl enable load_balancer$port.service
    sudo systemctl daemon-reload
    sudo systemctl restart load_balancer$port.service
    sudo systemctl status load_balancer$port.service

done

sudo rm -f /etc/nginx/sites-enabled/*

echo "upstream backend {" > temp.txt
for port in $ports
do 
    echo "  server localhost:$port;" >> temp.txt
done

echo "}
server{
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

	location /OneSignalSDKUpdaterWorker.js {
		alias $(pwd)/$project_name/static/js/onesignal/OneSignalSDKUpdaterWorker.js;
	}

	location /OneSignalSDKWorker.js {
		alias $(pwd)/$project_name/static/js/onesignal/OneSignalSDKWorker.js;
	}

	location / {
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
		proxy_pass http://backend;
	}

}" >> temp.txt
sudo mv temp.txt /etc/nginx/sites-available/$project_name
rm -f temp.txt

echo "##########  Creating Symlink for Nginx Sites  ##########"
sudo ln -s /etc/nginx/sites-available/$project_name /etc/nginx/sites-enabled/$project_name

sudo systemctl restart nginx
sudo systemctl status nginx

