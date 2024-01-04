from flask import Flask, render_template, request, redirect, session
import psycopg2.extras
import random

app = Flask(__name__)
app.secret_key = "queensqueries"

database_session = psycopg2.connect(
     database="hospital_youssef",
     port=5432,
     host="localhost",
     user="postgres",
     password="Youssef.8.3"
)

cursor = database_session.cursor(cursor_factory=psycopg2.extras.DictCursor)

@app.route('/', methods=['GET', 'POST'])
def home():  # put application's code here
    return render_template('Home.html')

@app.route('/Surgery', methods=['GET', 'POST'])
def surgery():  # put application's code here
    return render_template('Surgery.html')
@app.route('/ICU', methods=['GET', 'POST'])
def ICU():  # put application's code here
    return render_template('ICU.html')
@app.route('/doctor', methods=['GET', 'POST'])
def doctor():  # put application's code here
    return render_template('Doctor.html')
@app.route('/admin', methods=['GET', 'POST'])
def admin():  # put application's code here
    return render_template('Admin_Profile.html')


@app.route("/Home", methods=['GET', 'POST'])
def home_from_other_pages():  # put application's code here
    return render_template('Home.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    message = ''
    userssn = request.form.get("pssn")
    userfname = request.form.get("pfname")
    userlname = request.form.get("plname")
    useremail = request.form.get("pEmail")
    userpassword = request.form.get("ppassword")
    useraddress = request.form.get("paddress")
    userdate = request.form.get("pbirthdate")
    usergender = request.form.get("pGender")
    userphone = request.form.get("pphone")

    if useremail:
        cursor.execute('SELECT pemail FROM patient where pemail = %s', (useremail,))
        if cursor.fetchone():
            message = 'Account already exits!'
        else:
            cursor.execute('INSERT INTO patient(pssn, pfname, plname, pEmail, ppassword, paddress, pbirthdate, '
                           'pGender, pphone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (userssn, userfname, userlname, useremail, userpassword, useraddress, userdate,
                            usergender, userphone))
            database_session.commit()
            message = 'You have successfully registered!'

    return render_template("Registeration.html", msg=message)

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ''
    useremail = request.form.get("pEmail")
    userpassword = request.form.get("ppassword")
    cursor.execute('SELECT * FROM patient WHERE pEmail = %s AND ppassword = %s', (useremail, userpassword))
    patient_result = cursor.fetchone()

    # Check in the doctor table
    cursor.execute('SELECT * FROM doctor WHERE dEmail = %s AND dpassword = %s', (useremail, userpassword))
    doctor_result = cursor.fetchone()

    cursor.execute('SELECT * FROM admin WHERE aemail = %s AND apassword = %s', (useremail, userpassword))
    admin_result = cursor.fetchone()

    if patient_result:
        session['user'] = dict(patient_result)
        message = 'Logged in as a patient!'
        return redirect('/patient')
    elif doctor_result:
        session['user'] = dict(doctor_result)
        message = 'Logged in as a doctor!'
        return redirect('/doctor')
    elif admin_result:
        session['user'] = dict(doctor_result)
        message = 'Logged in as an admin!'
        return redirect('/Admin_Charts')
    else:
        message = 'Please enter correct email and password'
    return render_template('Home.html', msg=message)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session['user'] = None
    return redirect('/login')


@app.route('/Admin_Charts', methods=['GET', 'POST'])
def admin_charts():
    return render_template('Admin_Charts.html')


@app.route('/Admin_Patients_Database', methods=['GET', 'POST'])
def patients_database():
    patient1 = "hamsa"
    return render_template('Admin_Patients_Database.html', patient1=patient1)
@app.route('/Admin_Add_Doctor', methods=['GET', 'POST'])
def add_doctor():
    message = ''
    doctor_ssn = request.form.get("Doctor-SSN")
    doctor_fname = request.form.get("Doctor-FName")
    doctor_lname = request.form.get("Doctor-LName")
    doctor_email = request.form.get("Doctor-Email")
    doctor_password = request.form.get("Doctor-Password")
    doctor_address = request.form.get("Doctor-Address")
    doctor_birthdate = request.form.get("Doctor-Birthdate")
    doctor_gender = request.form.get("Doctor-Gender")
    doctor_phone = request.form.get("Doctor-Phone")
    doctor_salary = request.form.get("Doctor-Salary")
    doctor_education = request.form.get("Doctor-Education")
    doctor_specialization = request.form.get("Doctor-Specialisation")
    doctor_department_number = request.form.get("Doctor-Department-Number")
    cursor.execute('SELECT DEmail FROM Doctor where DEmail = %s', (doctor_email,))
    if cursor.fetchone():
        message = 'Doctor already exits in the database!'
    else:
        cursor.execute('INSERT INTO Doctor(DSSN, DFname, DLname, DEmail, DPassword, DAddress, DBirthdate, '
                       'DGender, DPhone, DEducation, DSalary, Specialization, DNo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (doctor_ssn, doctor_fname, doctor_lname, doctor_email, doctor_password, doctor_address, doctor_birthdate,
                        doctor_gender, doctor_phone,doctor_education,doctor_salary,doctor_specialization, doctor_department_number))
        database_session.commit()
        message = 'You have successfully added a new doctor to the database!'

    return render_template("Admin_Doctors_Database.html", admin_adding_warning=message)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    message = ''
    username = request.form.get("cname")
    useremail = request.form.get("cemail")
    userphone = request.form.get("cphone")
    usermessage = request.form.get("cmessage")

    cursor.execute('INSERT INTO contact(cname, cemail, cphone, cmessage) '
                   ' VALUES (%s, %s, %s, %s)',
                   (username, useremail, userphone, usermessage))
    database_session.commit()
    message = 'Your response has been recorded!'

    return render_template("Home.html")

@app.route("/book", methods=["GET", "POST"])
def book():
    message = ''
    userssn = request.form.get("inputPatientSSN")
    doctorspecialization = request.form.get("inputDoctorName")
    depname = request.form.get("inputDepartmentName")
    userphone = request.form.get("inputPhone")
    usersymptoms = request.form.get("inputSymptoms")
    userdate = request.form.get("inputDate")

    cursor.execute('SELECT did FROM doctor WHERE specialization = %s ORDER BY RANDOM() LIMIT 1',
                   (doctorspecialization,))
    result = cursor.fetchone()
    #if result:
        #cursor.execute('INSERT INTO examines(did)'
                       #'VALUES (%s)',
                     #  (result))
        #database_session.commit()

    cursor.execute('SELECT pid FROM patient WHERE pssn= %s', (userssn,))
    result1 = cursor.fetchone()
    #if result1:
        #cursor.execute('INSERT INTO examines(pid)'
                      # 'VALUES (%s)',
                       #(result1))
       # database_session.commit()
    if result and result1:
        cursor.execute('INSERT INTO examines(pid, did, department_name, phone, symptoms, start_date)'
                       'VALUES (%s, %s, %s, %s, %s, %s)',
                       (result1[0], result[0], depname, userphone, usersymptoms, userdate))
        database_session.commit()
        message = 'Your response has been recorded!'
    else:
        message = 'Error, doctor or patient not found'

    return render_template("Home.html", msg=message)

@app.route('/Admin_Add_Patient', methods=['GET', 'POST'])
def add_patient():
    message = ''
    patient_ssn = request.form.get("Patient-SSN")
    patient_fname = request.form.get("Patient-FName")
    patient_lname = request.form.get("Patient-LName")
    patient_email = request.form.get("Patient-Email")
    patient_password = request.form.get("Patient-Password")
    patient_address = request.form.get("Patient-Address")
    patient_birthdate = request.form.get("Patient-Birthdate")
    patient_gender = request.form.get("Patient-Gender")
    patient_phone = request.form.get("Patient-Phone")
    patient_medical_status = request.form.get("Patient-Medical-Status")
    patient_medical_history = request.form.get("Patient-Medical-History")
    patient_doctor_id = request.form.get("Patient-Doctor-ID")

    cursor.execute('SELECT pEmail FROM Patient where pEmail = %s', (patient_email,))
    if cursor.fetchone():
        message = 'Patient already exits in the database!'
    else:
        cursor.execute('INSERT INTO Patient(PSSN, PFname, PLname, pEmail, ppassword, Paddress, Pbirthdate, '
                       'Pgender, Pphone, medical_history, medical_status, DID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (patient_ssn, patient_fname, patient_lname, patient_email, patient_password, patient_address, patient_birthdate,
                        patient_gender, patient_phone, patient_medical_status, patient_medical_history, patient_doctor_id))
        database_session.commit()
        message = 'You have successfully added a new patient to the database!'

    return render_template("Admin_Patients_Database.html", admin_adding_warning=message)

@app.route('/Admin_Doctors_Database', methods=['GET', 'POST'])
def doctors_database():
    patient1 = "hamsa"
    return render_template('Admin_Doctors_Database.html', patient1=patient1)

@app.route("/patient", methods=["GET", "POST"])
def patient():

    return render_template("Patient.html")

if __name__ == '__main__':
    app.run()
