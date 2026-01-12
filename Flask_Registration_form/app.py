from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Store registered users (in real app, use database)
registered_users = []

@app.route('/')
def index():
    """Display registration form"""
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    """Handle form submission"""
    # Get form data
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    phone = request.form.get('phone')
    gender = request.form.get('gender')
    country = request.form.get('country')
    
    # Server-side validation
    errors = []
    
    if not username or len(username) < 3:
        errors.append("Username must be at least 3 characters")
    
    if not email or '@' not in email:
        errors.append("Valid email is required")
    
    if not password or len(password) < 6:
        errors.append("Password must be at least 6 characters")
    
    if password != confirm_password:
        errors.append("Passwords do not match")
    
    if errors:
        return render_template('index.html', errors=errors)
    
    # Store user data
    user_data = {
        'username': username,
        'email': email,
        'phone': phone,
        'gender': gender,
        'country': country,
        'registered_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    registered_users.append(user_data)
    
    return render_template('success.html', user=user_data)

@app.route('/users')
def show_users():
    """Display all registered users"""
    return render_template('users.html', users=registered_users)

if __name__ == '__main__':
    print("="*50)
    print(f"Flask Server Started: {datetime.now()}")
    print("Visit: http://127.0.0.1:5000")
    print("="*50)
    app.run(debug=True)