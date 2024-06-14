import React from "react";
import { Network } from "../game/objects/network";
const Lobby: React.FC = () => {
    return (
        <div>
            <h1>Waiting...</h1>
            {/* Add your waiting symbol here */}
        </div>
    );
};
function getBoard() {
    const network = new Network("ws://localhost:5553", () => null);
    network.connectWebSocket();
}

export default Lobby;

