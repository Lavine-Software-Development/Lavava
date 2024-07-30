import React, { useState, useEffect } from 'react';
import '../../styles/style.css';
import { Link, useNavigate } from 'react-router-dom';
import config from '../env-config';
import { abilityColors } from "../user-flow/ability_utils";

interface PlayerData {
    username: string;
    rank: number;
    is_current_user: boolean;
}

interface GameData {
    game_id: number;
    game_date: string;
    players: PlayerData[];
}

interface ProfileData {
    userName: string;
    displayName: string;
    email: string;
    abilities: { name: string; count: number }[];
    elo: number;
    last_game: GameData | null;
}

const Profile: React.FC = () => {
    const navigate = useNavigate();
    const [profileData, setProfileData] = useState<ProfileData>({
        userName: 'Loading...',
        displayName: 'Loading...',
        email: 'Loading...',
        abilities: [], // Default to at least one empty list
        elo: 1000,
        last_game: null,
    });

    const [isEditing, setIsEditing] = useState(false);
    const [newDisplayName, setNewDisplayName] = useState(profileData.displayName);
    const [popupMessage, setPopupMessage] = useState('');
    const [showPopup, setShowPopup] = useState(false);

    const handleChangePassword = () => {
        navigate("/change-password");
    };

    const handleMatchHistoryClick = () => {
        navigate("/match-history");
    };

    const handleLogout = () => {
        localStorage.removeItem("userToken");
        sessionStorage.clear();
        navigate("/login");
    };

    const handleEditClick = () => {
        setIsEditing(true);
        setNewDisplayName('');
        setPopupMessage('');
        setShowPopup(false);
    }

    const handleUpdateClick = () => {
        if (newDisplayName.trim() === '' || newDisplayName.length < 5) {
            setPopupMessage('Display name must be at least 5 characters long');
            setShowPopup(true);
            return;
        }

        fetch(`${config.userBackend}/update_display_name`, {
            method: 'POST', // use POST to send the data
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${localStorage.getItem('userToken')}`,
            },
            body: JSON.stringify({
                newDisplayName: newDisplayName,
            }),
        })
            .then((response) => response.ok)
            .then((ok) => {
                if (ok) {
                    // Update the displayName in the profileData state
                    setProfileData(prevData => ({
                        ...prevData,
                        displayName: newDisplayName,
                    }));
                    setIsEditing(false);
                    setPopupMessage('');
                    setShowPopup(false);
                }
            })
            .catch((error) => {
                console.error("Failed to update the user display name", error);
            });
        setIsEditing(false);
    }

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem('userToken');
            try {
                const response = await fetch(`${config.userBackend}/profile`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                const data = await response.json();
                if (response.ok) {
                    setProfileData(data);
                } else {
                    if (data.message === 'Login Token has expired!') {
                        localStorage.removeItem('userToken');
                        navigate("/login");
                    }
                    throw new Error(data.message);
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };
        fetchData();
    }, []);

    if (!localStorage.getItem('userToken')) {
        return (
            <div className="container" id="dashboard-container">
                <p><Link to="/login">Login here</Link> to see profile data.</p>
            </div>
        );
    }

    return (
        <div className="dashboard-container" id="dashboard-container">
            <div className="profile-card linear-gradient">
                <h2 className="text-shadow">Profile</h2>
                <p className="whiteText"><span className="text-shadow">User Name:</span> {profileData.userName}</p>
                <div className="display-name-container">
                    <p className="whiteText text-shadow">{!isEditing ? 'Display Name:' : 'New Name:'}</p>
                    {isEditing ? (
                        <>
                            <input 
                                type="text" 
                                value={newDisplayName} 
                                onChange={(e) => setNewDisplayName(e.target.value)} 
                                placeholder={profileData.displayName}
                                className="edit-input"
                            />
                            <button className="update-btn" onClick={handleUpdateClick}>Update</button>
                            {showPopup && 
                            <div className="popup">
                                <span>{popupMessage}</span>
                                <button onClick={() => setShowPopup(false)}>Close</button>
                            </div>
                            }
                        </>
                    ) : (
                        <p className="whiteText">{profileData.displayName}</p>
                    )}
                    {!isEditing && (
                        <button className="edit-btn" onClick={handleEditClick}>Edit</button>
                    )}
                </div>
                <p className="whiteText"><span className="text-shadow">Email:</span> {profileData.email}</p>
                <div className="button-container">
                    <button className="change-password-btn" onClick={handleChangePassword}>Change Password</button>
                    <button className="logout-btn" onClick={handleLogout}>Log Out</button>
                </div>
            </div>
            <div className="info-cards">
                <div className="info-card linear-gradient">
                <h2 className="text-shadow default-deck-text">Default Deck</h2>
                <div className="abilities-container-profile">
                {profileData.abilities.map((item, index) => (
                    <div key={index} className="ability-square" style={{ backgroundColor: abilityColors[item.name] }}>
                    <div className="ability-icon">
                        <img
                        src={`./assets/abilityIcons/${item.name}.png`}
                        alt={item.name}
                        className="ability-img"
                        />
                    </div>
                    <div className="ability-count">{item.count}</div>
                    </div>
                ))}
                </div>
                <div className="info-card linear-gradient">
                    <h2><span className="text-shadow elo-text">ELO:</span> <span className="elo-value">{profileData.elo}</span></h2>
                    <h2 className="text-shadow">Most Recent Ladder Game</h2>
                    {profileData.last_game ? (
                        <div className="game-history-item">
                            <p><strong>Date:</strong> {new Date(profileData.last_game.game_date).toLocaleDateString()} {new Date(profileData.last_game.game_date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</p>
                            <p><strong>Players:</strong></p>
                            <ul>
                                {profileData.last_game.players.map((player, index) => {
                                    let className = '';
                                    if (player.is_current_user) {
                                        className = player.rank === 1 ? 'current-user-win' : 'current-user-lose';
                                        }
                                    return (
                                        <li key={index} className={className}>
                                        {player.username} - Rank: {player.rank}
                                        {player.is_current_user && ' (You)'}
                                        </li>
                                    );
                                })}
                            </ul>
                        </div>
                    ) : (
                        <p>No recent games played.</p>
                    )}
                    <div className="button-container">
                        <button className="match-history-btn" onClick={handleMatchHistoryClick}>Match History</button>
                    </div>
                </div>
                {profileData.past_games.map((position, index) => (
                    <p key={index}>Game {index + 1}: {position}</p>
                ))}
            </div>
        </div>
    </div>
    );
};

export default Profile;