from flask import Flask
from controllers.home import home_bp
from controllers.list import list_bp
from controllers.create import create_bp
import os

app = Flask(__name__)

app.register_blueprint(home_bp)
app.register_blueprint(list_bp)
app.register_blueprint(create_bp)

app.secret_key = os.urandom(24)

if __name__ == "__main__":
  app.run(debug=True)

