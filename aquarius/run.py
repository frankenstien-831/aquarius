from aquarius.myapp import app
from aquarius.app.assets import assets
from flasgger import Swagger
from flask import jsonify
from aquarius.config import Config
from aquarius.constants import BaseURLs
from aquarius.constants import Metadata
import configparser

config = Config(filename=app.config['CONFIG_FILE'])
aquarius_url = config.aquarius_url


def get_version():
    conf = configparser.ConfigParser()
    conf.read('.bumpversion.cfg')
    return conf['bumpversion']['current_version']


app.config['SWAGGER'] = {
    'title': Metadata.TITLE,
    'version': get_version(),
    'description': Metadata.DESCRIPTION + '`' + aquarius_url + '`.',
    # 'basePath': BaseURLs.BASE_AQUARIUS_URL,
    # 'host': 'localhost:5000'
}
swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": BaseURLs.SWAGGER_URL
}


@app.route("/")
def version():
    info = dict()
    info['software'] = Metadata.TITLE
    info['version'] = get_version()
    return jsonify(info)


app.register_blueprint(assets, url_prefix=BaseURLs.ASSETS_URL)
swag = Swagger(app, config=swagger_config)


if __name__ == '__main__':
    if isinstance(config.aquarius_url.split(':')[-1], int):
        app.run(host=config.aquarius_url.split(':')[1],
                port=config.aquarius_url.split(':')[-1])
    else:
        app.run()
