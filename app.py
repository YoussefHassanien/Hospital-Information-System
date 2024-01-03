from flask import Flask, render_template, request, redirect, session
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "queensqueries"

database_session = psycopg2.connect(
     database="Hospital",
     port=5432,
     host="localhost",
     user="postgres",
     password="1792003"
)

cursor = database_session.cursor(cursor_factory=psycopg2.extras.DictCursor)

@app.route('/', methods=['GET', 'POST'])
def home():  # put application's code here
    return render_template('Home.html')

@app.route('/Surgery', methods=['GET', 'POST'])
def surgery():  # put application's code here
    return render_template('Surgery.html')
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
        return redirect('/admin')
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
    return render_template('Admin_Patients_Database.html')


@app.route('/Admin_Doctors_Database', methods=['GET', 'POST'])
def doctors_database():
    patient1 = "hamsa"
    return render_template('Admin_Doctors_Database.html', patient1=patient1)

@app.route("/patient", methods=["GET", "POST"])
def patient():

    return render_template("Patient.html")


if __name__ == '__main__':
    app.run()
