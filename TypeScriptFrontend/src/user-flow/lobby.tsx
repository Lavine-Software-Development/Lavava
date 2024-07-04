import React, { useEffect, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { NetworkContext } from "../game/NetworkContext";
import { abilityCountsConversion } from "../game/objects/utilities";
const updateCallback = () => {
    console.log("Update received");
};

const Lobby: React.FC = () => {
    const [boardData, setBoardData] = useState(null);
    const [gameID, setGameID] = useState("");
    const [gameType, setGameType] = useState("");
    const navigate = useNavigate();
    const network = useContext(NetworkContext);

    const gameCode = (code: string) => {
        setGameID(code);
        sessionStorage.setItem("key_code", code);
    };

    useEffect(() => {
        const storedAbilities = sessionStorage.getItem("selectedAbilities");
        setGameID(sessionStorage.getItem("key_code") || "");
        setGameType(sessionStorage.getItem("type") || "");
        const abilitiesFromStorage = storedAbilities
            ? JSON.parse(storedAbilities)
            : [];

        // Create a map from ability code to count using the NameToCode mapping
        const abilityCounts = abilityCountsConversion(abilitiesFromStorage);
        // const network = new Network(serverURL, updateCallback);
        console.log("Got network from context");
        // const network = new Network(serverURL, updateCallback);
        // network?.connectWebSocket();
        if (network) {
            network.gameIDCallback = gameCode;
            console.log("bind happened?");
        }

        network?.connectWebSocket();
        network?.setupUser(abilityCounts);
        // Wait for the board data
        network?.getBoardData().then((data) => {
            console.log("Board data received in component:", data);
            navigate("/play", { state: { boardData: data } });
            // setBoardData(data);
        });

        // Cleanup function to close the WebSocket when the component unmounts
        //return () => {

        //};
    }, []);

    if (!boardData) {
        return (
            <div>
                <h1>Waiting...</h1>
                {gameType != "LADDER" && <h2>Game Code: {gameID}</h2>}
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

