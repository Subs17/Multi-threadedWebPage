import socket
import threading
import os

# Define the server's IP and Port
HOST = '127.0.0.1' # Localhost number
PORT = 8080        # Port to listen for

# Function for handling client requests
def handle_client(connection, address):
    print(f"Connected to {address}")

    try:
        # Receive the request from the client (browser)
        request = connection.recv(1024).decode('utf-8')
        print(f"Request received:\n{request}")

        # Parse the request to extract the requested file
        headers = request.split('\n')
        if len(headers)>0: 
            first-line = headers[0].split()
            if len(first_line) > 1:
                file_requested = first_line[1]

                if file_requested == '/':
                    file_requested = '/index.html'

                try:
                    filepath = '.' + file_requested
                    with open(filepath, 'rb') as f:
                        response_content = f.read()
                    
                    # Create HTTP response headers
                    response_headers = "HTTP/1.1 200 OK\n"
                    response_headers += f"Content-Length: {len(response_content)}\n"
                    response_headers += "Content-Type: text/html\n\n"

                    # Send headers followed by Content
                    connection.sendall(response_headers.encode('utf-8'))
                    connection.sendall(response_content)
                
                except FileNotFoundError:
                    # If file is not found, throw a 404 response
                    response_headers = "HTTP/1.1 404 Not Found\n\n"
                    response_content = "<html><body><h1>404 Page Not Found</h1></body></html>"
                    connection.sendall(response_headers.encode('utf-8'))
                    connection.sendall(response_content.encode('utf-8'))

    except Exception as e: 
        print(f"Error handling the request: {e}")
    
    finally:
        # Close the connection once the response has been sent
        connection.close()

def start_server():
    # Create the server socket (IPv4, TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the specified host and Port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections (up to 5 simultaneous)
    server.socket.listen(5)
    print(f"Server started at {HOST}:{PORT}")

    while True:
        # Accept an incoming connection
        connection, address = server_socket.accept()

        # Create a new thread to handle each client request
        client_thread = threading.Thread(target=handle_client, args=(connection, address))
        client_thread.start()

if __name__ == "__main__":
    start_server()