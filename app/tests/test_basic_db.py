import sqlalchemy
from app import APP
from redis import Redis
from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
import unittest
import requests
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()
 

database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['PG_USER'],
    dbpass=os.environ['PG_PASS'],
    dbhost=os.environ['PG_HOST'],
    dbname=os.environ['PG_DB']
)

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)


# initialize the database connection
db = SQLAlchemy(app)

# initialize database migration management
migrate = Migrate(app, db)
 
 
 
class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
    # executed prior to each test
    def setUp(self):
        global transaction, connection, engine
        # Connect to the database and create the schema within a transaction
        engine = create_engine('postgresql+psycopg2://username:secretpassword@demodb-testing-postgresql.testing.svc.cluster.local/my-database')
        connection = engine.connect()
        transaction = connection.begin()

        str_conn = connection.execute("INSERT INTO guests (name, email) VALUES  ('Colin', 'colin@flugel.it')")
        transaction.commit()
        
        result = connection.execute('select name from guests')
  
        print(str_conn)

        for row in result:
          print("Prueba de busqueda de usuario haciendo un SELECT a la tabla GUESTS:", row['name'])

        
        connection.close()
  

    

#       Base.metadata.create_all(connection)

#        app.config['TESTING'] = True
#        app.config['WTF_CSRF_ENABLED'] = False
#        app.config['DEBUG'] = False
#        app.config['SQLALCHEMY_DATABASE_URI'] 
#        self.app = app.test_client()
#        print self.app
#        db.drop_all()
#        db.create_all()
 
        # Disable sending emails during unit testing
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
 
 
###############
#### tests ####
###############
 
    def test_main_page(self):
        "GET request to url returns a 200"
        url = 'http://demo-mockapp.jx-staging.flugel.it/'
        resp = requests.get(url)
        assert resp.status_code == 200
  #      response = self.app.get('/', follow_redirects=True)
  #      self.assertEqual(response.status_code, 200)
 
 
if __name__ == "__main__":
    unittest.main()
