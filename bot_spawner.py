import threading
import subprocess
import time
import random

def run_bot(bot_id, ip):
    cmd = f"python bot_client.py --id {bot_id} --ip {ip}"
    subprocess.Popen(cmd.split(), shell=False)

if __name__ == "__main__":
    num_bots = 20
    for i in range(num_bots):
        bot_id = f"BOT_{random.randint(1000, 9999)}"
        bot_ip = f"10.0.0.{random.randint(1, 255)}"  # Genera IP casuale
        threading.Thread(target=run_bot, args=(bot_id, bot_ip)).start()
        time.sleep(random.uniform(0.1, 0.5))
    print(f"[+] Spawned {num_bots} bots with unique IPs")