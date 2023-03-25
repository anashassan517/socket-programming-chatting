import tkinter as tk #gui library
import socket
import threading
import queue

def start_server():
    global server_socket, client_socket
    
    # Get the port number from the text box
    port_number = int(port_textbox.get())
    
    # Create a socket and bind it to the port number
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port_number))
    server_socket.listen(1)
    print("Server started")
    
    # Accept a client connection
    client_socket, address = server_socket.accept()
    print("Connected to client at", address)
    
    # Start the receive and send threads
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    send_thread = threading.Thread(target=send)
    send_thread.start()

def receive():
    # Receive data from the client and output it to the output textbox
    while True:
        data = client_socket.recv(1024).decode("utf-8")
        if not data:
            break
        input_textbox.configure(state=tk.NORMAL)
        input_textbox.delete("1.0", tk.END)
        input_textbox.insert(tk.END, data)
        input_textbox.configure(state=tk.DISABLED)

def send():
    # Send data entered in the output textbox to the client
    while True:
        data = output_queue.get()
        if data == "quit":
            client_socket.send(data.encode("utf-8"))
            client_socket.close()
            server_socket.close()
            print("Disconnected to the Client")
            break
        client_socket.send(data.encode("utf-8"))

def send_message():
    # Get the text from the output textbox and add it to the output queue
    data = output_textbox.get("1.0", "end-1c")
    output_queue.put(data)
    
    # Clear the output textbox
    output_textbox.delete("1.0", tk.END)

root = tk.Tk()

root.title('Instant LAN Messenger Server')

root.geometry('650x400')
# Create the "Enter Port" label
enter_label = tk.Label(root, text="Enter Port:")

# Create the port number label and text box
port_label = tk.Label(root, text="Port Number:")
port_textbox = tk.Entry(root)

# Create the input label and text box
input_label = tk.Label(root, text="Input")
input_textbox = tk.Text(root, height=6.5, width=60)

# Create the output label and text box
output_label = tk.Label(root, text="Output")
output_textbox = tk.Text(root, height=6.5, width=60)

# Create the start button
start_button = tk.Button(root, text="Start Listening", command=start_server)

# Create the send button
send_button = tk.Button(root, text="Send", command=send_message)

# Place the labels and text boxes in the window
enter_label.grid(row=0, column=0, columnspan=2)
port_label.grid(row=1, column=0)
port_textbox.grid(row=1, column=1)
input_label.grid(row=2, column=0, pady=10)
input_textbox.grid(row=2, column=1, pady=10)
output_label.grid(row=3, column=0, pady=10)
output_textbox.grid(row=3, column=1, pady=10)

# Place the start and send buttons in the last row
start_button.grid(row=5, column=0, pady=10)
send_button.grid(row=5, column=1, pady=10)

# Create a socket object and set it to None
server_socket = None
client_socket = None

# Create a queue to hold output messages
output_queue = queue.Queue()

root.mainloop()
