from werkzeug.security import generate_password_hash , check_password_hash

from flask import Blueprint , render_template , request , redirect , url_for , session , flash
from models import Patient
from database import db
from werkzeug.security import generate_password_hash

auth = Blueprint('auth',__name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash

        patient = patient(name=name , email=email , password=hashed_password)

        db.session.add(patient)
        db.session.commit()

        return redirect(url_for('auth_login'))
    
@auth.route('/login' , methods=['GET' , 'POST'])
def login():
    email = request.form['email']
    password = request.form['password']




    admin = Admin.query.filter_by(username=email).first()
    if admin and admin.password == password:
        session['user_id'] = admin.id
        session['role'] = 'admin'

        return redirect(url_for('admin_dashboard'))




    doctor = Doctor.query.filter_by(email=email).first()
    if doctor and check_password_hash(doctor.password , password):
        session['role'] = doctor
        session['user_id'] = doctor.id

        return redirect(url_for('doctor_dashboard'))




    patient = Patient.query.filter_by(email=email).first()
    if patient and check_password_hash(patient.password , password):
        session['role'] = patient
        session['user_id'] = patient.id

        return redirect(url_for('patient_dashboard'))



    flash('invaild credentials')




@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))