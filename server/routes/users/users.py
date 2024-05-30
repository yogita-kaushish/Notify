from flask import request, Blueprint
from controllers.users.users import create_user, get_users, get_user, update_user, partial_update_user, delete_user


def handle_users():
    if request.method == 'GET':
        return get_users(request)
    elif request.method == 'POST':
        return create_user(request)
    

def handle_user(u_id):
    if request.method == 'GET':
        return get_user(u_id)
    elif request.method == 'PUT':
        return update_user(request)
    elif request.method == 'PATCH':
        return partial_update_user(u_id,request)
    elif request.method == 'DELETE':
        return delete_user(u_id)
