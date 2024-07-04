import { NameToCode } from "./constants";

export class Network {
    public socket: WebSocket | null = null;
    serverURL: string;
    updateCallback: (board_data: any) => void;
    gameIDCallback: (game_id: string) => void;
    messageQueue: string[] = [];
    private boardDataPromise: Promise<any> | null = null;
    private boardDataResolver: ((data: any) => void) | null = null;
    private reconnectInterval: number;
    private reconnectAttempts: number;

    constructor(
        serverURL: string,
        updateCallback: (board_data: any) => void,
        reconnectInterval: number = 5000,
        reconnectAttempts: number = Infinity
    ) {
        this.serverURL = serverURL;
        this.updateCallback = updateCallback;
        this.reconnectInterval = reconnectInterval;
        this.reconnectAttempts = reconnectAttempts;

        // Initialize the board data promise
        this.boardDataPromise = new Promise((resolve) => {
            this.boardDataResolver = resolve;
        });
    }

    connectWebSocket(attempts = 0): void {
        if (attempts >= this.reconnectAttempts) {
            console.error("Max reconnect attempts reached");
            return;
        }

        console.log("Trying to connect to WebSocket...");
        this.socket = new WebSocket(this.serverURL);

        this.socket.onopen = () => {
            console.log("WebSocket Connected");
            this.messageQueue.forEach((msg) => this.sendMessage(msg)); // Send all queued messages
            this.messageQueue = []; // Clear the queue
        };

        this.socket.onmessage = (event) => {
            let data = JSON.parse(event.data);
            if (data.hasOwnProperty("game_id")) {
                this.gameIDCallback(data.game_id);
                console.log("Game ID received: ", data.game_id);
            } else {
                if (data.isFirst === true) {
                    if (this.boardDataResolver) {
                        this.boardDataResolver(data);
                        this.boardDataResolver = null; // Ensure the resolver is called only once
                    }
                } else {
                    this.updateCallback(data);
                }
            }
        };

        this.socket.onclose = () => {
            console.log("WebSocket Disconnected. Attempting to reconnect...");
            setTimeout(() => {
                this.connectWebSocket(attempts + 1);
            }, this.reconnectInterval);
        };

        this.socket.onerror = (error) => {
            console.error("WebSocket Error:", error);
            this.socket!.close(); // Close the socket to trigger the onclose event
        };
    }

    disconnectWebSocket(): void {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }

        // Reset the board data promise
        this.boardDataPromise = new Promise((resolve) => {
            this.boardDataResolver = resolve;
        });

        // Clear the message queue
        this.messageQueue = [];
    }

    sendMessage(message: string): void {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            console.log("Sending message: ", message);
            console.log("Socket: ", this.socket);
            const result = this.socket.send(message);
            console.log("Result: ", result);
        } else if (
            this.socket &&
            this.socket.readyState === WebSocket.CONNECTING
        ) {
            console.log("Queuing message due to WebSocket connecting");
            this.messageQueue.push(message);
        } else {
            console.error("WebSocket is not connected or has failed.");
        }
    }

    setupUser(abilities: { [x: string]: any }) {
        console.log("setup called");
        const code = sessionStorage.getItem("key_code");
        const type = sessionStorage.getItem("type");
        const playerCount = Number(sessionStorage.getItem("player_count")) || 0;

        const send_dict = {
            type: type,
            players: playerCount,
            code: code,
            mode: "default",
            abilities: abilities,
        };
        console.log("Trying to set up user with: ", send_dict);
        this.sendMessage(JSON.stringify(send_dict));
    }

    // Method to get the board data promise
    getBoardData(): Promise<any> {
        return this.boardDataPromise!;
    }

    test() {
        return "Test called";
    }
}

