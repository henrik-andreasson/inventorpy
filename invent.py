from app import create_app, db, cli
from app.models import User, Service
from app.modules.server.models import Server
from app.modules.hsm.models import HsmDomain, HsmPed, HsmPin, HsmPciCard, HsmBackupUnit

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
