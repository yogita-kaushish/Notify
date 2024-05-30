from utilities.database import execute_query


def get_users(request):
    return execute_query('Select * from users;')


def get_user(u_id):
    return execute_query('Select * from users where user_id = %(user_id)s;', {"user_id": u_id})


def create_user(request):
    if request.content_type != 'application/json':
        return {'error': 'Unsupported Media Type: Content-Type must be application/json'}, 415

    data = request.json
    if not data:
        return {'error': 'No data provided'}, 400

    required_fields = ['age', 'balance', 'email', 'user_id']
    for field in required_fields:
        if field not in data:
            return {'error': f'Missing required field: {field}'}, 400

    # Check if user_id exists
    check_user_query = "SELECT 1 FROM users WHERE user_id = %(user_id)s"
    try:
        existing_user = execute_query(check_user_query, {'user_id':  data['user_id']})
        if existing_user:
            return {'error': 'User ID already exists'}, 400
    except Exception as e:
        return {'error': f'Error checking user ID: {str(e)}'}, 500

    data['is_active'] = False

    fields = ', '.join(data.keys())
    values = ', '.join([f"%({field})s" for field in data.keys()])
    print(f"values={values}")
    sql_query = f"""
    INSERT INTO users ({fields})
    VALUES ({values})
    RETURNING user_id
    """

    try:
        result = execute_query(sql_query, data)
        print(f"result={result[0]}")
        if result:
            return {'message': 'User created successfully', 'user_id': data['user_id']}, 201
        else:
            return {'error': 'Failed to create user'}, 500
    except Exception as e:
        return {'error': f'Failed to create user: {str(e)}'}, 500


def update_user(request):
    if request.content_type != 'application/json':
        return {'error': 'Unsupported Media Type: Content-Type must be application/json'}, 415

    data = request.json
    if not data:
        return {'error': 'No data provided'}, 400

    # Assuming the 'users' table has fields 'user_id', 'username', 'email', 'age', etc.
    required_fields = ['age', 'balance', 'email','user_id']
    for field in required_fields:
        if field not in data:
            return {'error': f'Missing required field: {field}'}, 400

    user_id = data['user_id']

    # Check if user_id exists
    check_user_query = "SELECT 1 FROM users WHERE user_id = %(user_id)s"
    try:
        existing_user = execute_query(check_user_query, {'user_id': user_id})
    except Exception as e:
        return {'error': f'Error checking user ID: {str(e)}'}, 500

    if existing_user:
        # Update existing user
        set_clause = ', '.join([f"{field} = %({field})s" for field in data.keys() if field != 'user_id'])
        update_user_query = f"""
        UPDATE users 
        SET {set_clause}
        WHERE user_id = %(user_id)s
        """
        try:
            result = execute_query(update_user_query, data)
            return {'message': 'User updated successfully'}, 200
        except Exception as e:
            return {'error': f'Failed to update user: {str(e)}'}, 500
    else:
        # Create new user
        fields = ', '.join(data.keys())
        values = ', '.join([f"%({field})s" for field in data.keys()])
        insert_user_query = f"""
        INSERT INTO users ({fields})
        VALUES ({values})
        RETURNING user_id
        """
        try:
            result = execute_query(insert_user_query, data)
            if result:
                return {'message': 'User created successfully', 'user_id': data['user_id']}, 201
            else:
                return {'error': 'Failed to create user'}, 500
        except Exception as e:
            return {'error': f'Failed to create user: {str(e)}'}, 500


def partial_update_user(u_id, request):
    if request.content_type != 'application/json':
        return {'error': 'Unsupported Media Type: Content-Type must be application/json'}, 415

    data = request.json
    if not data:
        return {'error': 'No data provided'}

    try:
        user_id = int(u_id)
    except ValueError:
        return {'error': 'Invalid user ID'}

    set_clause = ', '.join([f"{field} = %({field})s" for field in data.keys()])
    sql_query = f"""
    UPDATE users 
    SET {set_clause}
    WHERE user_id = %(user_id)s
    """
    return execute_query(sql_query, {**data, 'user_id': user_id})


def delete_user(u_id):
    try:
        user_id = int(u_id)
    except ValueError:
        return {'error': 'Invalid user ID'}

    sql_query = """
    DELETE FROM users
    WHERE user_id = %(user_id)s
    """

    try:
        result = execute_query(sql_query, {'user_id': user_id})
        return result
    except Exception as e:
        return {'error': f'Failed to delete user: {str(e)}'}



