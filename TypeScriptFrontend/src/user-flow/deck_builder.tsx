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
    const [selectedBasicCounts, setSelectedBasicCounts] = useState<{ [key: string]: number }>({});
    const [initialSalary, setInitialSalary] = useState(0); // Store the initial salary
    const [salary, setSalary] = useState(0);
    const [experimentalOptionCount, setExperimentalOptionCount] = useState(3);
    const [basicOptionCount, setBasicOptionCount] = useState(3);
    const [error, setError] = useState("");
    const [royalAbilities, setRoyalAbilities] = useState<Ability[]>([]);
    const [deckMode, setDeckMode] = useState<string>(
        sessionStorage.getItem("gameMode") || "Experimental"
    );
    
    useEffect(() => {
        const fetchBasicAbilities = async () => {
            if (isTokenValid === false) return;
            try {
                const response = await fetch(`${config.userBackend}/abilities/Basic`);
                const data = await response.json();
                if (!sessionStorage.getItem("selectedBasicAbilities")) {
                    handleGetDeck();
                }
                if (response.ok) {
                    setRoyalAbilities(data.abilities);
                    setBasicOptionCount(data.options);
                    const storedBasicAbilities = sessionStorage.getItem("selectedBasicAbilities");
                    if (storedBasicAbilities) {
                        const parsedAbilities = JSON.parse(storedBasicAbilities);
                        const initialCounts = parsedAbilities.reduce((counts: {[key: string]: number}, ability: { name: string; count: number }) => {
                            counts[ability.name] = ability.count;
                            return counts;
                        }, {});
                        setSelectedBasicCounts(initialCounts);
                    }
                } else {
                    throw new Error(data.message);
                }
            } catch (error) {
                console.error('Error fetching abilities:', error);
            }
        };
        fetchBasicAbilities();
    }, [isTokenValid]);

    useEffect(() => {
        const fetchAbilities = async () => {
            if (isTokenValid === false) return;
            try {
                const response = await fetch(`${config.userBackend}/abilities/Experimental`);
                const data = await response.json();
                if (!sessionStorage.getItem("selectedExperimentalAbilities")) {
                    handleGetDeck();
                }
                if (response.ok) {
                    setAbilities(data.abilities);
                    setInitialSalary(data.credits);
                    setExperimentalOptionCount(data.options);
                    const storedExperimentalAbilities = sessionStorage.getItem("selectedExperimentalAbilities");
                    if (storedExperimentalAbilities) {
                        const parsedAbilities = JSON.parse(storedExperimentalAbilities);
                        const initialCounts = parsedAbilities.reduce((counts: {[key: string]: number}, ability: { name: string; count: number }) => {
                            counts[ability.name] = ability.count;
                            return counts;
                        }, {});
                        setSelectedCounts(initialCounts);
                    }
                } else {
                    throw new Error(data.message);
                }
            } catch (error) {
                console.error('Error fetching abilities:', error);
            }
        };
        fetchAbilities();
    }, [isTokenValid]);

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
        if (deckMode === "Experimental") {
            setSelectedCounts(abilities.reduce((counts: { [key: string]: number }, ability: Ability) => {
                counts[ability.name] = 0;
                return counts;
            }, {}));
            setSalary(abilities.reduce((total, ability) => total + (ability.cost * 0), salary)); // Reset salary to full amount
            sessionStorage.setItem('selectedExperimentalAbilities', JSON.stringify({ abilities: []}));
        }
        else {
            setSelectedBasicCounts(abilities.reduce((counts: { [key: string]: number }, ability: Ability) => {
                counts[ability.name] = 0;
                return counts;
            }, {}));
            sessionStorage.setItem('selectedBasicAbilities', JSON.stringify({ abilities: []}));
        }
    };

    const handleSaveDeck = async () => {
        setError("");
        const token = localStorage.getItem('userToken');
        if (token) {
            let selectedAbilities;
            if (deckMode === "Experimental") {
                selectedAbilities = Object.entries(selectedCounts)
                    .filter(([, count]) => count > 0)
                    .map(([name, count]) => ({ name, count }));
            } else {
                selectedAbilities = Object.entries(selectedBasicCounts)
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
            } catch (error) {
                console.error('Error saving deck:', error);
            }
        }
    };


    const handleGetDeck = async () => {
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
                    const experimentalDeckIndex = modes.findIndex((mode: string) => mode === "Experimental");
                    const basicDeckIndex = modes.findIndex((mode: string) => mode === "Basic");
                    const newDecks: any[][] = fetchedDecks.map((deck: any[]) => deck.slice(0, -1));
                    
                    if (experimentalDeckIndex !== -1) {
                        const experimentalInitialCounts = newDecks[experimentalDeckIndex].reduce((counts: { [key: string]: number }, ability: {name: string; count: number}) => {
                            counts[ability.name] = ability.count;
                            return counts;
                        }, {});
                        setSelectedCounts(experimentalInitialCounts);
                        sessionStorage.setItem("selectedExperimentalAbilities", JSON.stringify(newDecks[experimentalDeckIndex]));
                    }
                    
                    if (basicDeckIndex !== -1) {
                        const basicInitialCounts = newDecks[basicDeckIndex].reduce((counts: { [key: string]: number }, ability: {name: string; count: number}) => {
                            counts[ability.name] = ability.count;
                            return counts;
                        }, {});
                        setSelectedBasicCounts(basicInitialCounts);
                        sessionStorage.setItem("selectedBasicAbilities", JSON.stringify(newDecks[basicDeckIndex]));
                    }
                } else {
                    throw new Error(data.message);
                }
            } catch (error) {
                console.error('Error fetching decks:', error);
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
            if (increment && newCount === 1 && distinctAbilities >= experimentalOptionCount) {
                setError("You cannot select more than ${experimentalOptionCount} distinct abilities.");
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

            const selectedAbilities = Object.entries(newCounts)
                .filter(([, count]) => count > 0)
                .map (([name, count]) => ({ name, count}));

            sessionStorage.setItem('selectedExperimentalAbilities', JSON.stringify(selectedAbilities));

            return newCounts;
        });
    };

    const handleBasicButtonClick = (abilityName: string, increment: boolean) => {
        setError(""); // Clear previous errors
        setSelectedBasicCounts(prevCounts => {
            const abilityCost = abilities.find(a => a.name === abilityName)?.cost || 0;
            const currentCount = prevCounts[abilityName] || 0;
    
            // Prevent decrementing below zero
            if (!increment && currentCount === 0) {
                return prevCounts; // Return early if trying to decrement an ability at zero
            }
    
            const newCount = increment ? currentCount + 1 : Math.max(currentCount - 1, 0);
            const distinctAbilities = Object.keys(prevCounts).filter(name => prevCounts[name] > 0).length;
    
            // Check if adding a new distinct ability and already at max
            if (increment && newCount === 1 && distinctAbilities >= basicOptionCount) {
                setError(`You cannot select more than ${basicOptionCount} distinct abilities.`);
                return prevCounts;
            }

            if (increment && newCount === 2) {
                setError("You can only select an ability once in Basic decks.");
                return prevCounts;
            }
    
            // Check if salary allows for this increment
            // no salary in basic
            /*if (increment && (salary - abilityCost < 0)) {
                setError(`You cannot afford the ${abilityName} ability.`);
                return prevCounts;
            }*/
    
            const newCounts = {
                ...prevCounts,
                [abilityName]: newCount
            };
            const selectedAbilities = Object.entries(newCounts)
                .filter(([, count]) => count > 0)
                .map (([name, count]) => ({ name, count}));
            
            sessionStorage.setItem('selectedBasicAbilities', JSON.stringify(selectedAbilities));

            return newCounts;
        });
    };

    const getCurrentSelections = () => {
        if (deckMode === "Experimental") {
            return Object.entries(selectedCounts)
                .filter(([, count]) => count > 0)
                .map(([name, count]) => ({ name, count }));
        } else {
            return Object.entries(selectedBasicCounts)
                .filter(([, count]) => count > 0)
                .map(([name, count]) => ({ name, count }));
        }
    };

    const handleGameModeChange = (mode: string) => {
        setDeckMode(mode);
        sessionStorage.setItem("gameMode", mode);
    };

    const gridClassName = `ability-grid ${deckMode === "Experimental" ? "experimental-mode" : "basic-mode"}`;

    return (
        <div className="container" id="deck-builder-container">
            <h1>Deck Builder</h1>
            <div className="tab-and-salary-container">
                <div className="deck-tab-container">
                    <button 
                        className={`tab-button ${deckMode === "Basic" ? "active" : ""}`}
                        onClick={() => handleGameModeChange("Basic")}
                    >
                        Basic
                    </button>
                    <button 
                        className={`tab-button ${deckMode === "Experimental" ? "active" : ""}`}
                        onClick={() => handleGameModeChange("Experimental")}
                    >
                        Experimental
                    </button>
                </div>
                {deckMode === "Experimental" && (
                    <div className="salary-display">
                        <h2>Credits: {salary}</h2>
                    </div>
                )}
            </div>
            <div className={gridClassName}>
                {(deckMode === "Experimental" ? abilities : royalAbilities).map((ability, index) => (
                    <button
                    key={index}
                    className={`ability-button ${(deckMode === "Experimental" ? selectedCounts : selectedBasicCounts)[ability.name] > 0 ? 'selected' : ''}`}
                    onClick={() => deckMode === "Experimental" ? handleButtonClick(ability.name, true) : handleBasicButtonClick(ability.name, true)}
                    data-tooltip={ability.description}
                    onContextMenu={(e) => {
                        e.preventDefault();
                        deckMode === "Experimental" ? handleButtonClick(ability.name, false) : handleBasicButtonClick(ability.name, false);
                    }}
                    >
                    <img 
                        src={`./assets/abilityIcons/${ability.name}.png`} 
                        alt={ability.name} 
                        style={{ width: '70%', height: 'auto', marginBottom: '15%' }}
                    />
                    <div className="ability-name">{ability.name}</div>
                    <div className="ability-cost">Cost: {ability.cost}</div>
                    <div className="ability-count">
                        {(deckMode === "Experimental" ? selectedCounts : selectedBasicCounts)[ability.name] || 0}
                    </div>
                    </button>
                ))}
            </div>
            <div className="button-container">
                <div className="button-row">
                    <button className="custom-button start-fresh-button" data-tooltip="Reset current selections" onClick={handleStartFresh}>Start Fresh</button>
                    {localStorage.getItem('userToken') && (
                        <>
                            <button className="custom-button save-button" data-tooltip="Update your default deck" onClick={handleSaveDeck}>Save</button>
                            <button className="custom-button my-deck-button" data-tooltip="Select your saved deck" onClick={handleGetDeck}>My Deck</button>
                        </>
                    )}
                </div>
                <button className="custom-button ready-button" data-tooltip="Go to the home page" onClick={goHome}>Ready</button>
                {error && <p className="error-message">{error}</p>}
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
                {/* <h2 style={{ marginTop: '20px' }}>Selected abilities:</h2> */}
                <div className="abilities-container-friendly">
                    {/* {getCurrentSelections().length > 0 ? (
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
                    )} */}
                    {getCurrentSelections().length == 0 && (<p>No abilities selected for {deckMode} mode</p>)}
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
