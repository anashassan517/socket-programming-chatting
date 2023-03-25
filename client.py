import tkinter as tk #gui library
import socket
import threading
import queue

def connect():
    global client_socket
    
    # Get the IP address and port number from the text boxes
    ip_address = ip_textbox.get()
    port_number = int(port_textbox.get())
    
    # Create a socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_address, port_number))
    print("Connected to server")
    
    # Start the receive and send threads
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    send_thread = threading.Thread(target=send)
    send_thread.start()

def receive():
    # Receive data from the server and output it to the output textbox
    while True:
        data = client_socket.recv(1024).decode("utf-8")
        if not data:
            break
        input_textbox.configure(state=tk.NORMAL)
        input_textbox.delete("1.0", tk.END)
        input_textbox.insert(tk.END, data)
        input_textbox.configure(state=tk.DISABLED)

def send():
    # Send data entered in the output textbox to the server
    while True:
        data = output_queue.get()
        if data == "QUIT":
            client_socket.send(data.encode("utf-8"))
            client_socket.close()
            print("Disconnected to the Server")
            break
        client_socket.send(data.encode("utf-8"))

def send_message():
    # Get the text from the output textbox and add it to the output queue
    data = output_textbox.get("1.0", "end-1c")
    output_queue.put(data)
    
    # Clear the output textbox
    output_textbox.delete("1.0", tk.END)


def close():
    client_socket.close()
    print("Disconnected from the Server")
    root.destroy()
    

    
 

root = tk.Tk()

root.title('Instant LAN Messenger Client')

root.geometry('690x450')

# Create the "Enter IP and Port" label
enter_label = tk.Label(root, text="Enter IP and Port:")

# Create the IP address label and text box
ip_label = tk.Label(root, text="IP Address:")
ip_textbox = tk.Entry(root)

# Create the port number label and text box
port_label = tk.Label(root, text="Port Number:")
port_textbox = tk.Entry(root)

# Create the input label and text box
input_label = tk.Label(root, text="Input")
input_textbox = tk.Text(root, height=6.5, width=60)

# Create the output label and text box
output_label = tk.Label(root, text="Output")
output_textbox = tk.Text(root, height=6.5, width=60)

# Create the connect button
connect_button = tk.Button(root, text="Connect", command=connect)

# Create the send button
send_button = tk.Button(root, text="Send", command=send_message)


button = tk.Button(root, text = 'Terminate session', command = close)
button.grid(row=5, column=2)

# Place the labels and text boxes in the window
enter_label.grid(row=0, column=0, columnspan=2)
ip_label.grid(row=1, column=0)
ip_textbox.grid(row=1, column=1)
port_label.grid(row=2, column=0)
port_textbox.grid(row=2, column=1)
input_label.grid(row=3, column=0, pady=10)
input_textbox.grid(row=3, column=1, pady=10)
output_label.grid(row=4, column=0, pady=10)
output_textbox.grid(row=4, column=1, pady=10)

# Place the connect and send buttons in the last row
connect_button.grid(row=2, column=2)
send_button.grid(row=5, column=1,padx=10,pady=10)

# Create a socket object and set it to None
client_socket = None

# Create a queue to hold output messages
output_queue = queue.Queue()

root.mainloop()
