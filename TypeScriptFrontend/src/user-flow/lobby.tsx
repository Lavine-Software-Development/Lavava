import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { Network } from "../game/objects/network";
import { NameToCode } from "../game/objects/constants";
const serverURL = "ws://localhost:5553";
const updateCallback = () => {
    console.log("Update received");
};

const Lobby: React.FC = () => {
    const [boardData, setBoardData] = useState(null);
    const navigate = useNavigate();
    useEffect(() => {
        const storedAbilities = sessionStorage.getItem("selectedAbilities");
        const gameType = String(sessionStorage.getItem("type"));
        const playerCount = Number(sessionStorage.getItem("player_count")) || 0;
        const abilitiesFromStorage = storedAbilities
            ? JSON.parse(storedAbilities)
            : [];

        // Create a map from ability code to count using the NameToCode mapping
        const abilityCounts = abilitiesFromStorage.reduce(
            (
                acc: { [x: string]: any },
                ability: { name: string; count: number }
            ) => {
                const code = NameToCode[ability.name];
                if (code) {
                    acc[code] = ability.count;
                }
                return acc;
            },
            {}
        );
        const network = new Network(serverURL, updateCallback);
        network.connectWebSocket();
        network.setupUser(abilityCounts);
        // Wait for the board data
        network.getBoardData().then((data) => {
            console.log("Board data received in component:", data);
            navigate("/play", { state: { boardData: data } });
            // setBoardData(data);
        });

        // Cleanup function to close the WebSocket when the component unmounts
        // return () => {
        //     if (network.socket) {
        //         network.socket.close();
        //     }
        // };
    }, []);

    if (!boardData) {
        return (
            <div>
                <h1>Waiting...</h1>
                {/* Add your waiting symbol here */}
            </div>
        );
    }

    return (
        <div>
            <h1>Board Data Received</h1>
            {/* Render the board data here */}
            <pre>{JSON.stringify(boardData, null, 2)}</pre>
        </div>
    );
};

export default Lobby;

