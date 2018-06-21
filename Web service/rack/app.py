from flask_api import FlaskAPI
from flask_cors import CORS

import db
import snmp
import synchronize

app = FlaskAPI(__name__)
CORS(app)

app.register_blueprint(snmp.snmp,url_prefix='/snmp')
app.register_blueprint(synchronize.synchronize,url_prefix='/sync')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=1234)