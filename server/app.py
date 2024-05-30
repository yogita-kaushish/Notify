from flask import Flask
from routes.users.users import handle_users, handle_user
from routes.users.user_roles import handle_user_roles
from routes.utils.error_handling import handle_error_404, handle_error_405

app = Flask(__name__)

# Middleware Setup

# Application Handling Routes
app.route('/api/v1/users', methods=['GET', 'POST'])(handle_users)
app.route('/api/v1/users/<u_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])(handle_user)
app.route('/api/v1/users', methods=['GET', 'POST'])(handle_user_roles)
# app.route('/api/v1/users/str:<r_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])(handle_user_role)

# Error Handling Routes
app.errorhandler(404)(handle_error_404)
app.errorhandler(405)(handle_error_405)

if __name__ == '__main__':
    app.run(debug=True)
