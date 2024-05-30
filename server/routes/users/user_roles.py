from controllers.users.user_roles import get_user_roles, create_user_role

def handle_user_roles(request):
    if request.method == 'GET':
        return get_user_roles(request)
    elif request.method == 'POST':
        return create_user_role(request)


# def handle_user_role(request):
#     if request.method == 'GET':
#         msg = get_by_id(request)
#         return msg
#     elif request.method == 'PUT':
#         msg = put(request)
#         return msg
#     elif request.method == 'PATCH':
#         msg = patch(request)
#         return msg
#     elif request.method == 'DELETE':
#         msg = delete(request)
#         return msg
#     else:
#         return msg