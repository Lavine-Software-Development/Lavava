import React, { useState, useEffect } from "react";
import { Network } from "./game/slav/network";
const WebSocketTest: React.FC = () => {
    const [ws, setWs] = useState<WebSocket | null>(null);
    const [messages, setMessages] = useState<string[]>([]);
    const [inputMessage, setInputMessage] = useState("");
    const [connectionStatus, setConnectionStatus] = useState("Disconnected"); // State to track connection status

    // URL of your WebSocket server
    const serverUrl = "ws://localhost:5553";

    useEffect(() => {
        // Clean up on unmount
        return () => {
            if (ws) {
                ws.close();
                setConnectionStatus("Disconnected");
            }
        };
    }, [ws]);

    const connectWebSocket = () => {
        console.log("Trying to connect to WebSocket...");
        setConnectionStatus("Connecting..."); // Update status on trying to connect
        const socket = new WebSocket(serverUrl);
        socket.onopen = () => {
            console.log("WebSocket Connected");
            setConnectionStatus("Connected"); // Update status on successful connection
        };
        socket.onmessage = (event) => {
            setMessages((prevMessages) => [...prevMessages, event.data]);
            //call update callback here
        };
        socket.onclose = () => {
            console.log("WebSocket Disconnected");
            setConnectionStatus("Disconnected"); // Update status on disconnection
        };
        socket.onerror = (error) => {
            console.error("WebSocket Error:", error);
            setConnectionStatus("Error"); // Update status on error
        };
        setWs(socket);
    };

    const sendMessage = () => {
        if (ws) {
            ws.send(inputMessage);
            setInputMessage("");
        }
    };

    return (
        <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
            <div>Status: {connectionStatus}</div>{" "}
            {/* Display connection status */}
            <button
                onClick={connectWebSocket}
                style={{
                    padding: "10px 20px",
                    marginRight: "10px",
                    fontSize: "16px",
                    cursor: "pointer",
                }}
            >
                Connect to WebSocket
            </button>
            <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Write a message"
                style={{
                    padding: "10px",
                    marginRight: "10px",
                    width: "300px",
                    fontSize: "16px",
                }}
            />
            <button
                onClick={sendMessage}
                style={{
                    padding: "10px 20px",
                    fontSize: "16px",
                    cursor: "pointer",
                }}
            >
                Send Message
            </button>
            <div
                style={{
                    marginTop: "20px",
                    border: "1px solid #ccc",
                    height: "150px",
                    overflowY: "scroll",
                    padding: "10px",
                    backgroundColor: "#f9f9f9",
                }}
            >
                <h3 style={{ color: "#333" }}>Received Messages:</h3>
                {messages.map((msg, index) => (
                    <p
                        key={index}
                        style={{
                            margin: "5px 0",
                            padding: "5px",
                            borderBottom: "1px solid #eee",
                            color: "#333",
                        }}
                    >
                        {msg}
                    </p>
                ))}
            </div>
        </div>
    );
};

export default WebSocketTest;

