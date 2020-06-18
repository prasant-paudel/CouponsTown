import os
while 1:
    try:
        os.system('sudo python3 manage.py runserver 0.0.0.0:80')
    except:
        continue

