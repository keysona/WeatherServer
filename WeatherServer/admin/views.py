import flask_login as login

from flask import request, redirect, url_for, render_template
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.base import AdminIndexView, expose

from .forms import LoginForm


class AdminHomeView(AdminIndexView):

    @expose('/', methods=('GET', 'POST'))
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login'))
        return super().index()

    @expose('/login', methods=('GET', 'POST'))
    def login(self):
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate():
            user = form.get_user()
            login.login_user(user)
            return redirect(url_for('.index'))
        return render_template('form.html', form=form)

    @expose('/logout', methods=('GET', 'POST'))
    def logout(self):
        login.logout_user()
        return redirect(url_for('.index'))


class ProvinceView(ModelView):
    pass


class CityView(ModelView):
    pass


class CountryView(ModelView):
    pass


class WeatherHistoryView(ModelView):
    pass
