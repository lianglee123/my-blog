from flask import request, jsonify
from . import api


@api.errorhandler(404)
def page_not_found(e):
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response


@api.errorhandler(500)
def internal_server_error(e):
    response = jsonify({'error': 'internal server error'})
    response.status_code = 500
    return response


def bad_request(message):
    response = jsonify({'error': 'bad reqeust', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response
