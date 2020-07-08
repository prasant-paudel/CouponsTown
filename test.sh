username=prasant

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


