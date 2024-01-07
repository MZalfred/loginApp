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

# Generic function to query the database
def query_db(query, args=(), one=False):
    with sqlite3.connect('fitshirts.db') as conn:
        cur = conn.execute(query, args)
        rv = cur.fetchall()
        return (rv[0] if rv else None) if one else rv

# Route to fetch logs based on a date range
@app.route('/fetch-logs', methods=['GET'])
def fetch_logs():
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    query = 'SELECT * FROM activity_log WHERE DATE(timestamp) BETWEEN ? AND ?'
    data = query_db(query, (start_date, end_date))

    return jsonify(data)

# Route to log activities
@app.route('/activity', methods=['POST'])
def log_activity_route():
    # Route to handle POST requests for logging activities.
    try:
        user_id = request.form['user_id']
        action_type = request.form['action_type']
        log_activity(user_id, action_type)
        return jsonify({"status": "success", "user_id": user_id, "action": action_type})
    except KeyError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# Function to initialize the database
def init_db():
    # Initializes the database and creates necessary tables.
    with sqlite3.connect('fitshirts.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                     (user_id INTEGER PRIMARY KEY, username TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS activity_log 
                     (log_id INTEGER PRIMARY KEY, user_id INTEGER, action_type TEXT, 
                      timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()

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

# Route to fetch total hours
@app.route('/report/total_hours', methods=['GET'])
def total_hours():
    # Route to fetch the total hours worked by a user on a given date.
    user_id = request.args.get('user_id')
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    total_hours = calculate_total_hours(user_id, date)
    return jsonify({'user_id': user_id, 'date': date, 'total_hours': total_hours})

# Function to get activities by date
def get_activities_by_date(user_id, start_date, end_date):
    # Fetches a list of activities for a user within a specified date range.
    return query_db('''SELECT * FROM activity_log WHERE user_id = ? AND 
                       DATE(timestamp) BETWEEN DATE(?) AND DATE(?)''', 
                    (user_id, start_date, end_date))

# Route to fetch activities
@app.route('/activities', methods=['GET'])
def activities():
    user_id = request.args.get('user_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    activities = get_activities_by_date(user_id, start_date, end_date)
    return jsonify(activities)

# Function to get dashboard data
def get_dashboard_data():
    # Fetches data for the admin dashboard.
    return query_db('SELECT * FROM activity_log WHERE user_id >= 60')

# Route for admin dashboard
@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    # Route for an admin dashboard that provides various data points.
    dashboard_data = get_dashboard_data()
    return jsonify({'activities': dashboard_data})

# Route to handle login actions
@app.route('/login', methods=['POST'])
def login():
    user_id = request.form.get('user_id')
    action = request.form.get('action')
    
    if not user_id or action not in ['sign-in', 'sign-out']:
        return jsonify({"error": "Invalid data"}), 400
    
    log_activity(user_id, action)
    return jsonify({"status": "success", "user_id": user_id, "action": action, "timestamp": datetime.now().isoformat()})

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
