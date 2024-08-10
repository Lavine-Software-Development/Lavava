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
    decks: any[][];
}

const Leaderboard: React.FC = () => {
    const [leaderboard, setLeaderboard] = useState<Player[]>([]);
    const [selectedUser, setSelectedUser] = useState<UserDetails | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [currentUser, setCurrentUser] = useState(null);
    const [gameCount, setGameCount] = useState(0);
    const [deckMode, setDeckMode] = useState("Original");
    const [deckIndex, setDeckIndex] = useState<number>(0);
    const [usersDecks, setUsersDecks] = useState<any[][]>([]);
    const [decks, setDecks] = useState<any[][]>([]);

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
        //console.log(`Fetching details for user: ${username}`);
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
                //console.log("Fetched user data:", data);
                setSelectedUser(data);
                const fetchedDecks: any[][] = data.decks || [];
                const modes = fetchedDecks.map((deck: any[]) => deck[deck.length - 1]);
                const newDeckIndex = modes.findIndex((mode: string) => mode === deckMode);
                const newDecks: any[][] = fetchedDecks.map((deck: any[]) => deck.slice(0, -1));
                setDeckIndex(newDeckIndex);
                setUsersDecks(newDecks);
                setDecks(fetchedDecks);
            })
            .catch(error => {
                console.error('Error fetching user details:', error);
                setError(`Failed to load user details: ${error.message}`);
            });
    };

    useEffect(() => {
        handleMyDeck();
    }, [deckMode]);

    const handleMyDeck = () => {
        if (!decks || decks.length === 0) {
            return;
        }
    
        const modes = decks.map((deck: any[]) => (deck && deck.length > 0 ? deck[deck.length - 1] : undefined));
        const newDeckIndex = modes.findIndex((mode: string) => mode === deckMode);
        const newDecks = decks.map((deck: any[]) => deck.slice(0, -1));
    
        setDeckIndex(newDeckIndex);
        setUsersDecks(newDecks);
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
                        <div className="tab-container" style={{ marginBottom: '10px'}}>
                            <button 
                                className={`tab-button tab-profile ${deckMode === "Original" ? "active" : ""}`}
                                onClick={() => setDeckMode("Original")}
                            >
                                Original
                            </button>
                            <button 
                                className={`tab-button tab-profile ${deckMode === "Royale" ? "active" : ""}`}
                                onClick={() => setDeckMode("Royale")}
                            >
                                Royale
                            </button>
                        </div>
                        <h2 className="text-shadow default-deck-text">{deckMode} Deck</h2>
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
                                        <div className="ability-count">{item.count}</div>
                                    </div>
                                ))
                            ) : (
                                <p>You have no saved abilities for {deckMode} mode</p>
                            )
                        ) : (
                            <p>Loading your deck...</p>
                        )}
                        </div>
                        <button onClick={() => setSelectedUser(null)}>Close</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Leaderboard;