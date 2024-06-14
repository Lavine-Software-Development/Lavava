import { NameToCode } from "./constants";

export class Network {
    private socket: WebSocket | null = null;
    serverURL: string;
    updateCallback: (board_data) => void;
    messageQueue: string[] = [];

    constructor(serverURL: string, updateCallback: () => void) {
        this.serverURL = serverURL;
        this.updateCallback = updateCallback;
    }

    connectWebSocket(): void {
        console.log("Trying to connect to WebSocket...");
        this.socket = new WebSocket(this.serverURL);

        this.socket.onopen = () => {
            console.log("WebSocket Connected");
            this.messageQueue.forEach((msg) => this.sendMessage(msg)); // Send all queued messages
            this.messageQueue = []; // Clear the queue
        };

        this.socket.onmessage = (event) => {
            console.log("Received message: ", event.data);
            // this.updateCallback(event.data);
        };

        this.socket.onclose = () => {
            console.log("WebSocket Disconnected");
        };

        this.socket.onerror = (error) => {
            console.error("WebSocket Error:", error);
        };
    }

    sendMessage(message: string): void {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            console.log("Sending message: ", message);
            this.socket.send(message);
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
        const storedAbilities = sessionStorage.getItem("selectedAbilities");
        const abilitiesFromStorage = storedAbilities
            ? JSON.parse(storedAbilities)
            : [];
        const transformedAbilities = abilitiesFromStorage.reduce(
            (
                acc: { [x: string]: any },
                ability: { name: string; count: number }
            ) => {
                const code = NameToCode[ability.name];
                console.log("code is: ", code);
                if (code) {
                    acc[code] = ability.count;
                }
                console.log("acc is: ", acc);
                return acc;
            }
        );
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
        console.log("Trying to setp user with: ", send_dict);
        this.sendMessage(JSON.stringify(send_dict));
    }
}

