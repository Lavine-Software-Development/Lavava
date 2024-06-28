import React, { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

const Home: React.FC = () => {
    const navigate = useNavigate();
    const [selectedAbilities, setSelectedAbilities] = useState<any[]>([]);
    const [tab, setTab] = useState("HOST"); // State to manage tabs
    const [playerCount, setPlayerCount] = useState(2); // Default to 2 players
    const [keyCode, setKeyCode] = useState("");
    const [isLoggedIn, setIsLoggedIn] = useState(false); // State to track login status

    useEffect(() => {
        const storedAbilities = sessionStorage.getItem("selectedAbilities");
        const token = localStorage.getItem("userToken");
        setIsLoggedIn(!!token); // Update login status
        if (storedAbilities) {
            setSelectedAbilities(JSON.parse(storedAbilities));
        } else if (token) {
            fetch("http://localhost:5001/user_abilities", {
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
    }, []);

    const handleLogout = () => {
        localStorage.removeItem("userToken");
        sessionStorage.clear();
        navigate("/login");
    };

    const hostTab = (e: number, code: string) => {
        setPlayerCount(e);
        setKeyCode(code);
        setPlayerCountDropdownOpen(false); // Close the player count dropdown when selecting count
    };

    const handleHostGame = () => {
        sessionStorage.setItem("type", "HOST");
        sessionStorage.setItem("player_count", playerCount.toString());
        sessionStorage.setItem("key_code", keyCode);
        navigate("/play");
    };

    const handleJoinGame = () => {
        sessionStorage.setItem("type", "JOIN");
        sessionStorage.setItem("key_code", keyCode);
        navigate("/play");
    };

    // State and handlers for "Play" button dropdown
    const [playDropdownOpen, setPlayDropdownOpen] = useState<boolean>(false);
    const playDropdownRef = useRef<HTMLDivElement>(null);
    const handlePlayDropdownFocus = () => {
        setPlayDropdownOpen(!playDropdownOpen);
    };

    const setTabAndCloseDropdown = (tab: string) => {
        setTab(tab); // update tab state
        setPlayDropdownOpen(false); // Close the play dropdown
    };

    // State and handlers for player count dropdown
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

    useEffect(() => {
        window.addEventListener("click", handleClickOutsideDropdown);
        return () => {
            window.removeEventListener("click", handleClickOutsideDropdown);
        };
    }, [playDropdownOpen, playerCountDropdownOpen]);

    return (
        <div className="dashboard-container" id="home">
            <div className="profile-card">
                <h1 className="form-title">Home</h1>
                <div className="app-drop-down-container" ref={playDropdownRef}>
                    <button onClick={handlePlayDropdownFocus}>Play</button>
                    {playDropdownOpen && (
                        <ul>
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
            {selectedAbilities.length > 0 && (
                <div className="profile-card">
                    <h3 style={{ textAlign: "center" }}>Ability : Count</h3>
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
                    {tab === "HOST" ? (
                        <div>
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
                                                    hostTab(count, "")
                                                }
                                            >
                                                {count}
                                            </li>
                                        ))}
                                    </ul>
                                )}
                            </div>
                            <input
                                type="text"
                                placeholder="Enter Keycode"
                                onChange={(e) => setKeyCode(e.target.value)}
                                value={keyCode}
                            />
                            <button className="btn" onClick={handleHostGame}>
                                Host Game
                            </button>
                        </div>
                    ) : (
                        <div>
                            <input
                                type="text"
                                placeholder="Enter Keycode"
                                onChange={(e) => setKeyCode(e.target.value)}
                                value={keyCode}
                            />
                            <button className="btn" onClick={handleJoinGame}>
                                Join Game
                            </button>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default Home;
