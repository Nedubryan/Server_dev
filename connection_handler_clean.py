import socket
import ssl
import time
import traceback
from server.logger import setup_logger

logger = setup_logger()

def handle_client(conn, addr, search_func, max_payload=1024):
    """Handle client connection: validate input, search, and safely return response."""
    logger.info(f"Connection from {addr}")
    response = b""

    try:
        data = b""
        while True:
            chunk = conn.recv(1024)
            logger.debug(f"Received chunk: {chunk!r}")
            if not chunk:
                break
            data += chunk
            if b"\x00" in chunk:
                break

        logger.debug(f"Full received data: {data!r}")

        if not data:
            logger.warning("No data received.")
            response = b"ERROR: No data received\n"

        elif len(data) > max_payload:
            logger.warning(f"Payload too large: {len(data)} bytes (max {max_payload})")
            response = b"PAYLOAD TOO LARGE\n"
            try:
                conn.sendall(response)
                logger.info("Sent early PAYLOAD TOO LARGE response")
                time.sleep(0.1)
            except Exception as e:
                logger.warning(f"Early send failed: {e}")
            finally:
                try:
                    conn.shutdown(socket.SHUT_RDWR)
                except Exception:
                    pass
                try:
                    conn.close()
                except Exception:
                    pass
                logger.info(f"Connection to {addr} closed after oversized payload.")
            return  # exit early to avoid duplicate send/cleanup

        else:
            try:
                query = data.strip(b"\x00").decode("utf-8").strip()
                logger.debug(f"Decoded query: '{query}'")
            except UnicodeDecodeError:
                logger.warning("Invalid UTF-8 input.")
                response = b"ERROR: Invalid UTF-8\n"
            else:
                if not query:
                    logger.warning("Empty query after stripping.")
                    response = b"ERROR: Empty query\n"
                else:
                    logger.info(f"Received query: '{query}'")
                    try:
                        result = search_func(query)
                        logger.info(f"Search result: {result}")
                        response = b"STRING EXISTS\n" if result else b"STRING NOT FOUND\n"
                    except Exception as e:
                        logger.error(f"Search function error: {e}")
                        logger.debug(traceback.format_exc())
                        response = b"STRING NOT FOUND\n"

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.debug(traceback.format_exc())
        response = b"ERROR: Internal server error\n"

    try:
        if not response:
            logger.warning("No response generated. Sending fallback error.")
            response = b"ERROR: Empty response generated\n"

        logger.info(f"Sending response: {response.strip()}")
        conn.sendall(response)
        time.sleep(0.3)  # allow OS to flush buffer
    except Exception as e:
        logger.warning(f"Failed to send response: {e}")

    finally:
        try:
            conn.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass
        logger.info(f"Connection to {addr} closed.")
