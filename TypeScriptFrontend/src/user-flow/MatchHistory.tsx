import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import config from "../env-config";
import { jwtDecode } from "jwt-decode";

interface GameData {
    game_id: number;
    game_date: string;
    players: {
        username: string;
        rank: number;
        is_current_user: boolean;
    }[];
}

const MatchHistory: React.FC = () => {
    const navigate = useNavigate();
    const [matchHistory, setMatchHistory] = useState<GameData[]>([]);
    const [loading, setLoading] = useState(true);
    const [isDescending, setIsDescending] = useState(true);

    useEffect(() => {
        const fetchMatchHistory = async () => {
            const token = localStorage.getItem("userToken");
            try {
                const response = await fetch(
                    `${config.userBackend}/match-history`,
                    {
                        method: "GET",
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );
                const data = await response.json();
                if (response.ok) {
                    setMatchHistory(data.match_history);
                } else {
                    if (data.message === 'Login Token has expired!') {
                        localStorage.removeItem('userToken');
                        navigate("/login");
                    }
                    throw new Error(data.message);
                }
            } catch (error) {
                console.error("Error fetching match history:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchMatchHistory();
    }, []);

    const handleBack = () => {
        navigate(-1);
    };

    const toggleSortOrder = () => {
        setIsDescending(!isDescending);
    };

    const sortedMatchHistory = [...matchHistory].sort((a, b) => {
        const dateA = new Date(a.game_date).getTime();
        const dateB = new Date(b.game_date).getTime();
        return isDescending ? dateB - dateA : dateA - dateB;
    });

    if (loading) {
        return <div className="whiteText" style={{ fontSize: '26px', fontWeight: 'bold' }}>Match History Loading...</div>;
    }

    return (
        <div className="leaderboard-container scrollable-container">
            <div className="match-history-container">
                <button className="match-history-btn" onClick={handleBack}>Back to Profile</button>
                <h2>Ladder Match History</h2>
                <button className="sort-order-btn" onClick={toggleSortOrder}>
                    Sort: Recent Game
                    <span className="sort-arrow">{isDescending ? ' ↓' : ' ↑'}</span>
                </button>
                {sortedMatchHistory.map((game) => (
                    <div key={game.game_id} className="game-history-item">
                        <p>
                            <strong>Date:</strong>{" "}
                            {new Date(game.game_date).toLocaleDateString()}{" "}
                            {new Date(game.game_date).toLocaleTimeString([], {
                                hour: "2-digit",
                                minute: "2-digit",
                            })}
                        </p>
                        <p>
                            <strong>Players:</strong>
                        </p>
                        <ul>
                            {game.players.map((player, index) => {
                                let className = player.is_current_user
                                    ? player.rank === 1
                                        ? "current-user-win"
                                        : "current-user-lose"
                                    : "";
                                return (
                                    <li key={index} className={className}>
                                        {player.username} - Rank: {player.rank}
                                    </li>
                                );
                            })}
                        </ul>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default MatchHistory;