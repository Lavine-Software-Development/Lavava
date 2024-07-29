import React, { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import config from "../env-config";
import { jwtDecode } from 'jwt-decode';

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
        const savedPlayerCount = sessionStorage.getItem('playerCount');
        return savedPlayerCount ? parseInt(savedPlayerCount, 10) : 2;
    });
    const [keyCode, setKeyCode] = useState("");
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [showSalaryPopup, setShowSalaryPopup] = useState(false);
    const [showLoginPopup, setShowLoginPopup] = useState(false);
    const [showNoAbilityPopup, setShowNoAbilityPopup] = useState(false);
    const [friendlyMode, setFriendlyMode] = useState<string>(
        sessionStorage.getItem("friendlyMode") || "join"
    );
    const [showInvalidCodePopup, setShowInvalidCodePopup] = useState(false);

    useEffect(() => {
        sessionStorage.removeItem("key_code");
        const urlParams = new URLSearchParams(window.location.search);
        const invalidCode = urlParams.get('invalidCode');
        if (invalidCode === 'true') {
            setShowInvalidCodePopup(true);
        // Remove the query parameter
            window.history.replaceState({}, document.title, window.location.pathname);
        }

        const storedAbilities = sessionStorage.getItem("selectedAbilities");
        const token = localStorage.getItem("userToken");
        const isGuest = sessionStorage.getItem("guestToken");
        setIsLoggedIn(!!token);

        if (!isGuest && !token) {
            navigate("/login");
        }

        if (storedAbilities) {
            setSelectedAbilities(JSON.parse(storedAbilities));
        } else if (token) {
            fetch(`${config.userBackend}/user_abilities`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data && data.abilities) {
                        const abilities = data.abilities;
                        sessionStorage.setItem("selectedAbilities", JSON.stringify(abilities));
                        setSelectedAbilities(abilities);
                    }
                })
                .catch(error => {
                    console.error("Failed to fetch abilities:", error);
                });
        }

        const gameStyle = sessionStorage.getItem("gameStyle");
        if (gameStyle) {
            setTabAndCloseDropdown(gameStyle);
        }
        const storedFriendlyMode = sessionStorage.getItem("friendlyMode");
        if (storedFriendlyMode) {
            setFriendlyMode(storedFriendlyMode);
        }
        
    }, []);


    const hostTab = (e: number) => {
        setPlayerCount(e);
        sessionStorage.setItem('playerCount', e.toString());
        setPlayerCountDropdownOpen(false);
    };

    const handleHostGame = () => {
        sessionStorage.setItem("type", "HOST");
        sessionStorage.setItem("player_count", playerCount.toString());
        sessionStorage.removeItem("key_code");
        navigate("/lobby");
    };

    const handleLadderGame = () => {
        sessionStorage.setItem("type", "LADDER");
        sessionStorage.setItem("player_count", playerCount.toString());
        sessionStorage.removeItem("key_code");
        navigate("/lobby");
    };

    const handleJoinGame = () => {
        sessionStorage.setItem("type", "JOIN");
        sessionStorage.setItem("key_code", keyCode);
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
    }, [playDropdownOpen, playerCountDropdownOpen]);

    const handleClosePopups = () => {
        setShowSalaryPopup(false);
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
                    {selectedAbilities.length > 0 ? (
                        <button onClick={handlePlayDropdownFocus}>Play</button>
                    ) : (
                        <button
                            style={{ backgroundColor: "grey" }}
                            onClick={handlePlayDropdownFocus}
                        >
                            Play
                        </button>
                    )}
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
                <div style={{ height: '10px' }}></div> 
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
                            {selectedAbilities.map((ability, index) => (
                                <p style={{ textAlign: "center" }} key={index}>
                                    {ability.name}
                                    <img src={`./assets/abilityIcons/${ability.name}.png`} alt={ability.name}
                                        style={{
                                            width: "30px",
                                            height: "30px",
                                            objectFit: "contain",
                                            marginLeft: "10px",
                                            marginRight: "10px",
                                        }}
                                    />
                                    : {ability.count}
                                </p>
                            ))}
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
                                    <div
                                        className="key-code-container"
                                    >
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
                            <h3 style={{ textAlign: "center" }}>(For Elo)</h3>
                            {selectedAbilities.map((ability, index) => (
                                <p style={{ textAlign: "center" }} key={index}>
                                    {ability.name}
                                    <img
                                        src={`./public/assets/abilityIcons/${ability.name}.png`}
                                        alt={ability.name}
                                        style={{
                                            width: "30px",
                                            height: "30px",
                                            objectFit: "contain",
                                            marginLeft: "10px",
                                            marginRight: "10px",
                                        }}
                                    />
                                    : {ability.count}
                                </p>
                            ))}
                            {/* <label>Player Count:</label> */}
                            <div style={{ height: '65px' }}></div> 
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
                        <button onClick={() => setShowInvalidCodePopup(false)}>OK</button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Home;
