import React, { useEffect, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { NetworkContext } from "../game/NetworkContext";
import { abilityCountsConversion } from "../game/objects/utilities";

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

        const abilityCounts = abilityCountsConversion(abilitiesFromStorage);
        if (network) {
            network.gameIDEtcCallback = lobbyData;
        }
        
        network?.connectWebSocket();
        network?.setupUser(abilityCounts)
        network?.getBoardData().then((data) => {
            navigate("/play", { state: { boardData: data } });
        });

        // Handle back button
        const handleBackButton = (event: PopStateEvent) => {
            event.preventDefault();
            handleCancel();
        };

        // Push a new state to the history when entering the lobby
        history.pushState({ page: "lobby" }, "Lobby Page");

        // Add event listener for the popstate event
        window.addEventListener('popstate', handleBackButton);

        // Cleanup function
        return () => {
            window.removeEventListener('popstate', handleBackButton);
        };
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
            <pre>{JSON.stringify(boardData, null, 2)}</pre>
        </div>
    );
};

export default Lobby;