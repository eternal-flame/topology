"""
Provide functions to synchronize data from racks controller
to server, get general information of a topology to draw.
"""
from flask import request, Blueprint

from db import connect
import functions.generalFunc as generalFunc


general = Blueprint('general', __name__)
cursor  = connect.cursor()


@general.route('/discover/', methods=['GET'])
def discover():
	try:
		topoId = request.args.get('topoId')
		generalFunc.discoverNetwork(topoId)

	except:
		return {"status": "error"}

	return {"status": "success"}


@general.route('/synchronize/', methods=['GET'])
def synchronize():
	try:
		topoId = request.args.get('topoId')
		generalFunc.syncTable(topoId)

	except:
		return {"status": "error"}

	connect.commit()
	return {"status": "success"}


@general.route('/detail/', methods=['GET'])
def detail():
	# try:
	topoId = request.args.get('topoId')

	detail = generalFunc.getTopoDetail(topoId)

	return detail

	# except:
	# 	return {'status': 'error'}


@general.route('/save/', methods=['GET'])
def save():
	try:
		connect.commit()
	except:
		return {"status": "error"}

	return {"status": "success"}


@general.route('/discard/', methods=['GET'])
def discard():
	try:
		connect.rollback()
	except:
		return {"status": "error"}

	return {"status": "success"}
