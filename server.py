# server/server.py

import os
import socket
import ssl
import threading
from server.config_loader import load_config
from server.logger import setup_logger
from server.connection_handler_clean import handle_client
from server.file_search import search_with_grep

logger = setup_logger()

def start_server(stop_event=None):
    print(">>> [DEBUG] start_server() called")  # Debug print

    config_path = os.getenv("TEST_CONFIG_PATH", "config.json")
    print(f">>> [DEBUG] Using config file: {config_path}")

    config = load_config(config_path)
    host = config.get("host", "127.0.0.1")
    port = config.get("port", 12345)
    use_ssl = config.get("SSL_ENABLED", False)
    file_path = config.get("file_path", "data.txt")
    max_payload = config.get("MAX_PAYLOAD", 1024)

    print(f">>> [DEBUG] Server starting on {host}:{port}, SSL={use_ssl}, file={file_path}, max_payload={max_payload}")

    if not os.path.exists(file_path):
        print(f"!!! [ERROR] file_path does not exist: {file_path}")
        return

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_sock.bind((host, port))
        server_sock.listen(5)
        logger.info("Server listening...")

        if use_ssl:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
            server_sock = context.wrap_socket(server_sock, server_side=True)

        while not (stop_event and stop_event.is_set()):
            try:
                server_sock.settimeout(1.0)
                conn, addr = server_sock.accept()
                thread = threading.Thread(
                    target=handle_client,
                    args=(conn, addr, lambda query: search_with_grep(file_path, query)),
                    kwargs={"max_payload": max_payload},  # 👈 pass max_payload!
                    daemon=True
                )
                thread.start()
            except socket.timeout:
                continue
            except Exception as e:
                logger.error(f"Server error: {e}")
                break
    finally:
        logger.info("Shutting down server...")
        server_sock.close()


if __name__ == "__main__":
    print(">>> [DEBUG] __main__ block executing")
    start_server()
