import React, { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import config from "../env-config";

const Home: React.FC = () => {
    const navigate = useNavigate();
    const [selectedAbilities, setSelectedAbilities] = useState<any[]>([]);
    const [tab, setTab] = useState("");
    const [playerCount, setPlayerCount] = useState(2);
    const [keyCode, setKeyCode] = useState("");
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [showSalaryPopup, setShowSalaryPopup] = useState(false);
    const [showLoginPopup, setShowLoginPopup] = useState(false);
    const [showNoAbilityPopup, setShowNoAbilityPopup] = useState(false);

    useEffect(() => {
        const storedAbilities = sessionStorage.getItem("selectedAbilities");
        const token = localStorage.getItem("userToken");
        setIsLoggedIn(!!token);
        if (storedAbilities) {
            setSelectedAbilities(JSON.parse(storedAbilities));
        } else if (token) {
            fetch(`${config.userBackend}/user_abilities`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data && data.abilities) {
                        const abilities = data.abilities;
                        sessionStorage.setItem(
                            "selectedAbilities",
                            JSON.stringify(abilities)
                        );
                        setSelectedAbilities(abilities);
                    }
                })
                .catch((error) => {
                    console.error("Failed to fetch abilities:", error);
                });
        }
        const gameStyle = sessionStorage.getItem("gameStyle");
        if (gameStyle) {
            setTabAndCloseDropdown(gameStyle);
        }
    }, []);

    const handleLogout = () => {
        localStorage.removeItem("userToken");
        sessionStorage.clear();
        navigate("/login");
    };

    const hostTab = (e: number) => {
        setPlayerCount(e);
        setPlayerCountDropdownOpen(false);
    };

    const handleHostGame = () => {
        sessionStorage.setItem("type", "HOST");
        sessionStorage.setItem("player_count", playerCount.toString());
        sessionStorage.removeItem("key_code");
        // navigate('/play');
        navigate("/lobby");
    };

    const handleLadderGame = () => {
        sessionStorage.setItem("type", "LADDER");
        sessionStorage.setItem("player_count", playerCount.toString());
        sessionStorage.removeItem("key_code");
        // navigate('/play');
        navigate("/lobby");
    }

    const handleJoinGame = () => {
        sessionStorage.setItem("type", "JOIN");
        sessionStorage.setItem("key_code", keyCode);
        // navigate('/play');
        navigate("/lobby");
    };

    const [playDropdownOpen, setPlayDropdownOpen] = useState<boolean>(false);
    const playDropdownRef = useRef<HTMLDivElement>(null);
    const handlePlayDropdownFocus = () => {
        if (selectedAbilities.length > 0) {
            setPlayDropdownOpen(!playDropdownOpen);
        }
        else {
            setShowNoAbilityPopup(true);
        }
    };

    const setTabAndCloseDropdown = (tab: string) => {
        setTab(tab);
        sessionStorage.setItem("gameStyle", tab)
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

    return (
        <div className="dashboard-container" id="home">
            <div className="profile-card">
                <h1 className="form-title">Home</h1>
                <div className="app-drop-down-container" ref={playDropdownRef}>
                {selectedAbilities.length > 0 ? (
                    <button onClick={handlePlayDropdownFocus}>Play</button>
                    ) : (
                    <button style={{ backgroundColor: 'grey', }} onClick={handlePlayDropdownFocus}>Play</button>
                )} 
                    {playDropdownOpen && (
                        <ul>
                            <li onClick={handleLadderClick}>Ladder</li>
                            <li onClick={() => setTabAndCloseDropdown("HOST")}>
                                Host
                            </li>
                            <li onClick={() => setTabAndCloseDropdown("JOIN")}>
                                Join
                            </li>
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
                {isLoggedIn ? (
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
                )}
            </div>
            {(selectedAbilities.length > 0 && tab != "") && (
                <div className="profile-card">
                    {tab === "HOST" ? (
                        <div>
                            <h1 style={{ textAlign: "center" }}>Host</h1>
                            <h3 style={{ textAlign: "center" }}>
                                (Friendly Match)
                            </h3>
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
                            <label>Player Count:</label>
                            <div
                                className="player-count-drop-down-container"
                                ref={playerCountDropdownRef}
                            >
                                <button
                                    onClick={handlePlayerCountDropdownFocus}
                                >
                                    {playerCount}
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
                            <button className="btn" style={{ backgroundColor: 'green', }} onClick={handleHostGame}>
                                Host Match
                            </button>
                        </div>
                    ) : tab === "JOIN" ? (
                        <div>
                            <h1 style={{ textAlign: "center" }}>Join</h1>
                            <h3 style={{ textAlign: "center" }}>
                                (Friendly Match)
                            </h3>
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
                            <button className="btn"  style={{ backgroundColor: 'green', }} onClick={handleJoinGame}>
                                Join Match
                            </button>
                            <input
                                type="text"
                                className="text-box"
                                placeholder="enter key code"
                                value={keyCode}
                                onChange={(e) =>
                                    setKeyCode(e.target.value.toUpperCase())
                                }
                            />
                        </div>
                    ) : (
                        tab === "LADDER" && (
                            <div>
                                <h1 style={{ textAlign: "center" }}>Ladder</h1>
                                <h3 style={{ textAlign: "center" }}>
                                (For Elo)
                                </h3>
                                {selectedAbilities.map((ability, index) => (
                                    <p
                                        style={{ textAlign: "center" }}
                                        key={index}
                                    >
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
                                <label>Player Count:</label>
                                <div
                                    className="player-count-drop-down-container"
                                    ref={playerCountDropdownRef}
                                >
                                    <button
                                        onClick={handlePlayerCountDropdownFocus}
                                    >
                                        {playerCount}
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
                                    style={{ backgroundColor: 'green', }} 
                                    onClick={handleLadderGame}
                                >
                                    
                                    Find Match
                                </button>
                            </div>
                        )
                    )}
                </div>
            )}
            <div className="popup-container">
                {showSalaryPopup && (
                    <div className="popup salary-popup">
                        <p>
                            You cannot host a game with a leftover salary
                            greater than 10.
                        </p>
                        <button onClick={handleClosePopups}>OK</button>
                    </div>
                )}
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
            </div>
        </div>
    );
};

export default Home;

