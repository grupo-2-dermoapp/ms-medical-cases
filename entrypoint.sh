export FLASK_APP=entrypoint.py
flask db upgrade
flask run --host 0.0.0.0 --port 3020