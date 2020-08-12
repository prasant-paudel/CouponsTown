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
    echo "########### Created Load Balancer ###########"
	echo --> load_balancer$port.service

    sudo systemctl start load_balancer$port.service
    sudo systemctl enable load_balancer$port.service
    sudo systemctl daemon-reload
    sudo systemctl restart load_balancer$port.service

done



