from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager
from app import app, db, api
from consumer.models import Service, Users, UserLevel
from scheduler.models import AlertDetail, Alert, AlertStatus
from consumer import consumerRouter
from scheduler import schedulerRouter
from consumer.api import ServiceRegistration, UserRegistration, EditService, EditUser
from consumer.views import notif
from scheduler.ivr_workflow import initiate, menu

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def runserver():
    app.register_blueprint(consumerRouter)
    app.register_blueprint(schedulerRouter)
    api.add_resource(ServiceRegistration, '/oncall/service')
    api.add_resource(EditService, '/oncall/service/<string:service_id>')
    api.add_resource(UserRegistration, '/oncall/user')
    api.add_resource(EditUser, '/oncall/user/<string:email>')
    app.run(
        host=app.config['APP_HOSTNAME'],
        #host='localhost',
        port=app.config['APP_PORT'],
        debug=app.config['DEBUG'])


@manager.command
def set_alert_status():
    """
    Set Alert status in DB
    :return:
    """
    alert_statuses = AlertStatus.ALERT_STATUSES
    for status in alert_statuses:
        alert = AlertStatus(status=status[0])
        db.session.add(alert)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
