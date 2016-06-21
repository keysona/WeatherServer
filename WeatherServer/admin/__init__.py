import flask_login as login
from flask_admin import Admin

from .views import AdminHomeView, ProvinceView, CityView,\
                   CountryView, WeatherHistoryView
from .models import AdminUser, User
from WeatherServer.api.models import Province, City, Country,\
                                         WeatherHistory


def init_login(app):
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.objects(id=user_id).first()


def create_admin(*args, **kwargs):
    admin = Admin(index_view=AdminHomeView(endpoint='admin'), *args, **kwargs)
    admin.add_view(ProvinceView(Province))
    admin.add_view(CityView(City))
    admin.add_view(CountryView(Country))
    admin.add_view(WeatherHistoryView(WeatherHistory))
    return admin


def create_admin_blueprint(admin):
    from flask_admin.base import create_blueprint
    admin_blueprint = create_blueprint(admin)
    return admin_blueprint
