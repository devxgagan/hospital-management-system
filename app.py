from flask import Flask , render_template , url_for , session , redirect           #Flask = the main web app framework
from database import db            #Imports the db object you created
                                   #This connects Flask to your database
from models import Doctor , Patient , Appointment
from werkzeug.security import generate_password_hash
from datetime import date , timedelta



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
        
        doctor_count = Doctor.query.count()
        patient_count = Patient.query.count()
        appointment_count = Appointment.query.count()

        return render_template('admin_dashboard.html' , doctor_count=doctor_count , patient_count=patient_count , appointment_count=appointment_count)




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




    @app.route('/admin/doctor/add' , methods=['GET' , 'POST'])
    def add_doctor():
        if session.get('role') !='admin':
            return redirect(url_for('auth.login'))
        
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            password = generate_password_hash(request.form['password'])
            dept_id = request.form['department_id']


            doctor = Doctor(name=name , email=email , password=password , department_id=dept_id)

            db.session.add(doctor)
            db.session.commit()

            return redirect(url_for('admin_dashboard'))

        departments = Department.query.all()
        return render_template('admin_add_doctor.html', departments=departments)




    @app.route('/admin/doctors/edit/<int:id>' , methods=['GET' , 'POST'])
    def edit_doctor(id):
        if session.get('role') != 'admin':
            return redirect(url_for('auth.login'))
        
        doctor = Doctor.query.get_or_404(id)

        if request.method == 'POST' :
            doctor.name = request.form['name']
            doctor.name = request.form['email']
            db.session.commit()

            return redirect(url_for('admin_dashboard'))
        
        return render_template('admin_edit_doctor.html' , doctor=doctor)




    @app.route('/admin/appointments')
    def admin_appointments():
        if session.get('role') != 'admin' :
            return redirect(url_for('auth.login'))
        
        appointments = Appointment.query.order_by(Appointment.date).all()
        return render_template('admin_appointments.html' , appointments=appointments)




    @app.route('/admin/search')
    def admin_search():
        if session.get('role') != 'admin':
            return redirect(url_for('auth.login'))
        
        q = request.args.get('q' , '')

        doctors = Doctor.query.filter(Doctor.name.contains(q)).all()

        patients = Patient.query.filter(Patient.name.contains(q)).all()

        return render_template('admin_search.html' , doctors=doctors , patients=patients)




    @app.route('/admin/doctors/disable/<int:id>')
    def disable_doctor(id):
        doctor = Doctor.query.get(id)
        doctor.is_active = False
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    


    
    @app.route('/admin/patients/disable/<int:id>')
    def disable_patient(id):
        patient = Patient.query.get(id)
        patient.is_active = False
        db.session.commit()
        return redirect(url_for('admin_dashboard'))





    @app.route('/doctor/dashboard')
    def doctor_dashboard():
        if session.get('role') != 'doctor':
            return redirect(url_for('auth.login'))
        
        doctor_id = session['user_id']

        today = date.today()
        week_later = today + timedelta(days=7)

        appointments  =Appointment.query.filter(Appointment.doctor_id == doctor_id , Appointment.date >= today , Appointment.date , Appointment.date <=week_later).all()
        return render_template('doctor_dashboard.html' , appointments = appointments)




    @app.route('/doctor/appointment/<int:id>/complete')
    def complete_appointment(id):

        if session.get('role') != 'doctor':
            return redirect(url_for('auth.login'))

        appt = Appointment.query.get(id)
        appt.status = "Completed"
        db.session.commit()

        return redirect(url_for('doctor_dashboard'))



    @app.route('/doctor/appointment/<int:id>/cancel')
    def cancel_appointment(id):

        if session.get('role') != 'doctor':
            return redirect(url_for('auth.login'))

        appt = Appointment.query.get(id)
        appt.status = "Cancelled"
        db.session.commit()

        return redirect(url_for('doctor_dashboard'))




    @app.route('/doctor/treatment/<int:appt_id>', methods=['GET','POST'])
    def add_treatment(appt_id):

        if session.get('role') != 'doctor':
            return redirect(url_for('auth.login'))

        if request.method == 'POST':

            treatment = Treatment(
                appointment_id=appt_id,
                diagnosis=request.form['diagnosis'],
                prescription=request.form['prescription'],
                notes=request.form['notes']
            )

            db.session.add(treatment)
            db.session.commit()

            return redirect(url_for('doctor_dashboard'))

        return render_template('doctor_treatment.html')




    @app.route('/doctor/patient/<int:patient_id>/history')
    def patient_history(patient_id):

        if session.get('role') != 'doctor':
            return redirect(url_for('auth.login'))

        treatments = Treatment.query.join(Appointment).filter(
            Appointment.patient_id == patient_id
        ).all()
        return render_template('doctor_history.html', treatments=treatments)
    


    

    @app.route('/doctor/availability', methods=['GET','POST'])
    def doctor_availability():

        if session.get('role') != 'doctor':
            return redirect(url_for('auth.login'))

        if request.method == 'POST':

            for d in request.form.getlist('dates'):
                av = DoctorAvailability(
                    doctor_id=session['user_id'],
                    date=d
                )
                db.session.add(av)

            db.session.commit()
            return redirect(url_for('doctor_dashboard'))

        return render_template('doctor_availability.html')





    with app.app_context():
        import models       #Imports all database models (tables)
        db.create_all()
        models.create_admin_if_not_exists()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)