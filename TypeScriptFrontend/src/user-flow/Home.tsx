import React, { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

const Home: React.FC = () => {
    const navigate = useNavigate();
    const [selectedAbilities, setSelectedAbilities] = useState<any[]>([]);
    const [tab, setTab] = useState("HOST");
    const [playerCount, setPlayerCount] = useState(2);
    const [keyCode, setKeyCode] = useState("");
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [showSalaryPopup, setShowSalaryPopup] = useState(false);
    const [showLoginPopup, setShowLoginPopup] = useState(false);

    useEffect(() => {
        const storedAbilities = sessionStorage.getItem("selectedAbilities");
        const token = localStorage.getItem("userToken");
        setIsLoggedIn(!!token);
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
        setPlayerCountDropdownOpen(false);
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

    const [playDropdownOpen, setPlayDropdownOpen] = useState<boolean>(false);
    const playDropdownRef = useRef<HTMLDivElement>(null);
    const handlePlayDropdownFocus = () => {
        setPlayDropdownOpen(!playDropdownOpen);
    };

    const setTabAndCloseDropdown = (tab: string) => {
        setTab(tab);
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
    };

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
                            <li onClick={handleLadderClick}>Ladder</li>
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
                    {tab === "HOST" ? (
                        <div>
                            <h1 style={{ textAlign: "center" }}>Host Game</h1>
                            <h3 style={{ textAlign: "center" }}>
                                Ability : Count
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
                                                    hostTab(count, "")
                                                }
                                            >
                                                {count}
                                            </li>
                                        ))}
                                    </ul>
                                )}
                            </div>
                            <button className="btn" onClick={handleHostGame}>
                                Host
                            </button>
                            <button className="btn" onClick={handleHostGame}>
                                Host w/ Key
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
                    ) : tab === "JOIN" ? (
                        <div>
                            <h1 style={{ textAlign: "center" }}>Join Game</h1>
                            <h3 style={{ textAlign: "center" }}>
                                Ability : Count
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
                            <button className="btn" onClick={handleJoinGame}>
                                Join
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
                                <h1>Ladder</h1>
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
                                <button
                                    className="btn"
                                    onClick={handleHostGame}
                                >
                                    Join Ladder
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
            </div>
        </div>
    );
};

export default Home;
