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

    useEffect(() => {
        fetch(`${config.userBackend}/leaderboard`)
            .then(response => response.json())
            .then(data => {
                console.log("Leaderboard data:", data);
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

    if (error) {
        return <div className="error-message">{error}</div>;
    }

    return (
        <div className="leaderboard-container scrollable-container">
            <h1>Leaderboard</h1>
            <ul className="leaderboard-list">
                {leaderboard.map((player, index) => (
                    <li key={index} className={`leaderboard-item ${index < 3 ? 'top-three' : ''}`}>
                        <div className="rank-icon">
                            <span className={`rank ${index === 0 ? 'rank-1' : index === 1 ? 'rank-2' : index === 2 ? 'rank-3' : ''}`}>
                                {index + 1}
                            </span>
                        </div>
                        <span className="player-name" onClick={() => handleUserClick(player.userName)}>
                            {player.displayName !== "Not Yet Specified" ? player.displayName : player.userName}
                        </span>
                        <span className="player-score">{player.elo}</span>
                    </li>
                ))}
            </ul>
            {selectedUser && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h2>{selectedUser.displayName || selectedUser.username}</h2>
                        <p><strong>Username:</strong> {selectedUser.username}</p>
                        <p><strong className="elo-text">ELO:</strong> {selectedUser.elo}</p>
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