import React, { useState, useEffect } from 'react';
import '../../styles/style.css';
import { Link, useNavigate } from 'react-router-dom';
import config from '../env-config';
import { abilityColors } from "../user-flow/ability_utils";

interface PlayerData {
    username: string;
    rank: number;
    is_current_user: boolean;
    elo_change: number;
}

interface GameData {
    game_id: number;
    game_date: string;
    players: PlayerData[];
}

interface UserSettings {
    auto_attack: boolean;
    auto_spread: boolean;
    popups: boolean;
}

interface ProfileData {
    userName: string;
    displayName: string;
    email: string;
    decks: any[][];
    elo: number;
    last_game: GameData | null;
}

const Profile: React.FC = () => {
    const navigate = useNavigate();
    const [profileData, setProfileData] = useState<ProfileData>({
        userName: 'Loading...',
        displayName: 'Loading...',
        email: 'Loading...',
        decks: [[]], // Default to at least one empty list
        elo: 1000,
        last_game: null,
    });

    const [userSettings, setUserSettings] = useState<UserSettings>({
        auto_attack: false,
        auto_spread: false,
        popups: true,
    });

    const [isEditing, setIsEditing] = useState(false);
    const [newDisplayName, setNewDisplayName] = useState(profileData.displayName);
    const [popupMessage, setPopupMessage] = useState('');
    const [showPopup, setShowPopup] = useState(false);
    const [deckMode, setDeckMode] = useState("Basic");
    const [deckIndex, setDeckIndex] = useState<number>(0);
    const [usersDecks, setUsersDecks] = useState<any[][]>([]);
    const [decks, setDecks] = useState<any[][]>([]);

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

    const fetchUserSettings = async () => {
        const token = localStorage.getItem('userToken');
        try {
            const response = await fetch(`${config.userBackend}/frontend_get_user_settings`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });
            const data = await response.json();
            if (response.ok) {
                setUserSettings(data);
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            console.error('Error fetching user settings:', error);
        }
    };

    const updateUserSetting = async (setting: keyof UserSettings) => {
        const token = localStorage.getItem('userToken');
        try {
            const response = await fetch(`${config.userBackend}/update_user_settings`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ [setting]: !userSettings[setting] })
            });
            if (response.ok) {
                setUserSettings(prev => ({ ...prev, [setting]: !prev[setting] }));
            } else {
                throw new Error('Failed to update setting');
            }
        } catch (error) {
            console.error('Error updating user setting:', error);
        }
    };

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
                await fetchUserSettings();
                if (response.ok) {
                    setProfileData(data);
                    const fetchedDecks: any[][] = data.usersDecks || [];
                    const modes = fetchedDecks.map((deck: any[]) => deck[deck.length - 1]);
                    const newDeckIndex = modes.findIndex((mode: string) => mode === deckMode);
                    const newDecks: any[][] = fetchedDecks.map((deck: any[]) => deck.slice(0, -1));
                    setDeckIndex(newDeckIndex);
                    setUsersDecks(newDecks);
                    setDecks(fetchedDecks);
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

    useEffect(() => {
        handleMyDeck();
        console.log(profileData.last_game);
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
                <div className="user-settings">
                    <p className="whiteText"><h3 className="text-shadow">User Settings</h3></p>
                    <div className="setting-toggle">
                    <p className="whiteText"><span  className="text-shadow">Auto Attack:</span></p>
                        <label className="switch">
                            <input
                                type="checkbox"
                                checked={userSettings.auto_attack}
                                onChange={() => updateUserSetting('auto_attack')}
                            />
                            <span className="slider"></span>
                        </label>
                    </div>
                    <div className="setting-toggle">
                    <p className="whiteText"><span  className="text-shadow">Auto Spread:</span></p>
                        <label className="switch">
                            <input
                                type="checkbox"
                                checked={userSettings.auto_spread}
                                onChange={() => updateUserSetting('auto_spread')}
                            />
                            <span className="slider"></span>
                        </label>
                    </div>
                    <div className="setting-toggle">
                    <p className="whiteText"><span  className="text-shadow">Popups:</span></p>
                        <label className="switch">
                            <input
                                type="checkbox"
                                checked={userSettings.popups}
                                onChange={() => updateUserSetting('popups')}
                            />
                            <span className="slider"></span>
                        </label>
                    </div>
                </div>
                <div className="button-container">
                    <button className="change-password-btn" onClick={handleChangePassword}>Change Password</button>
                    <button className="logout-btn" onClick={handleLogout}>Log Out</button>
                </div>
            </div>
            <div className="info-cards">
                <div className="info-card linear-gradient">
                    <div className="tab-container" style={{ marginBottom: '10px'}}>
                        <button
                            className={`tab-blue-background-button ${deckMode === "Basic" ? "active" : ""}`}
                            onClick={() => setDeckMode("Basic")}
                        >
                            Basic
                        </button>
                        <button
                            className={`tab-blue-background-button ${deckMode === "Experimental" ? "active" : ""}`}
                            onClick={() => setDeckMode("Experimental")}
                        >
                            Experimental
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
                            <div className="no-abilities-message" style = {{margin: "0px"}}>
                                No Abilities Saved for {deckMode} mode.
                            </div>
                        )
                    ) : (
                        <p>Loading your deck...</p>
                    )}
                    </div>
                </div>
                    <div className="info-card linear-gradient">
                        <h2><span className="text-shadow elo-text">ELO:</span> <span className="elo-value">{profileData.elo}</span></h2>
                        <h2 className="text-shadow">Most Recent Ladder Game</h2>
                        {profileData.last_game ? (
                            <div className="game-history-item">
                                <p>
                                    <strong>Date:</strong>{" "}
                                    {new Date(profileData.last_game.game_date + "Z").toLocaleString([], {
                                        year: "numeric",
                                        month: "long",
                                        day: "numeric",
                                        hour: "2-digit",
                                        minute: "2-digit",
                                        hour12: true,
                                    })}
                                </p>
                                <p><strong>Players:</strong></p>
                                <ul>
                                    {profileData.last_game.players.map((player, index) => {
                                        let className = '';
                                        if (player.is_current_user) {
                                            className = player.elo_change > 0 || player.rank == 1 ? 'current-user-win' : 'current-user-lose';
                                        }
                                        return (
                                            <li key={index} className={className}>
                                                {player.rank} {player.username} 
                                                {player.elo_change != null &&
                                                ', ELO: ' + 
                                                    (Number(player.elo_change) > 0 
                                                    ? `+${player.elo_change}` 
                                                    : player.elo_change)
                                                }
                                            </li>
                                        );
                                    })}
                                </ul>
                            </div>
                        ) : (
                            <p>No recent games played.</p>
                        )}
                        <div className="match-history-btn-container">
                            <button className="match-history-btn" onClick={handleMatchHistoryClick}>Match History</button>
                        </div>
                    </div>
                </div>
            </div>
    );
};

export default Profile;