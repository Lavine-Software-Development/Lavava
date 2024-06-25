from flask import Flask, request, jsonify
import threading
from websocket_server import WebSocketServer
import asyncio
app = Flask(__name__)

# Port management
next_port = 5101  # Starting port for game servers
max_port = 5120   # Maximum port, assuming 20 games maximum
active_ports = set()

def find_available_port():
    global next_port
    for port in range(next_port, max_port + 1):
        if port not in active_ports:
            active_ports.add(port)
            return port
    return None  # No ports available

def launch_game_server(port):
    # Create and set a new event loop for the thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    server = WebSocketServer(port)
    server.run()

@app.route('/start_game', methods=['POST'])
def start_game():
    port = find_available_port()
    if port is None:
        return jsonify({'error': 'No available ports'}), 503  # Service Unavailable
        
    # Start the server in a new thread
    thread = threading.Thread(target=launch_game_server, args=(port,))
    thread.daemon = True
    thread.start()

    return jsonify({'message': 'Game server starting', 'port': port})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
