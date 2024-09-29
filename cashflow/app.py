from flask import Flask
from extensions import db, migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

# Import routes after initializing the app
from routes import *

if __name__ == '__main__':
    app.run(debug=True,port=3500)