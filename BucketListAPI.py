from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from instance.config import application_config

app = Flask(__name__)

def Env_name(env):
    app.config.from_object(application_config[env])

Env_name('developmentEnv')
databases = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
