import React, { useState, useEffect } from "react";
import '../../styles/style.css';
import config from '../env-config';
import { abilityColors } from "../user-flow/ability_utils";

interface Player {
    userName: string;
    displayName: string;
    elo: number;
}

interface UserDetails {
    username: string;
    displayName: string;
    elo: number;
    deck: Array<{name: string, count: number}>;
}

const Leaderboard: React.FC = () => {
    const [leaderboard, setLeaderboard] = useState<Player[]>([]);
    const [selectedUser, setSelectedUser] = useState<UserDetails | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [currentUser, setCurrentUser] = useState(null);
    const [gameCount, setGameCount] = useState(0);

    useEffect(() => {
        const fetchUserName = async () => {
            const token = localStorage.getItem("userToken");
            try {
                const response = await fetch(
                    `${config.userBackend}/current-user`,
                    {
                        method: "GET",
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );
                const data = await response.json();
                if (response.ok) {
                    setCurrentUser(data.username);
                    setGameCount(data.gameCount);
                } else {
                    throw new Error(data.message);
                }
            } catch (error) {
                console.error("Error fetching match history:", error);
            }
        };
        fetchUserName();
    }, []);

    useEffect(() => {
        fetch(`${config.userBackend}/leaderboard`)
            .then(response => response.json())
            .then(data => {
                //console.log("Leaderboard data:", data);
                setLeaderboard(data.leaderboard);
            })
            .catch(error => {
                console.error('Error fetching leaderboard data:', error);
                setError('Failed to load leaderboard data');
            });
    }, []);

    const handleUserClick = (username: string) => {
        console.log(`Fetching details for user: ${username}`);
        fetch(`${config.userBackend}/user/${username}`)
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => {
                        throw new Error(err.error || 'Failed to fetch user details');
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log("Fetched user data:", data);
                setSelectedUser(data);
            })
            .catch(error => {
                console.error('Error fetching user details:', error);
                setError(`Failed to load user details: ${error.message}`);
            });
    };

    const isCurrentUserOnLeaderboard = currentUser && leaderboard.some(player => player.userName === currentUser);

    if (error) {
        return <div className="error-message">{error}</div>;
    }

    return (
        <div className="leaderboard-container scrollable-container">
            <h1>Leaderboard</h1>
            {!isCurrentUserOnLeaderboard && currentUser && (
                <p className="leaderboard-info leaderboard-note">
                    Note: You need to play {3 - gameCount} more ladder matches to appear on the leaderboard.
                </p>
            )}
            <ul className="leaderboard-list">
                {leaderboard.map((player, index) => (
                    <li key={index} className={`leaderboard-item ${index < 3 ? 'top-three' : ''} ${player.userName === currentUser ? 'current-user' : ''}`}>
                        <div className="rank-icon">
                            <span className={`rank ${index === 0 ? 'rank-1' : index === 1 ? 'rank-2' : index === 2 ? 'rank-3' : ''}`}>
                                {index + 1}
                            </span>
                        </div>
                        <span className="player-name" onClick={() => handleUserClick(player.userName)}>
                            {player.displayName !== "Not Yet Specified" ? player.displayName : player.userName}
                            {player.userName === currentUser}
                        </span>
                        <span className="player-score">{player.elo}</span>
                    </li>
                ))}
            </ul>
            {selectedUser && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h2>{selectedUser.displayName !== "Not Yet Specified" ? selectedUser.displayName : selectedUser.username}</h2>
                        {selectedUser.displayName !== "Not Yet Specified" && (
                            <p><strong>Username:</strong> {selectedUser.username}</p>
                        )}
                        <p><strong>ELO:</strong> {selectedUser.elo}</p>
                        {selectedUser.deck && selectedUser.deck.length > 0 ? (
                            <div className="abilities-container-leaderboard">
                                {selectedUser.deck.map((card, index) => (
                                <div key={index} className="ability-square" style={{ backgroundColor: abilityColors[card.name] }}>
                                    <div className="ability-icon">
                                    <img
                                        src={`./assets/abilityIcons/${card.name}.png`}
                                        alt={card.name}
                                        className="ability-img"
                                    />
                                    </div>
                                    <div className="ability-count">{card.count}</div>
                                </div>
                                ))}
                            </div>
                        ) : (
                            <p>No deck information available</p>
                        )}
                        <button onClick={() => setSelectedUser(null)}>Close</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Leaderboard;