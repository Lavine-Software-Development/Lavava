import React, { useEffect, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { NetworkContext } from "../game/NetworkContext";
import { abilityCountsConversion } from "../game/objects/utilities";
const serverURL = "ws://localhost:5553";
const updateCallback = () => {
    console.log("Update received");
};

const Lobby: React.FC = () => {
    const [boardData, setBoardData] = useState(null);
    const navigate = useNavigate();
    const network = useContext(NetworkContext);
    useEffect(() => {
        const storedAbilities = sessionStorage.getItem("selectedAbilities");
        const abilitiesFromStorage = storedAbilities
            ? JSON.parse(storedAbilities)
            : [];

        // Create a map from ability code to count using the NameToCode mapping
        const abilityCounts = abilityCountsConversion(abilitiesFromStorage);
        // const network = new Network(serverURL, updateCallback);
        console.log("Got network from context");
        // const network = new Network(serverURL, updateCallback);
        // network?.connectWebSocket();
        network?.setupUser(abilityCounts);
        // Wait for the board data
        network?.getBoardData().then((data) => {
            console.log("Board data received in component:", data);
            navigate("/play", { state: { boardData: data } });
            // setBoardData(data);
        });

        // Cleanup function to close the WebSocket when the component unmounts
        // return () => {
        //     if (network?.socket) {
        //         network?.socket.close();
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

