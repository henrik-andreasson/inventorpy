import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
from sqlalchemy import MetaData

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()

from app.models import Audit
audit = Audit()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if app.config['PROXY_FIX'] != 0:
        app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=app.config['PROXY_FIX'], x_host=app.config['PROXY_FIX'])

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.modules.qr import bp as qr_bp
    app.register_blueprint(qr_bp, url_prefix='/qr')

    from app.modules.switch import bp as switch_bp
    app.register_blueprint(switch_bp, url_prefix='/switch')

    from app.modules.server import bp as server_bp
    app.register_blueprint(server_bp, url_prefix='/server')

    from app.modules.pc import bp as pc_bp
    app.register_blueprint(pc_bp, url_prefix='/pc')

    from app.modules.safe import bp as safe_bp
    app.register_blueprint(safe_bp, url_prefix='/safe')

    from app.modules.rack import bp as rack_bp
    app.register_blueprint(rack_bp, url_prefix='/rack')

    from app.modules.network import bp as network_bp
    app.register_blueprint(network_bp, url_prefix='/network')

    from app.modules.hsm import bp as hsm_bp
    app.register_blueprint(hsm_bp, url_prefix='/hsm')

    from app.modules.firewall import bp as fw_bp
    app.register_blueprint(fw_bp, url_prefix='/firewall')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Inventorpy Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/inventorpy.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Inventorpy startup')

    return app


def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from app import models
