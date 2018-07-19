<<<<<<< HEAD
release: yes "yes" | python manage.py migrate
web: uwsgi --http-socket=:$PORT --master --workers=2 --threads=8 --die-on-term --wsgi-file=bakerydemo/wsgi_production.py  --static-map /media/=/app/bakerydemo/media/ --offload-threads 1
=======
web: gunicorn gettingstarted.wsgi
>>>>>>> 353f0ebb142065a5637d555813b6efce41e85f92
