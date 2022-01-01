from application.dash_app import app
from settings.config import config

# server
server = app.server

if __name__ == '__main__':
	app.run_server(debug=True)