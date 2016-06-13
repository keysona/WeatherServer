from flask_script import Manager, Server
from WeatherServer import app


def _make_context():
    return dict()

manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0', port='5000',
                                        use_debugger=True))

if __name__ == '__main__':
    manager.run()

