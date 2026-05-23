from flask import Flask
import config
from extensions import db, socketio
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY

    # SQLAlchemy configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register Blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.patient import patient_bp
    from routes.doctor import doctor_bp
    from routes.ai import ai_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(ai_bp)

    socketio.init_app(app)
    import events # Register socket events

    # Create tables
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)

