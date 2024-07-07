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
    const [gameID, setGameID] = useState("");
    const [playerCount, setPlayerCount] = useState(0);
    const [gameType, setGameType] = useState("");
    const navigate = useNavigate();
    const network = useContext(NetworkContext);

    const lobbyData = (code: string, count: number) => {
        if (code === "INVALID") {
            network?.disconnectWebSocket();
            navigate("/home");
        }
        setGameID(code);
        setPlayerCount(count);
        sessionStorage.setItem("key_code", code);
    }

    const handleCancel = () => {
        network?.sendMessage({ action: "cancel_match"});
        network?.disconnectWebSocket();
        navigate("/home");
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
        console.log("Got network from context");
        if (network) {
            network.gameIDEtcCallback = lobbyData;
            console.log("bind happened?");
        }
        
        network?.connectWebSocket();
        network?.setupUser(abilityCounts)
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
            {gameID && 
                <button 
                    style={{
                        position: 'absolute',
                        top: '10px',
                        left: '10px',
                        padding: '10px 20px',
                        fontSize: '16px',
                        cursor: 'pointer'
                    }}
                    onClick={handleCancel}
                >
                    Cancel
                </button>
            }
                <h1>Waiting...</h1>
                { gameType != "LADDER" ? ( 
                    <div>
                        <h2>Game Code: { gameID }</h2>
                        <h2>{ playerCount } Player Friendly Match</h2>
                    </div> 
                ) : (
                    <h2>{ playerCount } Player Ladder Match</h2>
                )
                }
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

