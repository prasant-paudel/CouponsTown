# Create Backend Services
read -p "Username > " username
read -p "Project name > " project_name
read -p "
1. Development
2. Production

SELECT > " deploy_mode

if [ $deploy_mode -eq 2 ]; then
	read -p "Domain Name or IP Address > " domain_name
fi
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
    echo "########### Created Load Balancer ###########"
	echo "--> load_balancer$port.service"

    sudo systemctl start load_balancer$port.service
    sudo systemctl enable load_balancer$port.service
    sudo systemctl daemon-reload
    sudo systemctl restart load_balancer$port.service

done


sudo rm -f /etc/nginx/sites-enabled/*

echo "upstream backend {" > temp.txt
for port in $ports
do 
    echo "	server localhost:$port;" >> temp.txt
done
echo "}" >> temp.txt
if [ $deploy_mode -eq 2 ] ; then
	echo "
	server{
		listen 443 ssl;
		server_name $domain_name;
		
		ssl_certificate $(pwd)/ssl/certificate.pem;
		ssl_certificate_key $(pwd)/ssl/private_key.pem;
	" >> temp.txt
else
	echo "
	server{
		listen 80;
		server_name localhost;
	" >> temp.txt
fi

echo "	location /media/media/ {
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

sudo systemctl daemon-reload
sudo systemctl restart nginx
sudo systemctl status nginx

