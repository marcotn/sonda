set -e

python manage.py migrate --noinput

if [ "$DEBUG" == "1" ]; then
  python manage.py runserver 0.0.0.0:8000
else
  gunicorn --bind=0.0.0.0:8000 --workers=3 --max-requests=1000 --log-level=error sonda.wsgi:application
fi
