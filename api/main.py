from flask import Flask, escape, request, jsonify
from classes.easyrsa import EasyRSA
import logging
from os import environ
app = Flask(__name__)
easyrsa = EasyRSA(environ['CONTAINER'])

@app.route('/status', methods=['GET'])
@app.route('/', methods=['GET'])
def status():
    a = easyrsa.status()
    return jsonify(a), 200

@app.route('/list', methods=['GET'])
def list():
    a = easyrsa.list()
    return jsonify(a), 200

@app.route('/create', methods=['POST'])
def create():
    if not request.is_json or 'name' not in request.json:
        return "Bad request", 401
    a = easyrsa.add(request.json['name'])
    if a == 0:
        return "This key already exists", 406
    return jsonify(a), 201

@app.route('/delete', methods=['POST'])
def delete():
    if not request.is_json or 'name' not in request.json:
        return "Bad request", 401
    a = easyrsa.revoke(request.json['name'])
    if a == 0:
        return "Not found", 404
    return "OK", 200

@app.errorhandler(404)
def page_not_found_error(error):
    return "Not found", 404

@app.errorhandler(500)
def internal_server_error(error):
    return "Internal Server Error", 500