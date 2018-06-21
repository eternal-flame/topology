"""
Flask web service provide API to work with server database
"""
from flask_api import FlaskAPI
from flask_cors import CORS

import topology
import general
import node
import edge

app = FlaskAPI(__name__)
CORS(app)

app.register_blueprint(topology.topology, url_prefix='/topology')
app.register_blueprint(general.general, url_prefix='/general')
app.register_blueprint(node.node, url_prefix='/node')
app.register_blueprint(edge.edge, url_prefix='/edge')

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
