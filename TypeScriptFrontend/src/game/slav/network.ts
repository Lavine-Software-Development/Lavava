import { NameToCode } from "./constants";

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

    setupUser() {
        const storedAbilities = sessionStorage.getItem('selectedAbilities');
        const abilitiesFromStorage = storedAbilities ? JSON.parse(storedAbilities) : [];
        abilitiesFromStorage.reduce((acc: { [x: string]: any; }, ability: { name: string ; count: number; }) => {
            const code = NameToCode[ability.name];
            if (code) {
                acc[code] = ability.count;
            }
            return acc;
        }, {});

        const code = sessionStorage.getItem('key_code');
        const type = sessionStorage.getItem('type');
        const playerCount = Number(sessionStorage.getItem('player_count')) || 0;

        const send_dict = {"type": type, "players": playerCount, "code": code, "abilities": abilitiesFromStorage};
    }
}

