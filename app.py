from flask import Flask , render_template , url_for , session , redirect           #Flask = the main web app framework
from database import db            #Imports the db object you created
                                   #This connects Flask to your database

def create_app():          #It creates and returns the Flask app
    app=Flask(__name__)    #Creates a Flask application
                           #__name__ tells Flask where the app is located

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hms.db'       #Tells Flask which database to use
                                                                     #sqlite:///hms.db means : use SQLite , create a file named hms.db
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False         #Turns off an unnecessary feature , Saves memory

    app.config['SECRET_KEY'] = 'super-secret-key'

    db.init_app(app)         #Connects Flask app with SQLAlchemy

    from auth import auth
    app.register_blueprint(auth)

    # ✅ ADMIN DASHBOARD
    @app.route('/admin/dashboard')
    def admin_dashboard():
        if session.get('role') != 'admin':
            return redirect(url_for('auth.login'))
        return render_template('admin_dashboard.html')

    # ✅ DOCTOR DASHBOARD
    @app.route('/doctor/dashboard')
    def doctor_dashboard():
        if session.get('role') != 'doctor':
            return redirect(url_for('auth.login'))
        return render_template('doctor_dashboard.html')

    # ✅ PATIENT DASHBOARD
    @app.route('/patient/dashboard')
    def patient_dashboard():
        if session.get('role') != 'patient':
            return redirect(url_for('auth.login'))
        return render_template('patient_dashboard.html')
    
    with app.app_context():
        import models       #Imports all database models (tables)
        db.create_all()
        models.create_admin_if_not_exists()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)