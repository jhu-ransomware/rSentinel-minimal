import inspect
import logging
import socket
import constants

def init_client_to_server(ip_address):
    current_function_name = inspect.currentframe().f_globals["__name__"] + "." + inspect.currentframe().f_code.co_name
    logging.info(f"Currently executing: {current_function_name}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(constants.SOCKET_TIMEOUT_GLOBAL)

    try:
        sock.connect((ip_address, constants.PORT))
        return sock
    except socket.error as err:
        print("Socket creation/connection error:", err)
        return None