import os
import regex as re
import atexit
import requests
from threading import Thread
from pytz import timezone
from datetime import datetime
from pasgen import getrandompassword
from forms import SignUpForm, LoginForm, ResetForm, AddExchangerForm, ChangePasswordForm, CommentForm, MainForm, EditForm
from flask import Flask, redirect, url_for, render_template, flash, abort, request, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from forex_python.converter import CurrencyRates
from apscheduler.schedulers.background import BackgroundScheduler
from urllib.parse import urlsplit, urlunsplit


app = Flask(__name__)
Bootstrap(app)

# app.config['ENV'] = 'production'
# app.config['DEBUG'] = True
# app.config['TESTING'] = False

dollarRates = {'USD': 65.14074494, 'EUR': 73.24648392, 'GBP': 84.93819465, 'BTC': 335891.4}

# db connection
db_path = os.path.join(os.path.dirname(__file__), 'users.db')
exchangers_path = os.path.join(os.path.dirname(__file__), 'exchangers.db')
comment_path = os.path.join(os.path.dirname(__file__), 'comment.db')
rates_path = os.path.join(os.path.dirname(__file__), 'rates.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_BINDS'] = {'exchangers': 'sqlite:///{}'.format(exchangers_path),
                                  'comment': 'sqlite:///{}'.format(comment_path),
                                  'rates': 'sqlite:///{}'.format(rates_path)}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '2fHGGFdePK'

db = SQLAlchemy(app)

# Mail config
app.config.from_pyfile('config.cfg')

# Mail settings
mail = Mail(app)
s = URLSafeTimedSerializer('giax5RHYLB')


# login manager section
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


import models
import parser

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def update_data():
    # Timer(interval, update_data, [interval]).start()
    global dollarRates
    try:
        urlUSD = 'https://api.exchangerate-api.com/v4/latest/USD'
        urlEUR = 'https://api.exchangerate-api.com/v4/latest/EUR'
        urlGBP = 'https://api.exchangerate-api.com/v4/latest/GBP'
        urlBTC = 'https://blockchain.info/ticker'

        # Making our request
        response = requests.get(urlUSD)
        dataUSD = response.json()['rates']['RUB']

        response = requests.get(urlEUR)
        dataEUR = response.json()['rates']['RUB']

        response = requests.get(urlGBP)
        dataGBP = response.json()['rates']['RUB']

        response = requests.get(urlBTC)
        dataBTC = response.json()['RUB']['last']

        data = {'USD': dataUSD, 'EUR': dataEUR, 'GBP': dataGBP, 'BTC': dataBTC}

        if data:
            dollarRates = data
    except Exception as e:
        print(str(e))

# UPDATING RATES
scheduler = BackgroundScheduler()
scheduler.add_job(func=parser.run, trigger="interval", seconds=300)
# UPDATING DOLLAR RATES
scheduler.add_job(func=update_data, trigger="interval", seconds=600)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    form = LoginForm()
    form1 = ResetForm()

    if form.validate_on_submit():
        user = db.session.query(models.User).filter_by(email=(form.email.data).lower()).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect('/')

        flash("Invalid email or/and password!")
        return redirect(url_for('login'))

    if form1.validate_on_submit():
        if not db.session.query(models.User).filter_by(email=form1.email.data.lower()).first():
            flash("User with email you entered not found!")
            return redirect(url_for('login'))
        else:
            new_password = getrandompassword()
            curr = db.session.query(models.User).filter_by(email=form1.email.data.lower()).first()
            curr.password = generate_password_hash(new_password, method='sha256')
            db.session.commit()

            msg = Message('Password reset', sender='ouramazingapp@gmail.com', recipients=[form1.email.data])
            msg.html = 'Your new password is <b>{}</b>, you can change it in account settings'.format(new_password)
            Thread(target=send_async_email, args=(app, msg)).start()

            flash('Check your email for further instructions')
            return redirect(url_for('login'))

    return render_template("login.html", form=form, form1=form1)


# SignUp page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect('/')

    form = SignUpForm()
    if form.validate_on_submit():
        if db.session.query(models.User).filter_by(email=(form.email.data).lower()).first():
            flash("User already exists!")
            return redirect(url_for('signup'))
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        if re.search('[a-zA-Z]', form.name.data):
            new_user = models.User(name=form.name.data, email=(form.email.data).lower(), password=hashed_password)

            db.session.add(new_user)
            db.session.commit()

            # Message sending
            token = s.dumps(form.email.data, salt='email-confirm')
            msg = Message('Confirm Email', sender='ouramazingapp@gmail.com', recipients=[form.email.data])

            link = url_for('confirm_email', token=token, _external=True)
            msg.body = 'Your link is {}'.format(link)

            Thread(target=send_async_email, args=(app, msg)).start()
            flash("Success! Now you can log in")
            return redirect(url_for('login'))
        else:
            flash('Invalid name! It must contain at least 1 english letter')
            return redirect(url_for('signup'))

    return render_template('signup.html', form=form)


@app.route('/exchanger/<r>', methods=['GET', 'POST'])
def exchanger(r):
    ex = db.session.query(models.Exchangers).filter_by(id=r).first()
    if not ex:
        abort(404)
    ex_data = [ex.name, ex.country, ex.description, ex.comments, ex.positives, ex.complains, ex.link, ex.id, ex.ownerId,
               ex.image, ex.dateOfCreation]

    badges = []
    if ex.badges:
        badges = ex.badges.split(',')

    form = CommentForm()
    form1 = EditForm()

    comments = db.session.query(models.Comment).filter(models.Comment.exchangerId == r)
    comments = comments[::-1]

    recent = comments[:5]

    if form.validate_on_submit():
        if len(form.review.data) > 5:
            if current_user.id == ex.ownerId:
                new_comment = models.Comment(review=str(form.review.data), type=str(form.type.data),
                                         userId=current_user.id, userName=current_user.name, exchangerId=r, byAdmin=1)
            else:
                new_comment = models.Comment(review=str(form.review.data), type=str(form.type.data),
                                             userId=current_user.id, userName=current_user.name, exchangerId=r, byAdmin=0)

            db.session.add(new_comment)
            # db.session.commit()

            if current_user.id != ex.ownerId:
                if form.type.data == 'Positive':
                    ex.positives = ex.positives + 1
                elif form.type.data == 'Complain':
                    ex.complains = ex.complains + 1
                else:
                    ex.comments = ex.comments + 1

            db.session.commit()
            return redirect('/exchanger/{}'.format(r))

    ex = db.session.query(models.Exchangers).filter_by(id=r).first()
    if form1.validate_on_submit():
        if form1.name.data:
            ex.name = form1.name.data
        if form1.url.data:
            ex.link = form1.url.data
        if form1.description.data:
            ex.description = form1.description.data
        # if form1.picURL.data:
        #     ex.image = form1.picURL.data

        db.session.commit()
        return redirect('/exchanger/{}'.format(r))

    return render_template('exchanger.html', ex_data=ex_data, form=form, comments=comments, recent=recent, form1=form1, badges=badges)


# Sending confirmation link
@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
        curr = db.session.query(models.User).filter_by(email=email).first()
        curr.email_confirmed = 1
        db.session.commit()
    except SignatureExpired:
        return '<h1>The confirmation link has expired</h1>'
    return render_template('confirm_email.html')


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    today = datetime.now().strftime('%A %d %b %Y')
    global dollarRates
    form = MainForm()
    if form.validate_on_submit():
        if form.firstCurr.data == form.secondCurr.data:
            return redirect('/')
        else:
            uri = '/search?in=' + form.firstCurr.data + '&out=' + form.secondCurr.data
            return redirect(uri)
    return render_template('main.html', form=form, dollarRates=dollarRates, today=today)


@app.route('/addexchanger', methods=['GET', 'POST'])
def addexchanger():
    if request.method == 'POST':
        url = request.form.get('url')
        name = request.form.get('name')
        xml = request.form.get('xml')
        country = request.form.get('country')
        description = request.form.get('comments')

        msg = Message('Exchanger adding request', sender='ouramazingapp@gmail.com', recipients=['tbago@yandex.ru'])
        msg.html = str(name) + ' ' + str(url) + ' ' + str(xml) + ' ' + str(country) + ' ' + \
                   str(description)
        Thread(target=send_async_email, args=(app, msg)).start()
        flash("We will check your exchanger and add it to our system")
        return redirect('addexchanger')
    return render_template('addexchanger.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    d = {'WMR': 'WM RUB', 'QWRUB': 'QIWI RUB', 'YAMRUB': 'YNDX RUB', 'BTC': 'BTC', 'SBERRUB': 'RUB'}
    fCurr = request.args.get('in')
    sCurr = request.args.get('out')

    rates = db.session.query(models.Rates).filter_by(type=(fCurr+sCurr)).order_by(models.Rates.coef)

    exchangers = []

    if rates:
        for i in rates:
            exchangers.append(db.session.query(models.Exchangers).filter_by(id=i.exchangerId).first())

    return render_template('search.html', rates=rates, exchangers=exchangers, found=len(exchangers), d=d, fCurr=fCurr,
                           sCurr=sCurr)


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    change_password_form = ChangePasswordForm()
    if change_password_form.validate_on_submit():
        if check_password_hash(current_user.password, change_password_form.current_password.data) and (change_password_form.new_password.data == change_password_form.new_password_confirm.data):
            new_hashed_password = generate_password_hash(change_password_form.new_password.data, method='sha256')

            curr = db.session.query(models.User).filter_by(email=current_user.email).first()
            curr.password = new_hashed_password

            db.session.commit()
            flash('Successfully updated your password!')
            return redirect(url_for('settings'))
        elif check_password_hash(current_user.password, change_password_form.current_password.data) and (change_password_form.new_password.data != change_password_form.new_password_confirm.data):
            flash('Entered new passwords do not match')
            return redirect(url_for('settings'))
        else:
            flash('Current password is wrong!')
            return redirect(url_for('settings'))
    if request.method == 'POST':
        fCurr = request.form.get('first')
        sCurr = request.form.get('second')
        ratio = request.form.get('input')

        try:
            ratio = float(ratio)
            if ratio <= 1:
                flash('Ratio must be bigger than 1')
                return redirect(url_for('settings'))
            try:
                uri = '/data?in=' + fCurr + '&out=' + sCurr
                r = requests.get('http://' + request.host + uri)
                data = r.json()
                if int(data['ratio']) == -1:
                    flash('You can not subscribe on this kind of currency exchange')
                    return redirect(url_for('settings'))
                if ratio > data['ratio']:
                    flash('Your ratio can not be bigger than the current one')
                    return redirect(url_for('settings'))
                print(data['ratio'])
            except Exception as e:
                flash('Some error occurred')
                return redirect(url_for('settings'))
        except Exception as e:
            flash('Ratio input format is wrong!')
            return redirect(url_for('settings'))


    return render_template('settings.html', change_password_form=change_password_form)


# @app.route('/test', methods=['GET', 'POST'])
# def test():
#     return render_template('test.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        url = request.form.get('url')
        name = request.form.get('name')
        email = request.form.get('email')
        subj = request.form.get('subject')
        message = request.form.get('comments')

        msg = Message(subj, sender='ouramazingapp@gmail.com', recipients=['tbago@yandex.ru'])
        msg.html = str(str(name) + ' ' + str(email) + ' ' + str(message))
        Thread(target=send_async_email, args=(app, msg)).start()

        return redirect(url)
    else:
        return abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/terms', methods=['GET', 'POST'])
def terms():
    return render_template('terms.html')


@app.route('/data', methods=['GET', 'POST'])
def data():
    fCurr = request.args.get('in')
    sCurr = request.args.get('out')

    q = {'ratio': -1}

    if fCurr != sCurr:
        try:
            cf = db.session.query(models.Rates).filter_by(type=(fCurr + sCurr)).order_by(models.Rates.coef).first().coef
            q = {'ratio': cf}
        except Exception as e:
            q = {'ratio': -1}

    return jsonify(q)


if __name__ == '__main__':
    app.run(debug=True)

