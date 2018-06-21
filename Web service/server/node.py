"""
Provide functions to get detail of a device, edit this information,
add new device or delete device from device list of topology.
"""
from flask import request, Blueprint

from db import connect
import functions.nodeFunc as nodeFunc

node = Blueprint('node', __name__)

cursor = connect.cursor()


@node.route('/detail/', methods=['GET'])
def detail():
	try:
		topoId   = request.args.get('topoId')
		deviceId = request.args.get('node')
		
		nodeDetail = nodeFunc.getNodeDetail(topoId, deviceId)
		if not nodeDetail:
			return {'status' : 'Not found'}
	except:
		return {'status': 'error'}

	return nodeDetail


@node.route('/edit/', methods=['POST'])
def edit():
	try:
		topoId = request.args.get('topoId')
		data   = request.get_json()
		
		status = nodeFunc.editNode(topoId, data)

	except:
		return {'status': 'error'}

	return status


@node.route('/delete/', methods=['POST'])
def delete():
	try:
		topoId = request.args.get('topoId')
		node   = request.get_json()['node']

		status = nodeFunc.deleteNode(topoId, node)
	except:
		return {'status': 'error'}

	return status


@node.route('/add/', methods=['POST'])
def add():
	try:
		topoId = request.args.get('topoId')
		data   = request.get_json()['data']

		nodeFunc.addNode(topoId, data)
	except:
		return {'status': 'error'}

	return {'status': 'success'}
