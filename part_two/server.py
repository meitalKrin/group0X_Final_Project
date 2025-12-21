import socket
import threading

HOST =  "0.0.0.0"
PORT = 5000

clients = set()
clients_lock = threading.Lock()

def handle_client(conn: socket.socket, addr):
    print(f"[+] Connected: {addr}")
    with conn:
        try:
            while True:
                data = conn.recv(4096)  # blocking read
                if not data:
                    break  # client disconnected

                msg = data.decode("utf-8", errors="replace").strip()
                print(f"[{addr}] {msg}")

                # Echo back (for testing)
                conn.sendall(f"Server got: {msg}\n".encode("utf-8"))
        except ConnectionError:
            pass
        finally:
            with clients_lock:
                clients.discard(conn)
            print(f"[-] Disconnected: {addr}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(10)
        print(f"Server listening on {HOST}:{PORT}")
        
        while True:
            conn, addr = server.accept()
            with clients_lock:
                clients.add(conn)
                print(f"Connected by {addr}")
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
            
if __name__ == "__main__":
    main()