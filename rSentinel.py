import socket
import threading
import time
import logging
import inspect
import constants
import argparse

logging.basicConfig(level=logging.INFO)

FAULT_STATUS_ARRAY = None

def send_status(status_message, node_name, peer_addresses, my_address):
    current_function_name = inspect.currentframe().f_globals["__name__"] + "." + inspect.currentframe().f_code.co_name
    logging.info(f"Started executing: {current_function_name}")

    while True:
        for address in peer_addresses:
            if address[0] != my_address[0]:
                logging.info(f"{current_function_name} - Attempting to send status to: {address}")
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.connect(address)
                        send_msg = status_message + " - " + node_name
                        sock.sendall(send_msg.encode())
                except Exception as e:
                    logging.error(f"{current_function_name} - Error sending status to: {address} - {e}")
        time.sleep(10)  # Send status every 10 seconds

def receive_status(my_address):
    current_function_name = inspect.currentframe().f_globals["__name__"] + "." + inspect.currentframe().f_code.co_name
    logging.info(f"Started executing: {current_function_name}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', my_address[1]))
        s.listen(10)
        logging.info(f"{current_function_name} - Waiting for receive connections at - {my_address}")

        while True:
            conn, addr = s.accept()
            with conn:
                receipt_data = conn.recv(1024).decode()
                print(f"{current_function_name} - Received status from {addr}: {receipt_data}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Your script description here.")
    parser.add_argument('-nn', '--node_num', type=str, help='Provide the node number starting with index 0')
    parser.add_argument('-p', '--port', type=str, help='Port number on which to run the service')
    parser.add_argument('-fs', '--fault_status', type=str, help='Fault status for current node for testing purposes')
    args = parser.parse_args()

    # PEER_IPS = [(ip, CONSTANTS["PORT"]) for ip in CONSTANTS["PEER_IPS"]]
    peer_addresses = [(entry["host"], entry["port"]) for entry in constants.PEER_ADDRESSES]
    logging.info(f"Peer IP addresses: {peer_addresses}")

    my_ip = socket.gethostbyname(socket.gethostname())
    my_address = (my_ip, int(args.port))
    logging.info(f"My IP address: {my_address}")
    status_message = "Alive and well"  # The status message you want to send

    threading.Thread(target=receive_status, kwargs={'my_address': my_address}).start()
    threading.Thread(target=send_status,kwargs={'status_message': status_message, 'node_name': args.node_num, 'peer_addresses': peer_addresses, 'my_address': my_address}).start()
