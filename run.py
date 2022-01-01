from application.dash_app import app
from settings.config import config

app.run_server(port=config.port, debug=True)