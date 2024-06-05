export class Network {
    private socket: WebSocket | null = null;
    serverURL: string;
    //add update callback function
    constructor(serverURL: string) {
        this.serverURL = serverURL;
    }

    // A method that doesn't perform any meaningful operation
    pointless(value: any): void {
        console.log("This is a pointless function", value);
    }

    // Method to connect to the WebSocket server
    connectWebSocket(): void {
        console.log("Trying to connect to WebSocket...");
        this.socket = new WebSocket(this.serverURL);

        this.socket.onopen = () => {
            console.log("WebSocket Connected");
            this.sendMessage("Hello from the client!"); //send player join/host data
        };

        this.socket.onmessage = (event) => {
            console.log("Received message: ", event.data);
        };

        this.socket.onclose = () => {
            console.log("WebSocket Disconnected");
        };

        this.socket.onerror = (error) => {
            console.error("WebSocket Error:", error);
        };
    }

    // Method to send a message through the WebSocket
    sendMessage(message: string): void {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            console.log("Sending message: ", message);
            this.socket.send(message);
        } else {
            console.error("WebSocket is not connected.");
        }
    }

    setupUser(initData) {}
}

