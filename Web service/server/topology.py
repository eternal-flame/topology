"""
Provide functions to get topology list, add new topology, edit
and delete existing topology, use to store information about
topology to send to rack controllers to get data.
"""
from flask import request, Blueprint

import functions.topoFunc as topoFunc

topology = Blueprint('topology', __name__)


@topology.route('/list/', methods=['GET'])
def list():
	try:
		topoList = topoFunc.getToposList()
	except:
		return {"status": "error"}

	return topoList

	
@topology.route('/detail/', methods=['GET'])
def detail():

	try:
		topoId     = request.args.get('topoId')
		topoDetail = topoFunc.getTopoDetail(topoId)

	except:
		return {'status': 'error'}

	return topoDetail


@topology.route('/add/', methods=['POST'])
def add():
	try:
		# Get data send by client
		data = request.get_json()

		topoFunc.addNewTopo(data)

	except:
		return {'status': 'error'}

	return {'status': 'success'}


@topology.route('/edit/', methods=['POST'])
def edit():
	try:
		data     = request.get_json()
		topoFunc.editTopo(data)

	except:
		return {'status': 'error'}

	return {'status': 'success'}


@topology.route('/delete/', methods=['POST'])
def delete():
	try:
		# Get ID of topology want to delete
		topoId    = request.get_json()['topoId']
		topoFunc.deleteTopo(topoId)

	except:
		return {"status": "error"}

	return {"status": "success"}
