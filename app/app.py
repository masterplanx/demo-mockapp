"""
high level support for doing this and that.
"""
import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from flask_migrate import Migrate



DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['PG_USER'],
    dbpass=os.environ['PG_PASS'],
    dbhost=os.environ['PG_HOST'],
    dbname=os.environ['PG_DB']
)

APP = Flask(__name__)
APP.config.update(
    SQLALCHEMY_DATABASE_URI=DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# initialize the database connection
DB = SQLAlchemy(APP)

# initialize database migration management
MIGRATE = Migrate(APP, DB)

@APP.route('/')
def view_registered_guests():
    """Return the pathname of the KOS root directory."""
    from models import Guest
    guests = Guest.query.all()
    return render_template('guest_list.html', guests=guests)


@APP.route('/register', methods=['GET'])
def view_registration_form():
    """Return the pathname of the KOS root directory."""
    return render_template('guest_registration.html')


@APP.route('/register', methods=['POST'])
def register_guest():
    """Return the pathname of the KOS root directory."""
    from models import Guest
    name = request.form.get('name')
    email = request.form.get('email')

    guest = Guest(name, email)
    DB.session.add(guest)
    DB.session.commit()

    return render_template(
        'guest_confirmation.html', name=name, email=email)



@APP.route('/cache')
def hello():
    """Return the pathname of the KOS root directory."""
    redis = Redis(
        host=os.environ['REDIS_HOST'],
        port=os.environ['REDIS_PORT2'],
        db=0,
        password=os.environ['RD_PASS']
        )
    redis.incr('hits')
    return 'This Flask demo has been viewed %s time(s).' % redis.get('hits')
