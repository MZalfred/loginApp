from datetime import datetime
from flask import Flask, request, jsonify
import sqlite3

# Initialize Flask app
app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    # A simple route that returns a greeting message when visited.
    return 'Hello, this is FIT SHIRTS app backend!'

# Function to log activities
def log_activity(user_id, action_type):
    # Connects to the database and logs the specified activity for a user.
    with sqlite3.connect('fitshirts.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO activity_log (user_id, action_type) VALUES (?, ?)', (user_id, action_type))

# Route to log activities
@app.route('/activity', methods=['POST'])
def log_activity_route():
    # Route to handle POST requests for logging activities.
    try:
        user_id = request.form['user_id']
        action_type = request.form['action_type']  # 'sign-in', 'sign-out', etc.
        log_activity(user_id, action_type)
        return jsonify({"status": "success", "user_id": user_id, "action": action_type})
    except KeyError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# Function to initialize the database
def init_db():
    # Initializes the database and creates necessary tables.
    with sqlite3.connect('fitshirts.db') as conn:
        c = conn.cursor()
        # Create necessary tables
        # ... (your table creation code here)

# Call init_db to initialize database
init_db()

def calculate_total_hours(user_id, date):
    # Calculates the total hours logged by a user on a specific date.
    with sqlite3.connect('fitshirts.db') as conn:
        c = conn.cursor()
        query = '''SELECT SUM(julianday(end_time) - julianday(start_time)) * 24 as total_hours
                   FROM activity_log 
                   WHERE user_id = ? AND DATE(timestamp) = ? AND action_type IN ('sign-in', 'sign-out')'''
        c.execute(query, (user_id, date))
        result = c.fetchone()
        return result[0] if result else 0

@app.route('/report/total_hours', methods=['GET'])
def total_hours():
    # Route to fetch the total hours worked by a user on a given date.
    user_id = request.args.get('user_id')
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))  # default to current date
    total_hours = calculate_total_hours(user_id, date)
    return jsonify({'user_id': user_id, 'date': date, 'total_hours': total_hours})

# Function to get activities by date
def get_activities_by_date(user_id, start_date, end_date):
    # Fetches a list of activities for a user within a specified date range.
    with sqlite3.connect('fitshirts.db') as conn:
        c = conn.cursor()
        query = '''SELECT * FROM activity_log WHERE user_id = ? AND 
                   DATE(timestamp) BETWEEN DATE(?) AND DATE(?)'''
        c.execute(query, (user_id, start_date, end_date))
        return c.fetchall()

# Route to handle login actions
@app.route('/login', methods=['POST'])
def login():
    # Handles user login actions. Currently, it only returns the username and action.
    try:
        username = request.form['username']
        user_action = request.form['action']  # 'sign-in' or 'sign-out'
        # Assuming log_login is defined elsewhere or you can define it
        # log_login(username, user_action)
        return f"{username} {user_action}"
    except KeyError:
        return "Missing username or action", 400

@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    # Placeholder route for an admin dashboard.
    # In a real application, implement queries to gather and return necessary data.
    dashboard_data = {
        'total_users': 0,  # Replace with actual data
        'recent_activities': []  # Replace with actual data
    }
    return jsonify(dashboard_data)

# Route to fetch activities
@app.route('/activities', methods=['GET'])
def activities():
    # Fetches and returns a list of activities for a user within a specified date range.
    user_id = request.args.get('user_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    activities = get_activities_by_date(user_id, start_date, end_date)
    return jsonify(activities)

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
