import os
import xmltodict
import json
import logging
from flask import Flask, request, abort, g
from requests.exceptions import ConnectionError
# from oracle_db import add_row
from mongo_db import add_row
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth


# Initializing the Extensions
db = SQLAlchemy()
auth = HTTPBasicAuth()

# Logging Variable
request_count = 0

def create_app():

    app = Flask(__name__)

    logging.basicConfig(filename='application.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    app.config['SECRET_KEY'] = 'key for authentication'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHMEY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    from auth_database import Authorized

    # Creating the Authorized Users table using sqlite engine
    with app.app_context():
        if not os.path.exists('db.sqlite3'):
            db.create_all()
    
    @auth.verify_password
    def verify_password(username, password):
        user = Authorized.query.filter_by(username=username).first()

        if not user or not user.verify_password(password):
            return False
        
        g.user = user
        return True


    @app.route('/xml-payload/authorized_users/', methods=['POST'])
    def add_user():
        username = request.json.get('username')
        password = request.json.get('password')

        if username is None or password is None:
            # abort(400)
            return 'Invalid Entry (username or password is missing)'
        if Authorized.query.filter_by(username=username).first() is not None:
            # abort(400)
            return 'Already an authorized user.'

        user = Authorized(username=username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()

        return 'User added to the list of Authorized Users.'



    @app.route('/xml-payload/', methods=['POST'])
    @auth.login_required
    def parse_xml():
        if request.method == 'POST':
            try:
                
                payload = request.data
                json_payload = xmltodict.parse(payload)

                family = json_payload['ApplicationMessage']['family']
                message_type = json_payload['ApplicationMessage']['type']
                businessObjectId = json_payload['ApplicationMessage']['businessObjectId']
                payload = json_payload['ApplicationMessage']['payloadXml']

                parsed_payload = json.dumps(payload)

                add_row(family, message_type, businessObjectId,parsed_payload)
                

                response = {'family': family, 'type':message_type, 'businessObjectId':businessObjectId, 'payload':parsed_payload}

                if response:
                    global request_count
                    request_count+=1
                    app.logger.info('Data Injected Successfully!')
                    app.logger.info(f'Injection Count: {request_count}')
                    app.logger.info(f'Injected Data: {response}')

                    # return 'Data Injected Successfully!'
                    return (json.dumps(response),
                    201,
                    {'Content-Type': "application/json"}
                    )
                else:
                    message = "Data Injection Failed, Please look into the issue!"
                    app.logger.info(f'{message}')
                    
                    return f'{message}'

            except ConnectionError as ce:
                print(ce)
    
    return app