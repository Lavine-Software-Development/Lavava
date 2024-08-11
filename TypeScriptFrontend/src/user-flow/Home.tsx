import React, { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import config from "../env-config";
import { jwtDecode } from 'jwt-decode';
import { abilityColors } from "../user-flow/ability_utils";

function getDeviceType() {
    const ua = navigator.userAgent;

    if (/mobile/i.test(ua)) {
        return "Mobile";
    }
    if (/tablet/i.test(ua)) {
        return "Tablet";
    }
    if (/iPad|PlayBook/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) {
        return "Tablet";
    }
    return "Desktop";
}

const Home: React.FC = () => {
    const navigate = useNavigate();
    // check if login token has expired
    useEffect(() => {
        const validateToken = () => {
            const token = localStorage.getItem("userToken");
            if (!token){
                return;
            }

            try {
                const decodedToken = jwtDecode(token);
                const currentTime = Date.now() / 1000; // convert to seconds
                if (decodedToken.exp < currentTime) {
                    localStorage.removeItem("userToken");
                    navigate("/login")
                }
            } catch (error) {
                console.error("Error deccoding token:", error);
                localStorage.removeItem("userToken");
            }
        };

        validateToken();
    }, []);

    const [selectedAbilities, setSelectedAbilities] = useState<any[]>([]);
    const [tab, setTab] = useState("");
    const [playerCount, setPlayerCount] = useState(() => {
        const savedPlayerCount = sessionStorage.getItem("playerCount");
        return savedPlayerCount ? parseInt(savedPlayerCount, 10) : 2;
    });
    const [keyCode, setKeyCode] = useState("");
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [showLoginPopup, setShowLoginPopup] = useState(false);
    const [showNoAbilityPopup, setShowNoAbilityPopup] = useState(false);
    const [friendlyMode, setFriendlyMode] = useState<string>(
        sessionStorage.getItem("friendlyMode") || "join"
    );
    const [gameMode, setGameMode] = useState<string>(
        sessionStorage.getItem("gameMode") || "Original"
    );
    const [gameModeDropdownOpen, setGameModeDropdownOpen] = useState<boolean>(false);
    const gameModeDropdownRef = useRef<HTMLDivElement>(null);
    const [showInvalidCodePopup, setShowInvalidCodePopup] = useState(false);
    const [deckIndex, setDeckIndex] = useState<number>(0);
    const [usersDecks, setUsersDecks] = useState<any[][]>([]);
    const [decks, setDecks] = useState<any[][]>([]);
    const [guestDecks, setGuestDecks] = useState<any[][]>([]);

    useEffect(() => {
        sessionStorage.removeItem("key_code");
        const urlParams = new URLSearchParams(window.location.search);
        const invalidCode = urlParams.get("invalidCode");
        if (invalidCode === "true") {
            setShowInvalidCodePopup(true);
            // Remove the query parameter
            window.history.replaceState(
                {},
                document.title,
                window.location.pathname
            );
        }
        const token = localStorage.getItem("userToken");
        const isGuest = sessionStorage.getItem("guestToken");
        setIsLoggedIn(!!token);

        if (isGuest) {
            // Load guest decks
            const guestDecks = JSON.parse(sessionStorage.getItem('guestDecks') || '{}');
            setGuestDecks(guestDecks);
            setSelectedAbilities(guestDecks[gameMode])
        } else if (token) {
            // Fetch user decks from backend
            fetch(`${config.userBackend}/user_abilities`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data && data.decks) {
                        const fetchedDecks: any[][] = data.decks || [];
                        const modes = fetchedDecks.map((deck: any[]) => deck[deck.length - 1]);
                        const newDeckIndex = modes.findIndex((mode: string) => mode === gameMode);
                        const newDecks: any[][] = fetchedDecks.map((deck: any[]) => deck.slice(0, -1));
                        setDeckIndex(newDeckIndex);
                        setUsersDecks(newDecks);
                        setDecks(fetchedDecks);
                        setSelectedAbilities(newDecks[newDeckIndex]);
                    }
                })
                .catch((error) => {
                    console.error("Failed to fetch abilities:", error);
                });
        }

        let prevMode = sessionStorage.getItem("gameMode");
        if (prevMode === "Royale") {
            handleGameModeChange("Royale");
        } else {
            handleGameModeChange("Original");
        }

        if (!isGuest && !token) {
            navigate("/login");
        }

        const gameStyle = sessionStorage.getItem("gameStyle");
        if (gameStyle) {
            setTabAndCloseDropdown(gameStyle);
        }
        const storedFriendlyMode = sessionStorage.getItem("friendlyMode");
        if (storedFriendlyMode) {
            setFriendlyMode(storedFriendlyMode);
        }
        const storedGameMode = sessionStorage.getItem("gameMode");
        if (storedGameMode) {
            setGameMode(storedGameMode);
        }
    }, []);

    useEffect(() => {
        const isGuest = sessionStorage.getItem("guestToken");
        if (isGuest) {
            setSelectedAbilities(guestDecks[gameMode]);
        }
        else {
            handleMyDeck();
            setSelectedAbilities(usersDecks[deckIndex]);
        }
    }, [gameMode]);

    const handleMyDeck = () => {
        if (!decks || decks.length === 0) {
            return;
        }
    
        const modes = decks.map((deck: any[]) => (deck && deck.length > 0 ? deck[deck.length - 1] : undefined));
        const newDeckIndex = modes.findIndex((mode: string) => mode === gameMode);
        const newDecks = decks.map((deck: any[]) => deck.slice(0, -1));
    
        setDeckIndex(newDeckIndex);
        setUsersDecks(newDecks);
    };

    const handleGameModeDropdownFocus = () => {
        setGameModeDropdownOpen(!gameModeDropdownOpen);
    };
    
    const handleGameModeChange = (mode: string) => {
        setGameMode(mode);
        sessionStorage.setItem("gameMode", mode);
        setGameModeDropdownOpen(false);
    };

    const hostTab = (e: number) => {
        setPlayerCount(e);
        sessionStorage.setItem("playerCount", e.toString());
        setPlayerCountDropdownOpen(false);
    };

    const handleHostGame = () => {
        sessionStorage.setItem("type", "HOST");
        sessionStorage.setItem("player_count", playerCount.toString());
        sessionStorage.removeItem("key_code");
        sessionStorage.setItem("reconnect", "false");
        navigate("/lobby");
    };

    const handleLadderGame = () => {
        sessionStorage.setItem("type", "LADDER");
        sessionStorage.setItem("player_count", playerCount.toString());
        sessionStorage.removeItem("key_code");
        sessionStorage.setItem("reconnect", "false");
        navigate("/lobby");
    };

    const handleJoinGame = () => {
        sessionStorage.setItem("type", "JOIN");
        sessionStorage.setItem("key_code", keyCode);
        sessionStorage.setItem("reconnect", "false");
        navigate("/lobby");
    };

    const [playDropdownOpen, setPlayDropdownOpen] = useState<boolean>(false);
    const playDropdownRef = useRef<HTMLDivElement>(null);
    const handlePlayDropdownFocus = () => {
        const deviceType = getDeviceType();
        if (deviceType !== "Desktop") {
            alert("Please use a desktop to play.");
            return;
        }
        setPlayDropdownOpen(!playDropdownOpen);
        if (selectedAbilities.length > 0) {
            setPlayDropdownOpen(!playDropdownOpen);
        } else {
            setShowNoAbilityPopup(true);
        }
    };

    const setTabAndCloseDropdown = (tab: string) => {
        setTab(tab);
        sessionStorage.setItem("gameStyle", tab);
        setKeyCode("");
        setPlayDropdownOpen(false);
    };

    const [playerCountDropdownOpen, setPlayerCountDropdownOpen] =
        useState<boolean>(false);
    const playerCountDropdownRef = useRef<HTMLDivElement>(null);

    const handlePlayerCountDropdownFocus = () => {
        setPlayerCountDropdownOpen(!playerCountDropdownOpen);
    };

    const handleClickOutsideDropdown = (e: any) => {
        if (
            playDropdownOpen &&
            playDropdownRef.current &&
            !playDropdownRef.current.contains(e.target)
        ) {
            setPlayDropdownOpen(false);
        }

        if (
            gameModeDropdownOpen &&
            gameModeDropdownRef.current &&
            !gameModeDropdownRef.current.contains(e.target as Node)
        ) {
            setGameModeDropdownOpen(false);
        }

        if (
            playerCountDropdownOpen &&
            playerCountDropdownRef.current &&
            !playerCountDropdownRef.current.contains(e.target)
        ) {
            setPlayerCountDropdownOpen(false);
        }
    };

    const handleLadderClick = () => {
        if (!isLoggedIn) {
            setShowLoginPopup(true); // Show login popup if not logged in
        } else {
            setTabAndCloseDropdown("LADDER"); // Proceed with setting the tab to LADDER
        }
    };

    const handleFriendlyClick = () => {
        setTabAndCloseDropdown("FRIENDLY"); // Proceed with setting the tab to FRIENDLY
    };

    useEffect(() => {
        window.addEventListener("click", handleClickOutsideDropdown);
        return () => {
            window.removeEventListener("click", handleClickOutsideDropdown);
        };
    }, [gameModeDropdownOpen, playDropdownOpen, playerCountDropdownOpen]);

    const handleClosePopups = () => {
        setShowLoginPopup(false);
        setShowNoAbilityPopup(false);
    };

    const switchToHost = () => {
        setFriendlyMode("host");
        sessionStorage.setItem("friendlyMode", "host");
    };

    const switchToJoin = () => {
        setFriendlyMode("join");
        sessionStorage.setItem("friendlyMode", "join");
    };
    

    return (
        <div className="dashboard-container" id="home">
            <div className="profile-card">
                <h1 className="form-title">Home</h1>
                <div className="app-drop-down-container" ref={playDropdownRef}>
                    <button onClick={handlePlayDropdownFocus}>Play</button>
                    {playDropdownOpen && (
                        <ul>
                            <li onClick={handleLadderClick}>Ladder</li>
                            <li onClick={handleFriendlyClick}>Friendly</li>
                        </ul>
                    )}
                </div>
                <input
                    type="submit"
                    className="btn"
                    value="Build Deck"
                    onClick={() => navigate("/builder")}
                />
                <input
                    type="submit"
                    className="btn"
                    value="How To Play"
                    onClick={() => navigate("/how-to-play")}
                />
                {/* {isLoggedIn ? (
                    <input
                        type="submit"
                        className="btn"
                        value="Log Out"
                        onClick={handleLogout}
                    />
                ) : (
                    <input
                        type="submit"
                        className="btn"
                        value="Login"
                        onClick={() => navigate("/login")}
                    />
                )} */}
                <input
                    type="submit"
                    className="btn"
                    value="The Team"
                    onClick={() => navigate("/team")}
                />
                <div style={{ height: "10px" }}></div>
            </div>
            {selectedAbilities.length > 0 && tab !== "" && (
                <div className="profile-card">
                    {tab === "FRIENDLY" ? (
                        <div>
                            <div className="switch-buttons">
                                <button
                                    className="btn"
                                    style={{
                                        backgroundColor:
                                            friendlyMode === "host"
                                                ? "green"
                                                : "lightgreen",
                                        marginRight: "10px", // Adjust margin as needed
                                    }}
                                    onClick={switchToHost}
                                >
                                    Host Game
                                </button>
                                <button
                                    className="btn"
                                    style={{
                                        backgroundColor:
                                            friendlyMode === "join"
                                                ? "green"
                                                : "lightgreen",
                                    }}
                                    onClick={switchToJoin}
                                >
                                    Join Game
                                </button>
                            </div>
                            <h1 style={{ textAlign: "center" }}>
                                Friendly Match
                            </h1>
                            <h3 style={{ textAlign: "center" }}>(No elo)</h3>

                            <div className="abilities-container-friendly">
                                {usersDecks && usersDecks[deckIndex] ? (
                                    usersDecks[deckIndex].length > 0 ? (
                                        usersDecks[deckIndex].map((item: { name: string; count: number }, index: number) => (
                                            <div key={index} className="ability-square" style={{ backgroundColor: abilityColors[item.name]}}>
                                                <div className="ability-icon">
                                                    <img
                                                        src={`./assets/abilityIcons/${item.name}.png`}
                                                        alt={item.name}
                                                        className="ability-img"
                                                    />
                                                </div>
                                                <div className="ability-count" style={{fontSize: '1.2rem'}}>{item.count}</div>
                                            </div>
                                        ))
                                    ) : (
                                        <p>You have no saved abilities for {gameMode} mode</p>
                                    )
                                ) : (
                                    <p>Loading your deck...</p>
                                )}
                                </div>
                            {friendlyMode === "host" ? (
                                <>
                                    {/* <label>Player Count:</label> */}
                                    <div
                                        className="player-count-drop-down-container"
                                        ref={playerCountDropdownRef}
                                    >
                                        <button
                                            onClick={
                                                handlePlayerCountDropdownFocus
                                            }
                                        >
                                            {playerCount} Players
                                        </button>
                                        {playerCountDropdownOpen && (
                                            <ul>
                                                {[2, 3, 4, 5].map((count) => (
                                                    <li
                                                        key={count}
                                                        onClick={() =>
                                                            hostTab(count)
                                                        }
                                                    >
                                                        {count}
                                                    </li>
                                                ))}
                                            </ul>
                                        )}
                                    </div>
                                    <div
                                        className="player-count-drop-down-container"
                                        ref={gameModeDropdownRef}
                                    >
                                        <button onClick={handleGameModeDropdownFocus}>
                                            {gameMode} Mode
                                        </button>
                                        {gameModeDropdownOpen && (
                                            <ul>
                                                <li onClick={() => handleGameModeChange("Original")}>
                                                    Original
                                                </li>
                                                <li onClick={() => handleGameModeChange("Royale")}>
                                                    Royale
                                                </li>
                                            </ul>
                                        )}
                                    </div>
                                    <button
                                        className="btn"
                                        style={{ backgroundColor: "green" }}
                                        onClick={handleHostGame}
                                    >
                                        Host Match
                                    </button>
                                </>
                            ) : (
                                <>
                                    <div className="key-code-container">
                                        <input
                                            type="text"
                                            className="text-box"
                                            placeholder="enter key code"
                                            value={keyCode}
                                            onChange={(e) =>
                                                setKeyCode(
                                                    e.target.value.toUpperCase()
                                                )
                                            }
                                        />
                                    </div>
                                    <button
                                        className="btn"
                                        style={{ backgroundColor: "green" }}
                                        onClick={handleJoinGame}
                                    >
                                        Join Match
                                    </button>
                                </>
                            )}
                        </div>
                    ) : tab === "LADDER" ? (
                        <div>
                            <h1 style={{ textAlign: "center" }}>Ladder</h1>
                            <h3 style={{ textAlign: "center" }}>(For elo)</h3>

                            <div style={{ height: "43px" }}></div>
                            <div
                                className="player-count-drop-down-container"
                                ref={playerCountDropdownRef}
                            >
                                <button
                                    onClick={handlePlayerCountDropdownFocus}
                                >
                                    {playerCount} Players
                                </button>
                                {playerCountDropdownOpen && (
                                    <ul>
                                        {[2, 3, 4, 5].map((count) => (
                                            <li
                                                key={count}
                                                onClick={() => hostTab(count)}
                                            >
                                                {count}
                                            </li>
                                        ))}
                                    </ul>
                                )}
                            </div>
                            <div
                                className="player-count-drop-down-container"
                                ref={gameModeDropdownRef}
                            >
                                <button onClick={handleGameModeDropdownFocus}>
                                    {gameMode} Mode
                                </button>
                                {gameModeDropdownOpen && (
                                    <ul>
                                        <li onClick={() => handleGameModeChange("Original")}>
                                            Original
                                        </li>
                                        <li onClick={() => handleGameModeChange("Royale")}>
                                            Royale
                                        </li>
                                    </ul>
                                )}
                            </div>
                            {/* <div style={{ height: '5px' }}></div>  */}
                            <button
                                className="btn"
                                style={{ backgroundColor: "green" }}
                                onClick={handleLadderGame}
                            >
                                Find Match
                            </button>
                        </div>
                    ) : null}
                </div>
            )}
            <div className="popup-container">
                {showLoginPopup && !isLoggedIn && (
                    <div className="popup login-popup">
                        <p>You need to log in to play Ladder.</p>
                        <button onClick={() => navigate("/login")}>
                            Log In
                        </button>
                        <button onClick={handleClosePopups}>Cancel</button>
                    </div>
                )}
                {showNoAbilityPopup && (
                    <div className="popup login-popup">
                        <p>You need to build a deck to Play.</p>
                        <button onClick={() => navigate("/builder")}>
                            Build
                        </button>
                        <button onClick={handleClosePopups}>Cancel</button>
                    </div>
                )}
                {showInvalidCodePopup && (
                    <div className="popup invalid-code-popup">
                        <p>Invalid game code. Please try again.</p>
                        <button onClick={() => setShowInvalidCodePopup(false)}>
                            OK
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Home;

