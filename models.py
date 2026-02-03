from database import db
from datetime import datetime

class Admin(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(100) , unique=True , nullable=False)
    password = db.Column(db.String(200) , nullable=False)




class Department(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(100) , unique=True , nullable=False)
    discription = db.Column(db.Text)

    doctors = db.relationship('Doctor' , backref='department' , lazy=True)




class Doctor(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(100) , nullable=False)
    email = db.Column(db.String(120) , unique=True , nullable=False)
    password = db.Column(db.String(200) , nullable=False)
    experience_years = db.Column(db.Integer)
    department_id = db.Column(db.Integer , db.ForeignKey('department.id'))
    is_active = db.Column(db.Boolean , default=True)

    appointments = db.relationship('Appointment' , backref='doctor' , lazy=True)




class Patient(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(100) , nullable=False)
    email = db.Column(db.String(120) , unique=True , nullable=False)
    password = db.Column(db.String(200) , nullable=False)
    contact = db.Column(db.String(15))
    is_active = db.Column(db.Boolean, default=True)

    appointments = db.relationship('Appointment' , backref='patient' , lazy=True)




class Appointment(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    doctor_id = db.Column(db.Integer , db.ForeignKey('doctor.id') , nullable=False)
    patient_id = db.Column(db.Integer , db.ForeignKey('patient.id') , nullable=False)
    date = db.Column(db.Date , nullable=False)
    time = db.Column(db.String(15) , nullable=False) 
    status = db.Column(db.String(20) , default='Booked')

    treatment = db.relationship('Treatment' , backref='appointment' , uselist=False)




class Treatment(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    appointment_id = db.Column(db.Integer , db.ForeignKey('appointment.id') , nullable=False , unique=True)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes =db.Column(db.Text)




class DoctorAvailability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer,db.ForeignKey('doctor.id'),nullable=False)
    date = db.Column(db.Date, nullable=False)
    is_available = db.Column(db.Boolean, default=True)




def create_admin_if_not_exists():
    from database import db
    admin = Admin.query.filter_by(username="admin").first()
    if not admin:
        admin = Admin(username="admin" , password="admin123")
        db.session.add(admin)
        db.session.commit()
