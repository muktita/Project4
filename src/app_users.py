from venv import create
from quart_schema import QuartSchema
from quart import Quart, g, request
from api.game.game import app_create
from api.users.users import app_users
import toml
import logging

app = Quart(__name__)
QuartSchema(app)

app.logger.setLevel(logging.INFO)

#app.register_blueprint(app_create)
app.register_blueprint(app_users)

#config app here
app.config.from_file(f'./config/config.toml', toml.load)


if __name__ == '__main__':
    
    app.run(debug=True)