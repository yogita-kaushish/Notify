from utilities.database import execute_query

def get_user_roles(request):
    result = execute_query('Select * from users')
    return result

def get_user_role(request):
    return 'get_by_id req'

def create_user_role(request):
    return 'post'

def update_user_role(request):
    return 'put req'

def partial_update_user_role(request):
    return 'patch req'

def delete_user_role(request):
    return 'user deleted'

