import socket
import threading

HOST = "127.0.0.1" # Localhost
PORT = 5000 # Server Port

def receive_messages(sock):
    while True: # Message Receiving loop
        try:
            data = sock.recv(4096) #breaking down the data
            print("\n" + data.decode("utf-8").strip()) # Printing it onto console
        except:
            break

async def main ():
    username = input("Choose username: ") 

    with socket.create_connection((HOST, PORT)) as sock: #creating a new connection
        threading.Thread(target=receive_messages, args=(sock,), daemon=True).start() # Setting the thread for receiving messages

        await sock.sendall(f"Hello {username}\n".encode("utf-8")) # sending register command

        print("Commands:")
        print("  MSG <message>")
        print("  QUIT")

        while True: # Main input loop
            msg = input("> ") #receiving commands
            if not msg: # If message is empty, just move on
                continue

            sock.sendall((msg + "\n").encode("utf-8")) # Sending the command received to the server

            if msg.upper() == "QUIT": # breaking the loop and killing the client
                break

if __name__ == "__main__":
    main()