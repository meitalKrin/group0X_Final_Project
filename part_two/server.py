import socket
import threading

HOST =  "0.0.0.0"
PORT = 5000

clients = {}
clients_lock = threading.Lock()

def handle_client(conn: socket.socket, addr):
    print(f"[+] Connected: {addr}")
    username = ""
    with conn:
        try:
            while True:
                data = conn.recv(4096)  # blocking read
                if not data:
                    break  # client disconnected
        
                msg = data.decode("utf-8", errors="replace").strip() # Decoding the data
                command = msg.split(" ", 1) # Getting the specific command used
                print(f"[{addr}] {msg}")

                if(command[0].lower() == "hello"): # Registering to the client list and keeping username
        
                    with clients_lock: # Locking client threads to avoid mismatch and errors mid register.
                        clients[command[1]] = conn #Saving connection under username
                        username = command[1] # Saving username for future message use
                
                elif(command[0].lower() == "msg"): #Sending a message to a specific user
                
                    toSend = command[1].split(" ", 1) # Extracting username and message to pass
                    receiver, msg_to_send = clients.get(toSend[0]), f"{username}: {toSend[1]}".encode("utf-8") # Getting conn via username and reformatting message to also hold sender name
                
                    try:
                        if(receiver):
                            receiver.send(msg_to_send)
                
                        else: # If no such user exists
                            conn.send(b"User Not Found")
                
                    except Exception as e: # for any unexpected errors
                        print(e)
                        conn.send(b"There was an error while attempting to send message")
                else:
                    conn.send(b"Unrecognized Command")
        except ConnectionError: # For sudden connection issues and disconnects
            pass
            print(f"[-] Disconnected: {addr}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server: # setting the server up
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Options for hte socket
        server.bind((HOST, PORT)) # Binding To 0.0.0.0 and port of our choice
        server.listen(10) 
        
        print(f"Server listening on {HOST}:{PORT}")
        
        while True: # Main server loop
            conn, addr = server.accept() # Receiving clients 
            print(f"Connected by {addr}") # Announcing Connection
        
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True) # Creating a new listening thread for the connected client
            t.start() # starting the thread
            
if __name__ == "__main__":
    main()