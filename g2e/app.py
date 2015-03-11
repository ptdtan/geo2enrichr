"""This module starts the g2e server and handles all valid, incoming requests.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import sys
import flask

from core.util.crossdomain import crossdomain
from core.extractionmaker import extraction_maker


app = flask.Flask(__name__, static_url_path='')
app.debug = True


ALLOWED_ORIGINS = '*'
ENTRY_POINT = '/g2e'
# PURPLE_WIRE: If we want to be able to spin up multiple instances of g2e,
# this needs to be either configurable or automatically generated.
SERVER_ROOT = '/Users/gwg/g2e'


# http://superuser.com/questions/149329/what-is-the-curl-command-line-syntax-to-do-a-post-request
# curl --data "geo_dataset=GDS5077" http://localhost:8083/g2e/extract
# curl --data "geo_dataset=GDS5077&platform=GPL10558&A_cols=GSM1071454,GSM1071455&B_cols=GSM1071457,GSM1071455" http://localhost:8083/g2e/extract

# curl --data "geo_dataset=GDS5077&platform=GPL10558&A_cols=GSM1071454,GSM1071455&B_cols=GSM1071457,GSM1071455" http://localhost:8083/g2e/extract


# git diff --stat
# git diff --shortstat

# last release: b30a09a90ce3ab4582b5546b0e98bf7c9500c514
# current: 595aa71294dadd3f5334ac6bd364f614fd377689


@app.route(ENTRY_POINT + '/', methods=['GET'])
@crossdomain(origin='*')
def index():
	directory = SERVER_ROOT + '/g2e/webapp'
	return flask.send_from_directory(directory, 'index.html')


@app.route(ENTRY_POINT + '/extract', methods=['GET', 'PUT', 'POST', 'OPTIONS'])
@crossdomain(origin=ALLOWED_ORIGINS, headers=['Content-Type'])
def extract():
	"""Single entry point for extracting a gene list from a SOFT file.
	Delegates to constructors that handle data processing and further
	delegation to the DAO and ORM.
	"""
	if flask.request.method == 'PUT' or flask.request.method == 'POST':
		return flask.jsonify({
			'extraction_id': extraction_maker(args=flask.request.form)
		})
	elif flask.request.method == 'GET':
		return flask.jsonify(
			extraction_maker(id=flask.request.args.get('id'))
		)
	

if __name__ == '__main__':
	if len(sys.argv) > 1:
		port = int(sys.argv[1])
	else:
		# Defined by AMP
		port = 8083
	if len(sys.argv) > 2:
		host = sys.argv[2]
	else:
		host = '0.0.0.0'
	app.run(port=port, host=host)
