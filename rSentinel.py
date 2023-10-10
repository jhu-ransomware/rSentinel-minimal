import socket
import threading
import time
import json
import logging
import inspect

logging.basicConfig(level=logging.INFO)

CONSTANTS = None

with open("constants.json", "r") as f:
    CONSTANTS = json.load(f)

PEER_IPS = [(ip, CONSTANTS["PORT"]) for ip in CONSTANTS["PEER_IPS"]]
logging.info(f"Peer IP addresses: {PEER_IPS}")

my_ip = socket.gethostbyname(socket.gethostname())
MY_ADDRESS = (my_ip, CONSTANTS["PORT"])
logging.info(f"My IP address: {my_ip}")
STATUS_MESSAGE = "Alive and well"  # The status message you want to send

def send_status():
    global MY_ADDRESS
    global STATUS_MESSAGE

    while True:
        for address in PEER_IPS:
            if address != MY_ADDRESS:  # Don't send a message to yourself
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect(address)
                        s.sendall(STATUS_MESSAGE.encode())
                except ConnectionRefusedError:
                    pass  # Handle the case where the peer isn't available
        time.sleep(10)  # Send status every 10 seconds

def receive_status():
    global MY_ADDRESS

    current_function_name = inspect.currentframe().f_globals["__name__"] + "." + inspect.currentframe().f_code.co_name
    logging.info(f"Started executing: {current_function_name}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(MY_ADDRESS)
        s.listen(10)
        logging.info(f"{current_function_name} - Waiting for receive connections")

        while True:
            conn, addr = s.accept()
            with conn:
                status = conn.recv(1024).decode()
                print(f"{current_function_name} - Received status from {addr}: {status}")

if __name__ == "__main__":
    threading.Thread(target=send_status).start()
    threading.Thread(target=receive_status).start()
