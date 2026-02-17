'''import os
import math
import re
import hashlib
import secrets
import string
import requests
from flask import Flask, render_template, request, jsonify

# --- CONFIGURATION: FIX TEMPLATE ERROR ---
# This forces Flask to look for index.html in the SAME folder as this script
base_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=base_dir)

# --- FEATURE 1: ROBUST PASSWORD GENERATOR ---
def generate_strong_password(length=16, use_symbols=True, use_numbers=True):
    """
    Generates a cryptographically secure random password.
    """
    chars = string.ascii_letters
    if use_numbers:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

# --- FEATURE 2: ENTROPY CALCULATOR (Math) ---
def calculate_entropy(password):
    """
    Calculates bits of entropy based on character pool size.
    """
    pool_size = 0
    if re.search(r'[a-z]', password): pool_size += 26
    if re.search(r'[A-Z]', password): pool_size += 26
    if re.search(r'[0-9]', password): pool_size += 10
    if re.search(r'[^a-zA-Z0-9]', password): pool_size += 32
    
    if pool_size == 0: return 0
    
    entropy = len(password) * math.log2(pool_size)
    return round(entropy, 2)

# --- FEATURE 3: TIME TO CRACK ESTIMATOR (New) ---
def calculate_crack_time(entropy):
    """
    Estimates time to crack assuming a high-end GPU cluster 
    (100 Billion guesses/second).
    """
    # 2^entropy = Total combinations
    try:
        combinations = 2 ** entropy
        seconds = combinations / 100_000_000_000 # 100 Billion guesses/sec
    except OverflowError:
        return "Centuries+" 

    if seconds < 1: return "Instant"
    if seconds < 60: return f"{round(seconds)} seconds"
    if seconds < 3600: return f"{round(seconds/60)} minutes"
    if seconds < 86400: return f"{round(seconds/3600)} hours"
    if seconds < 31536000: return f"{round(seconds/86400)} days"
    if seconds < 31536000 * 100: return f"{round(seconds/31536000)} years"
    return "Centuries+"

# --- FEATURE 4: REAL DATA BREACH CHECK (Pwned API) ---
def check_pwned_api(password):
    """
    Checks the 'Have I Been Pwned' API securely using k-Anonymity.
    Only sends the first 5 chars of the hash.
    """
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1password[:5], sha1password[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    
    # CRITICAL FIX: Add a User-Agent so the API doesn't block us
    headers = {
        'User-Agent': 'PasswordToolkit-StudentProject-v1'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code != 200:
            return {"error": f"API Error: {response.status_code}"}
        
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return {"found": True, "count": int(count)}
        
        return {"found": False, "count": 0}
        
    except Exception as e:
        print(f"API Connection Error: {e}")
        return {"found": False, "error": str(e)}

# --- FLASK ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    password = data.get('password', '')
    
    if not password:
        return jsonify({"error": "No password provided"}), 400

    # 1. Run Calculations
    entropy = calculate_entropy(password)
    crack_time = calculate_crack_time(entropy)
    breach_status = check_pwned_api(password)
    
    # 2. Determine Labels
    strength_label = "WEAK"
    if entropy > 45: strength_label = "DECENT" 
    if entropy > 80: strength_label = "STRONG"

    # 3. Send Response
    return jsonify({
        "entropy": entropy,
        "strength_label": strength_label,
        "crack_time_display": crack_time,       # <--- New Data for Frontend
        "breach_found": breach_status.get('found', False),
        "breach_count": breach_status.get('count', 0)
    })

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    length = int(data.get('length', 16))
    use_sym = data.get('symbols', True)
    use_num = data.get('numbers', True)
    
    password = generate_strong_password(length, use_sym, use_num)
    return jsonify({"password": password})

if __name__ == '__main__':
    print("------------------------------------------------")
    print("SERVER RUNNING! Open this URL in your browser:")
    print("http://127.0.0.1:5000")
    print("------------------------------------------------")
    app.run(debug=True)'''