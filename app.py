from flask import Flask
from database import db

def create_app():
    app=Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hms.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        import models
        db.create_all()
        models.create_admin_if_not_exists()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)