. ../followDem-venv/bin/activate

export FLASK_APP=app.py
export DATABASE_URL=postgresql://postgres:@localhost/followdem
flask run