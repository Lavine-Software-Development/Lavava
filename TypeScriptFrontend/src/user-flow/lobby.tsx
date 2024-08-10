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
    const [first, setFirst] = useState(true);
    const [gameMode, setGameMode] = useState("");
    const [botRequested, setBotRequested] = useState(false);

    const lobbyData = (code: string, count: number, mode: string) => {
        if (code === "INVALID") {
            network?.disconnectWebSocket();
            navigate("/home?invalidCode=true");
        }
        setGameID(code);
        setPlayerCount(count);
        setGameMode(mode);
        sessionStorage.setItem("key_code", code);
    };

    const handleCancel = () => {
        network?.sendMessage({ action: "cancel_match" });
        network?.disconnectWebSocket();
        navigate("/home");
    };

    const handleBotRequest = () => {
        network?.sendMessage({ action: "bot_request" });
        console.log("Bot requested");
        setBotRequested(true);
    };

    useEffect(() => {
        const reconnect = sessionStorage.getItem("reconnect");
        if (reconnect == "false") {
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
            network?.setupUser(abilityCounts);
            console.log("Lobby shit going on");

            network?.getBoardData().then((data) => {
                navigate("/play", { state: { boardData: data } });
            });
            sessionStorage.setItem("reconnect", "true");
        } else {
            navigate("home");
        }
    }, []);

    if (!boardData) {
        return (
            <div>
                {gameID && (
                    <button
                        style={{
                            position: "absolute",
                            top: "10px",
                            left: "10px",
                            padding: "10px 20px",
                            fontSize: "16px",
                            cursor: "pointer",
                        }}
                        onClick={handleCancel}
                    >
                        Cancel
                    </button>
                )}
                <h1 className="whiteText">Waiting...</h1>
                {gameType != "LADDER" ? (
                    <div>
                        <h2 className="whiteText">Game Code: {gameID}</h2>
                        <h2 className="whiteText">
                            {playerCount} Player {gameMode} Friendly Match
                        </h2>
                    </div>
                ) : (
                    <h2 className="whiteText">
                        {playerCount} Player {gameMode} Ladder Match
                    </h2>
                )}
                {gameID && !botRequested && (
                    <div
                        style={{
                            position: "absolute",
                            right: "50px",
                            bottom: "10px",
                            display: "flex",
                            flexDirection: "column",
                            alignItems: "center",
                        }}
                    >
                        <h2 style={{ marginBottom: "10px" }}>No one online?</h2>
                        <button
                            style={{
                                padding: "10px 20px",
                                fontSize: "16px",
                                cursor: "pointer",
                            }}
                            onClick={handleBotRequest}
                        >
                            Play Bots
                        </button>
                    </div>
                )}
                {botRequested && (
                    <h2
                        style={{
                            position: "absolute",
                            right: "50px",
                            bottom: "10px",
                        }}
                    >
                        Bot requested
                    </h2>
                )}
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