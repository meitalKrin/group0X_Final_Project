import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            print("\n" + data.decode("utf-8").strip())
        except:
            break

def main():
    username = input("Choose username: ")

    with socket.create_connection((HOST, PORT)) as sock:
        sock.sendall(f"HELLO {username}\n".encode("utf-8"))

        threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

        print("Commands:")
        print("  CHAT <username>")
        print("  MSG <message>")
        print("  QUIT")

        while True:
            msg = input("> ")
            if not msg:
                continue

            sock.sendall((msg + "\n").encode("utf-8"))

            if msg.upper() == "QUIT":
                break

if __name__ == "__main__":
    main()