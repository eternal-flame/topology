"""
Provide functions to add new edge between two nodes,
edit port status of two endpoint and delete a existing edge.
"""
from flask import request, Blueprint

from db import connect
import functions.edgeFunc as edgeFunc

edge = Blueprint('edge', __name__)

cursor = connect.cursor()


@edge.route('/edit/', methods=['POST'])
def edit():
	try:
		topoId = request.args.get('topoId')
		data   = request.get_json()

		edgeFunc.editEdge(topoId, data)
	except:
		return {'status': 'error'}

	return {'status': 'success'}


@edge.route('/delete/', methods=['POST'])
def delete():
	try:
		topoId    = request.args.get('topoId')
		connectId = request.get_json()['edge']

		status = edgeFunc.deleteEdge(topoId, connectId)
	except:
		return {'status': 'error'}

	return status


@edge.route('/add/', methods=['POST'])
def add():
	try:
		topoId = request.args.get('topoId')
		data   = request.get_json()['data']

		edgeFunc.addEdge(topoId, data)
	except:
		return {'status': 'error'}

	return {'status': 'success'}
