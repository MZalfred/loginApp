from flask import Flask, request, jsonify
import sqlite3

# Initialize Flask app
app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return 'Hello, this is FIT SHIRTS app backend!'

# Function to log activities
def log_activity(user_id, action_type):
    with sqlite3.connect('fitshirts.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO activity_log (user_id, action_type) VALUES (?, ?)', (user_id, action_type))

# Route to log activities
@app.route('/activity', methods=['POST'])
def log_activity_route():
    try:
        user_id = request.form['user_id']
        action_type = request.form['action_type']  # 'sign-in', 'sign-out', etc.
        log_activity(user_id, action_type)
        return jsonify({"status": "success", "user_id": user_id, "action": action_type})
    except KeyError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# Function to initialize the database
def init_db():
    with sqlite3.connect('fitshirts.db') as conn:
        c = conn.cursor()
        # Create necessary tables
        # ... (your table creation code here)

# Call init_db to initialize database
init_db()

# Function to get activities by date
def get_activities_by_date(user_id, start_date, end_date):
    with sqlite3.connect('fitshirts.db') as conn:
        c = conn.cursor()
        query = '''SELECT * FROM activity_log WHERE user_id = ? AND 
                   DATE(timestamp) BETWEEN DATE(?) AND DATE(?)'''
        c.execute(query, (user_id, start_date, end_date))
        return c.fetchall()

# Route to handle login actions
@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        user_action = request.form['action']  # 'sign-in' or 'sign-out'
        # Assuming log_login is defined elsewhere or you can define it
        # log_login(username, user_action)
        return f"{username} {user_action}"
    except KeyError:
        return "Missing username or action", 400

# Route to fetch activities
@app.route('/activities', methods=['GET'])
def activities():
    user_id = request.args.get('user_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    activities = get_activities_by_date(user_id, start_date, end_date)
    return jsonify(activities)

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
