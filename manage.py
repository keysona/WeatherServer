from flask_script import Manager, Server, Shell
from WeatherServer.api import Province, City, Country
from WeatherServer import app


def _make_context():
    return dict(Province=Province, City=City,
                Country=Country)

manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0', port='5000',
                                        use_debugger=True))
manager.add_command('shell', Shell(make_context=_make_context))

if __name__ == '__main__':
    manager.run()
