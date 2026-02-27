from flask import Flask, request, render_template, redirect, url_for, session
import logging
import re

app = Flask(__name__)
app.secret_key = 'super_secret_honeypot_key'

# Cấu hình log
logging.basicConfig(filename='hacker_activity.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Dữ liệu giả
fake_database = [
    {"id": 101, "name": "Nguyen Van An", "position": "System Admin", "email": "admin@company.com", "salary": "$5000"},
    {"id": 102, "name": "Tran Thi Binh", "position": "HR Manager", "email": "hr@company.com", "salary": "$3000"},
    {"id": 103, "name": "Le Hoang Nam", "position": "Senior Developer", "email": "dev01@company.com", "salary": "$4000"},
    {"id": 104, "name": "Boss", "position": "CEO", "email": "ceo@company.com", "salary": "$99999"},
]

def analyze_attack(input_string):
    input_string = input_string.lower()
    if re.search(r"(union|select|insert|update|drop|alert|' or 1=1|--|#)", input_string):
        return "SQL INJECTION"
    if re.search(r"(<script>|javascript:|onerror|onload|alert\()", input_string):
        return "XSS ATTACK"
    if re.search(r"(\.\./|\.\.\\|/etc/passwd)", input_string):
        return "PATH TRAVERSAL"
    return "SAFE"

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ip = request.remote_addr

        log_msg = f"!!! CAPTURED CREDENTIALS !!! IP: {ip} | User: {username} | Pass: {password}"
        print(f"\033[93m{log_msg}\033[0m")
        logging.info(f"TYPE: CREDENTIAL_HARVEST | IP: {ip} | User: {username} | Pass: {password}")

        session['logged_in'] = True
        session['user'] = username
        return redirect(url_for('search'))

    return render_template('login.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    results = []
    error = None

    if request.method == 'POST':
        query = request.form.get('query', '')
        ip = request.remote_addr

        attack_type = analyze_attack(query)

        if attack_type != "SAFE":
            log_msg = f"!!! ATTACK DETECTED ({attack_type}) !!! IP: {ip} | Payload: {query}"
            print(f"\033[91m{log_msg}\033[0m")
            logging.info(f"TYPE: WEB_ATTACK | IP: {ip} | Attack: {attack_type} | Payload: {query}")

            error = f"SQL Error: Syntax error near '{query}' at line 1."
        else:
            results = [user for user in fake_database if query.lower() in user['name'].lower() or query.lower() in user['position'].lower()]

    return render_template('search.html', results=results, username=session.get('user'), error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    print(">>> COMBO HONEYPOT RUNNING ON PORT 8081...")
    app.run(host='0.0.0.0', port=8081)
