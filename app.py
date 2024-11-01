# app.py
from flask import Flask, render_template, request, redirect, url_for, flash

from model import db, User, Cv
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Session
from flask import Flask, render_template, request, Response, send_file
from io import BytesIO
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

user_data = []


@login_manager.user_loader
def load_user(user_id):
    session = Session(db.engine)
    return session.get(User, int(user_id))

@app.route('/')
@login_required
def index():
    cvs = Cv.query.all()
    return render_template('index.html', cvs=cvs)

@app.route('/index')
@login_required
def indexa():
    cvs = Cv.query.all()
    return render_template('index.html', cvs=cvs)


@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    users = User.query.all()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_user.html', users=users)

@app.route('/generate_cv', methods=['GET', 'POST'])
@login_required
def generate_cv():
    def generate_pdf_file():
        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        p.drawString(100, 750, "CV")

        y = 700
        for cv in user_data:
            p.drawString(100, y - 60, f"firstname: {cv['firstname']}")
            p.drawString(100, y - 80, f"lastname: {cv['lastname']}")
            p.drawString(100, y - 100, f"birthday: {cv['birthday']}")
            p.drawString(100, y - 120, f"address: {cv['address']}")
            p.drawString(100, y - 140, f"phone: {cv['phone']}")
            p.drawString(100, y - 160, f"job: {cv['job']}")
            p.drawString(100, y - 180, f"education: {cv['education']}")
            p.drawString(100, y - 200, f"summery: {cv['summery']}")
            y -= 60

        p.showPage()
        p.save()

        buffer.seek(0)
        return buffer
    cvs = Cv.query.all()
    if request.method == 'POST':
        try:
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            birthday = request.form['birthday']
            address = request.form['address']
            phone = request.form['phone']
            job = request.form['job']
            education = request.form['education']
            summery = request.form['summery']
            new_Cv = Cv(firstname=firstname, lastname=lastname, birthday=birthday,
                        address=address, phone=phone, job=job, education=education, summery=summery)
            db.session.add(new_Cv)
            db.session.commit()
            if firstname and lastname and birthday and address and phone and job and  education and summery :
                user_data.append({
                    'firstname' : firstname,
                    'lastname' : lastname,
                    'birthday' : birthday,
                    'address' : address,
                    'phone' : phone,
                    'job' : job,
                    'education' : education,
                    'summery' : summery
                })
            pdf_file = generate_pdf_file()
            response = send_file(
                pdf_file,
                as_attachment=True,
                download_name=f'cv_{firstname}.pdf',
                mimetype='application/pdf'
            )
            flash('CV generated successfully!')
            return response
        except KeyError as e:
            flash(f'Missing form variable: {str(e)}')
    return render_template('generate_cv.html', cvs=cvs)

@app.route('/remove_user', methods=['GET', 'POST'])
@login_required
def remove_user():
    users = User.query.all()
    if request.method == 'POST':
        username = request.form['username']
        user_to_remove = User.query.filter_by(username=username).first()
        if user_to_remove:
            db.session.delete(user_to_remove)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            flash('User not found!')
    return render_template('remove_user.html', users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password!')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
