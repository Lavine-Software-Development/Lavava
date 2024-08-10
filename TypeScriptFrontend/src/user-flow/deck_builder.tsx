import React, { useState, useEffect } from 'react';
import '../../styles/style.css';
import config from '../env-config';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import { abilityColors } from "../user-flow/ability_utils";

interface Ability {
    description: string;
    name: string;
    cost: number;
}

const DeckBuilder: React.FC = () => {
    const navigate = useNavigate();
    const [isTokenValid, setIstokenValid] = useState<boolean | null>(null);
    const [showPopup, setShowPopup] = useState(false);

    // check if login token has expired
    useEffect(() => {
        const validateToken = () => {
            const token = localStorage.getItem("userToken");
            if (!token){
                return;
            }

            try {
                const decodedToken = jwtDecode(token);
                const currentTime = Date.now() / 1000; // convert to seconds
                if (decodedToken.exp < currentTime) {
                    localStorage.removeItem("userToken");
                    setIstokenValid(false);
                    navigate("/login");
                } else {
                    setIstokenValid(true);
                }
            } catch (error) {
                console.error("Error decoding token:", error);
                localStorage.removeItem("userToken");
                setIstokenValid(false);
                navigate("/login");
            }
        };

        validateToken();
    }, []);

    const [abilities, setAbilities] = useState<Ability[]>([]);
    const [selectedCounts, setSelectedCounts] = useState<{ [key: string]: number }>({});
    const [selectedRoyaleCounts, setSelectedRoyaleCounts] = useState<{ [key: string]: number }>({});
    const [initialSalary, setInitialSalary] = useState(0); // Store the initial salary
    const [salary, setSalary] = useState(0); 
    const [error, setError] = useState("");
    const [royalAbilities, setRoyalAbilities] = useState<Ability[]>([]);
    const [deckMode, setDeckMode] = useState<string>("Original");
    const [deckIndex, setDeckIndex] = useState<number>(0);
    const [usersDecks, setUsersDecks] = useState<any[][]>([]);
    const [decks, setDecks] = useState<any[][]>([]);
    
    useEffect(() => {
        const fetchRoyaleAbilities = async () => {
            if (isTokenValid === false) return;
            handleGetDecks();
            try {
                const response = await fetch(`${config.userBackend}/abilities/Royale`);
                const data = await response.json();
                if (response.ok) {
                    setRoyalAbilities(data.abilities);
                } else {
                    throw new Error(data.message);
                }
            } catch (error) {
                console.error('Error fetching abilities:', error);
            }
        };
        fetchRoyaleAbilities();
    }, []);

    useEffect(() => {
        const fetchAbilities = async () => {
            if (isTokenValid === false) return;
            try {
                const response = await fetch(`${config.userBackend}/abilities/Original`);
                const data = await response.json();
                if (response.ok) {
                    setAbilities(data.abilities);
                    setInitialSalary(data.salary);
                } else {
                    throw new Error(data.message);
                }
            } catch (error) {
                console.error('Error fetching abilities:', error);
            }
        };
        fetchAbilities();
    }, []);

    useEffect(() => {
        // This effect recalculates the salary whenever selectedCounts changes
        const totalCost = Object.entries(selectedCounts).reduce((total, [name, count]) => {
            const abilityCost = abilities.find(a => a.name === name)?.cost || 0;
            return total + abilityCost * count;
        }, 0);
        setSalary(initialSalary - totalCost); // Update the salary based on the total cost
    }, [selectedCounts, abilities, initialSalary]);

    const handleStartFresh = () => {
        setError("");
        setSelectedCounts(abilities.reduce((counts: { [key: string]: number }, ability: Ability) => {
            counts[ability.name] = 0;
            return counts;
        }, {}));
        setSelectedRoyaleCounts(abilities.reduce((counts: { [key: string]: number }, ability: Ability) => {
            counts[ability.name] = 0;
            return counts;
        }, {}));
        setSalary(abilities.reduce((total, ability) => total + (ability.cost * 0), salary)); // Reset salary to full amount
    };

    const handleSaveDeck = async () => {
        setError("");
        const token = localStorage.getItem('userToken');
        if (token) {
            let selectedAbilities;
            if (deckMode === "Original") {
                selectedAbilities = Object.entries(selectedCounts)
                    .filter(([, count]) => count > 0)
                    .map(([name, count]) => ({ name, count }));
            } else {
                selectedAbilities = Object.entries(selectedRoyaleCounts)
                    .filter(([, count]) => count > 0)
                    .map(([name, count]) => ({ name, count }));
            }

            try {
                // Make a dummy backend call to save the user's deck
                await fetch(`${config.userBackend}/save_deck`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({ abilities: selectedAbilities, mode: deckMode }),
                });
                setShowPopup(true);
                setTimeout(() => {
                    setShowPopup(false);
                }, 1000);
                handleGetDecks();
            } catch (error) {
                console.error('Error saving deck:', error);
            }
        }
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
    

    const handleGetDecks = async () => {
        const token = localStorage.getItem('userToken');
        if (token) {
            try {
                const response = await fetch(`${config.userBackend}/user_abilities`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                const data = await response.json();
                if (response.ok) {
                    const fetchedDecks: any[][] = data.decks || [];
                    const modes = fetchedDecks.map((deck: any[]) => deck[deck.length - 1]);
                    const newDeckIndex = modes.findIndex((mode: string) => mode === deckMode);
                    const newDecks: any[][] = fetchedDecks.map((deck: any[]) => deck.slice(0, -1));
                    setDeckIndex(newDeckIndex);
                    setUsersDecks(newDecks);
                    setDecks(fetchedDecks);
                } else {
                    throw new Error(data.message);
                }
            } catch (error) {
                console.error('Error fetching decks:', error);
                setUsersDecks([]); // Set to empty array in case of error
            }
        }
    };

    const goHome = () => {
        navigate('/home');
    };

    const handleButtonClick = (abilityName: string, increment: boolean) => {
        setError(""); // Clear previous errors
        setSelectedCounts(prevCounts => {
            const abilityCost = abilities.find(a => a.name === abilityName)?.cost || 0;
            const currentCount = prevCounts[abilityName] || 0;
    
            // Prevent decrementing below zero
            if (!increment && currentCount === 0) {
                return prevCounts; // Return early if trying to decrement an ability at zero
            }
    
            const newCount = increment ? currentCount + 1 : Math.max(currentCount - 1, 0);
            const distinctAbilities = Object.keys(prevCounts).filter(name => prevCounts[name] > 0).length;
    
            // Check if adding a new distinct ability and already at max
            if (increment && newCount === 1 && distinctAbilities >= 4) {
                setError("You cannot select more than 4 distinct abilities.");
                return prevCounts;
            }
    
            // Check if salary allows for this increment
            if (increment && (salary - abilityCost < 0)) {
                setError(`You cannot afford the ${abilityName} ability.`);
                return prevCounts;
            }
    
            const newCounts = {
                ...prevCounts,
                [abilityName]: newCount
            };
            return newCounts;
        });
    };

    const handleRoyaleButtonClick = (abilityName: string, increment: boolean) => {
        setError(""); // Clear previous errors
        setSelectedRoyaleCounts(prevCounts => {
            const abilityCost = abilities.find(a => a.name === abilityName)?.cost || 0;
            const currentCount = prevCounts[abilityName] || 0;
    
            // Prevent decrementing below zero
            if (!increment && currentCount === 0) {
                return prevCounts; // Return early if trying to decrement an ability at zero
            }
    
            const newCount = increment ? currentCount + 1 : Math.max(currentCount - 1, 0);
            const distinctAbilities = Object.keys(prevCounts).filter(name => prevCounts[name] > 0).length;
    
            // Check if adding a new distinct ability and already at max
            if (increment && newCount === 1 && distinctAbilities >= 4) {
                setError("You cannot select more than 4 distinct abilities.");
                return prevCounts;
            }

            if (increment && newCount === 2) {
                setError("You can select an ability once in Royale decks.");
                return prevCounts;
            }
    
            // Check if salary allows for this increment
            if (increment && (salary - abilityCost < 0)) {
                setError(`You cannot afford the ${abilityName} ability.`);
                return prevCounts;
            }
    
            const newCounts = {
                ...prevCounts,
                [abilityName]: newCount
            };
            return newCounts;
        });
    };

    const getCurrentSelections = () => {
        if (deckMode === "Original") {
            return Object.entries(selectedCounts)
                .filter(([, count]) => count > 0)
                .map(([name, count]) => ({ name, count }));
        } else {
            return Object.entries(selectedRoyaleCounts)
                .filter(([, count]) => count > 0)
                .map(([name, count]) => ({ name, count }));
        }
    };

    return (
        <div className="container" id="deck-builder-container">
            <h1>Deck Builder</h1>
            <div className="tab-container">
                <button 
                    className={`tab-button ${deckMode === "Original" ? "active" : ""}`}
                    onClick={() => setDeckMode("Original")}
                >
                    Original
                </button>
                <button 
                    className={`tab-button ${deckMode === "Royale" ? "active" : ""}`}
                    onClick={() => setDeckMode("Royale")}
                >
                    Royale
                </button>
            </div>
            <div className="ability-grid">
                {(deckMode === "Original" ? abilities : royalAbilities).map((ability, index) => (
                    <button
                        key={index}
                        className={`ability-button ${(deckMode === "Original" ? selectedCounts : selectedRoyaleCounts)[ability.name] > 0 ? 'selected' : ''}`}
                        onClick={() => deckMode === "Original" ? handleButtonClick(ability.name, true) : handleRoyaleButtonClick(ability.name, true)}
                        data-tooltip={ability.description}
                        onContextMenu={(e) => {
                            e.preventDefault();
                            deckMode === "Original" ? handleButtonClick(ability.name, false) : handleRoyaleButtonClick(ability.name, false);
                        }}
                    >
                        <img src={`./assets/abilityIcons/${ability.name}.png`} alt={ability.name} 
                        style={{ width: '70%', height: 'auto', marginBottom: '15%' }}/>
                        <div className="ability-name">{ability.name}</div>
                        {deckMode === "Original" && <div className="ability-cost">Cost: {ability.cost}</div>}
                        <div className="ability-count">{(deckMode === "Original" ? selectedCounts : selectedRoyaleCounts)[ability.name] || 0}</div>
                    </button>
                ))}
            </div>
            <div className="button-container">
                <div className="button-row">
                    <button className="custom-button start-fresh-button" data-tooltip="Reset current selections" onClick={handleStartFresh}>Start Fresh</button>
                    {localStorage.getItem('userToken') && (
                        <>
                            <button className="custom-button save-button" data-tooltip="Update your default deck" onClick={handleSaveDeck}>Save</button>
                        </>
                    )}
                </div>
                <button className="custom-button ready-button" data-tooltip="Go to the home page" onClick={goHome}>Ready</button>
                {error && <p className="error-message">{error}</p>}
                {deckMode === "Original" && (
                    <div className="salary-display">
                        <h2>Credits: {salary}</h2>
                    </div>
                )}
                <div className="click-instructions">
                    <span className="click-instruction">
                        <img src="/assets/left_click.png" alt="Left click" className="click-icon" />
                        Select
                    </span>
                    <span className="click-instruction">
                        <img src="/assets/right_click.png" alt="Right click" className="click-icon" />
                        Deselect
                    </span>
                </div>
                <h2 style={{ marginTop: '20px' }}>Selected abilities:</h2>
                <div className="abilities-container-friendly">
                    {getCurrentSelections().length > 0 ? (
                        getCurrentSelections().map((item, index) => (
                            <div key={index} className="ability-square" style={{ backgroundColor: abilityColors[item.name] , width: '100px', height: '100px'}}>
                                <div className="ability-icon">
                                    <img
                                        src={`./assets/abilityIcons/${item.name}.png`}
                                        alt={item.name}
                                        className="ability-img"
                                    />
                                </div>
                                <div className="ability-count" style={{fontSize: '1.2rem'}}>{item.count}</div>
                            </div>
                        ))
                    ) : (
                        <p>No abilities selected for {deckMode} mode</p>
                    )}
                </div>
                <h2 style={{ marginTop: '20px' }}>Your {deckMode} Mode Deck:</h2>
                <div className="abilities-container-friendly">
                {usersDecks && usersDecks[deckIndex] ? (
                    usersDecks[deckIndex].length > 0 ? (
                        usersDecks[deckIndex].map((item: { name: string; count: number }, index: number) => (
                            <div key={index} className="ability-square" style={{ backgroundColor: abilityColors[item.name], width: '100px', height: '100px' }}>
                                <div className="ability-icon">
                                    <img
                                        src={`./assets/abilityIcons/${item.name}.png`}
                                        alt={item.name}
                                        className="ability-img"
                                    />
                                </div>
                                <div className="ability-count" style={{fontSize: '1.2rem'}}>{item.count}</div>
                            </div>
                        ))
                    ) : (
                        <p>You have no saved abilities for {deckMode} mode</p>
                    )
                ) : (
                    <p>Loading your deck...</p>
                )}
                </div>
            </div>
            {showPopup && (
                <div className="popup">
                    Deck saved successfully!
                </div>
            )}
        </div>
    );
};

export default DeckBuilder;
