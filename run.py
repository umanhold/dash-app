from dash_app import app
from settings.config import config

app.run_server(host=config.host, port=config.port)