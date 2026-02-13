"""
Auth Routes - Authentication and authorization
"""

from flask import render_template, session, redirect, url_for, request, flash, current_app
from utils.security import get_admin_credentials, get_client_ip, log_ip_activity, log_audit_event
from utils.data import load_data, get_or_create_workspace
from werkzeug.security import check_password_hash, generate_password_hash
from models import User
from extensions import db
from . import auth_bp


@auth_bp.route('/dashboard/login', methods=['GET', 'POST'])
def login():
    """Admin and User login"""
    ADMIN_CREDENTIALS = get_admin_credentials()
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        client_ip = get_client_ip()

        # Check main Admin
        if username == ADMIN_CREDENTIALS.get('username') and ADMIN_CREDENTIALS.get('username'):
            if check_password_hash(ADMIN_CREDENTIALS['password_hash'], password):
                session['admin_logged_in'] = True
                session['is_admin'] = True
                session['is_demo_mode'] = False
                session['is_demo'] = False
                session['is_verified'] = True
                session['username'] = username
                flash('Admin Login Successful!', 'success')
                log_ip_activity('admin_login', f"User: {username}")
                return redirect(url_for('dashboard.index'))

        # Check users in database first
        db_user = User.query.filter_by(username=username).first()
        if db_user and check_password_hash(db_user.password_hash, password):
            session['admin_logged_in'] = True
            session['user_id'] = db_user.id
            session['username'] = db_user.username
            session['is_admin'] = (db_user.role == 'admin')
            session['is_demo'] = db_user.is_demo
            session['is_verified'] = db_user.is_verified
            # Set demo mode from database
            if db_user.role == 'admin':
                session['is_demo_mode'] = False
            else:
                session['is_demo_mode'] = db_user.is_demo

            # If the user must change their password on first login, force them to do so
            if db_user.must_change_password:
                session['force_change_password'] = True
                log_audit_event('force_password_required', username=db_user.username, details='First-login password change required')
                flash('You must change your password before continuing.', 'warning')
                return redirect(url_for('dashboard.change_password'))

            flash(f'Welcome back, {username}!', 'success')
            log_ip_activity('user_login', f"User: {username}")
            return redirect(url_for('dashboard.index'))
        
        # Fallback: Check users in data.json for backward compatibility
        data = load_data()
        users = data.get('users', [])
        for user in users:
            if user['username'] == username and check_password_hash(
                    user['password_hash'], password):
                # Check if user exists in DB, if not, create it
                db_user = User.query.filter_by(username=username).first()
                if not db_user:
                    current_app.logger.info(f"Creating DB user for {username} from JSON data")
                    workspace = get_or_create_workspace(username, user.get('name', username))
                    db_user = User(
                        username=username,
                        password_hash=user['password_hash'],
                        email=user.get('email', ''),
                        role=user.get('role', 'user'),
                        is_demo=user.get('is_demo', True),
                        must_change_password=user.get('must_change_password', False),
                        workspace_id=workspace.id
                    )
                    db.session.add(db_user)
                    db.session.commit()
                    current_app.logger.info(f"Created DB user {username} with workspace {workspace.id}")
                else:
                    current_app.logger.info(f"DB user {username} already exists")
                
                session['admin_logged_in'] = True
                session['user_id'] = db_user.id if db_user else user['id']
                session['username'] = user['username']
                session['is_admin'] = (user.get('role') == 'admin')
                session['is_demo'] = user.get('is_demo', True)
                session['is_verified'] = user.get('is_verified', False)
                session['is_demo_mode'] = user.get('is_demo', True)

                if user.get('must_change_password', False):
                    session['force_change_password'] = True
                    flash('You must change your password before continuing.', 'warning')
                    return redirect(url_for('dashboard.change_password'))

                flash(f'Welcome back, {username}!', 'success')
                log_ip_activity('user_login', f"User: {username}")
                return redirect(url_for('dashboard.index'))

        flash('Invalid credentials. Please try again.', 'error')
        log_ip_activity('failed_login', f"Username: {username}")

    return render_template('dashboard/login.html')


@auth_bp.route('/dashboard/logout')
def logout():
    """Logout current user"""
    from utils.decorators import login_required
    
    if 'admin_logged_in' not in session:
        flash('Please login to access this page.', 'error')
        return redirect(url_for('auth.login'))
    
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/dashboard/register', methods=['GET', 'POST'])
def register():
    """Register new user and sync with management dashboard"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('dashboard/register.html')
            
        # Check if user already exists
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username or email already exists.', 'error')
            return render_template('dashboard/register.html')
            
        try:
            # Create a professional workspace for the new user
            workspace_name = f"{username}'s Portfolio"
            workspace = get_or_create_workspace(username, workspace_name)
            
            # Create the user in the database
            new_user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                role='user',
                is_active=True,
                is_verified=False,
                is_demo=True,
                workspace_id=workspace.id
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! You can now log in.', 'success')
            log_ip_activity('user_registration', f"User: {username}")
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration error: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'error')
            
    return render_template('dashboard/register.html')
