from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# db config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'AFK'

from login import login_bp
from account import account_bp
from upload import upload_bp
from stats import stats_bp

app.register_blueprint(login_bp)
app.register_blueprint(account_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(stats_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)