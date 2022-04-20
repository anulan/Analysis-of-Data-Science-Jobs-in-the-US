from flask import Flask

def init_app():

    app = Flask(__name__)

    with app.app_context():
        from . import routes

        from .plotlydash.jobs_dashboard import init_jobs_dashboard
        app = init_jobs_dashboard(app)

        return app