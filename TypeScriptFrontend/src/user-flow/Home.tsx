import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

const Home: React.FC = () => {
    const navigate = useNavigate();
    const [selectedAbilities, setSelectedAbilities] = useState<any[]>([]);
    const [tab, setTab] = useState("HOST"); // State to manage tabs
    const [playerCount, setPlayerCount] = useState(2); // Default to 2 players
    const [keyCode, setKeyCode] = useState("");

    useEffect(() => {
        const storedAbilities = sessionStorage.getItem("selectedAbilities");
        const token = localStorage.getItem("userToken");
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
    };

    const handleHostGame = () => {
        sessionStorage.setItem("type", "HOST");
        sessionStorage.setItem("player_count", playerCount.toString());
        sessionStorage.setItem("key_code", keyCode);
        // navigate('/play');
        navigate("/lobby");
    };

    const handleJoinGame = () => {
        sessionStorage.setItem("type", "JOIN");
        sessionStorage.setItem("key_code", keyCode);
        // navigate('/play');
        navigate("/lobby");
    };

    return (
        <div className="dashboard-container" id="home">
            <div className="profile-card">
                <h1 className="form-title">Home</h1>
                <a href="profile">Profile</a>
                <input
                    type="submit"
                    className="btn"
                    value="Build Deck"
                    onClick={() => navigate("/builder")}
                />
                <nav
                    style={{
                        backgroundColor: "#f0f0f0",
                        padding: "10px 0",
                        borderBottom: "2px solid #ccc",
                        marginBottom: "20px",
                    }}
                >
                    <div
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            gap: "20px",
                        }}
                    >
                        <Link
                            to="/websocket-test"
                            style={{
                                padding: "10px 20px",
                                textDecoration: "none",
                                color: "#333",
                                fontWeight: "bold",
                            }}
                        >
                            WebSocket Test
                        </Link>
                    </div>
                </nav>
                <input
                    type="submit"
                    className="btn"
                    value="Log Out"
                    onClick={handleLogout}
                />
            </div>
            {selectedAbilities.length > 0 && (
                <div className="profile-card">
                    <div className="tab-header">
                        <button onClick={() => setTab("HOST")}>HOST</button>
                        <button onClick={() => setTab("JOIN")}>JOIN</button>
                    </div>
                    <ul>
                        {selectedAbilities.map((ability, index) => (
                            <li key={index}>
                                {ability.name} - Count: {ability.count}
                            </li>
                        ))}
                    </ul>
                    {tab === "HOST" ? (
                        <div>
                            <label>Player Count:</label>
                            <select
                                onChange={(e) =>
                                    hostTab(Number(e.target.value), "1234")
                                }
                                value={playerCount}
                            >
                                {[2, 3, 4, 5].map((count) => (
                                    <option key={count} value={count}>
                                        {count}
                                    </option>
                                ))}
                            </select>

                            <button
                                className="btn"
                                onClick={() => handleHostGame()}
                            >
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
                            <button
                                className="btn"
                                onClick={() => handleJoinGame()}
                            >
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

