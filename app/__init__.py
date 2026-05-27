from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes.incidents import incidents_bp
    from app.routes.safety import safety_bp

    app.register_blueprint(incidents_bp)
    app.register_blueprint(safety_bp)

    return app