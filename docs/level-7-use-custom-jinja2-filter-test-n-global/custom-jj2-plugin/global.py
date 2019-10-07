from moban.plugins.jinja2.extensions import jinja_global

jinja_global('global', dict(hello='world'))
