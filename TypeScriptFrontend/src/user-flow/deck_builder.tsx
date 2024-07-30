import React, { useState, useEffect } from 'react';
import '../../styles/style.css';
import config from '../env-config';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';

interface Ability {
    description: string;
    name: string;
    cost: number;
}

const DeckBuilder: React.FC = () => {
    const navigate = useNavigate();
    const [isTokenValid, setIstokenValid] = useState<boolean | null>(null);

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
                    navigate("/login")
                } else {
                    setIstokenValid(true);
                }
            } catch (error) {
                console.error("Error deccoding token:", error);
                localStorage.removeItem("userToken");
                setIstokenValid(false);
                navigate("/login")
            }
        };

        validateToken();
    }, []);

    const [abilities, setAbilities] = useState<Ability[]>([]);
    const [selectedCounts, setSelectedCounts] = useState<{ [key: string]: number }>({});
    const [initialSalary, setInitialSalary] = useState(0); // Store the initial salary
    const [salary, setSalary] = useState(0); 
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchAbilities = async () => {
            if (isTokenValid === false) return;
            try {
                const response = await fetch(`${config.userBackend}/abilities`);
                const data = await response.json();
                if (response.ok) {
                    setAbilities(data.abilities);
                    setInitialSalary(data.salary);
                    const storedAbilities = sessionStorage.getItem('selectedAbilities');
                    if (storedAbilities) {
                        const parsedAbilities = JSON.parse(storedAbilities);
                        const initialCounts = parsedAbilities.reduce((counts: { [key: string]: number }, ability: { name: string; count: number }) => {
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
        setSelectedCounts(abilities.reduce((counts: { [key: string]: number }, ability: Ability) => {
            counts[ability.name] = 0;
            return counts;
        }, {}));
        sessionStorage.setItem('selectedAbilities', JSON.stringify({ abilities: [] }));
        setSalary(abilities.reduce((total, ability) => total + (ability.cost * 0), salary)); // Reset salary to full amount
    };

    const handleSaveDeck = async () => {
        const token = localStorage.getItem('userToken');
        if (token) {
            const selectedAbilities = Object.entries(selectedCounts)
                .filter(([, count]) => count > 0)
                .map(([name, count]) => ({ name, count }));

            try {
                // Make a dummy backend call to save the user's deck
                await fetch(`${config.userBackend}/save_deck`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({ abilities: selectedAbilities }),
                });
            } catch (error) {
                console.error('Error saving deck:', error);
            }
        }
    };

    const handleResetDeck = async () => {
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
                    const userAbilities = data.abilities;
                    const initialCounts = userAbilities.reduce((counts: { [key: string]: number }, ability: { name: string; count: number }) => {
                        counts[ability.name] = ability.count;
                        return counts;
                    }, {});
                    setSelectedCounts(initialCounts);
                    sessionStorage.setItem('selectedAbilities', JSON.stringify(userAbilities));
                } else {
                    throw new Error(data.message);
                }
            } catch (error) {
                console.error('Error resetting deck:', error);
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
    
            // Update session storage
            const selectedAbilities = Object.entries(newCounts)
                .filter(([, count]) => count > 0)
                .map(([name, count]) => ({ name, count }));
            sessionStorage.setItem('selectedAbilities', JSON.stringify(selectedAbilities));
    
            return newCounts;
        });
    };
    
    

    return (
        <div className="container" id="deck-builder-container">
            <h1>Deck Builder</h1>
            <div className="ability-grid">
                {abilities.map((ability, index) => (
                    <button
                        key={index}
                        className={`ability-button ${selectedCounts[ability.name] > 0 ? 'selected' : ''}`}
                        onClick={() => handleButtonClick(ability.name, true)}
                        data-tooltip = {ability.description}
                        onContextMenu={(e) => {
                            e.preventDefault();
                            handleButtonClick(ability.name, false);
                        }}
                    >
                        {/* icon in background 
                        <div style={{zIndex: 0, opacity: 0.25}}>
                            <img src={`./assets/abilityIcons/${ability.name}.png`} alt={ability.name} 
                            style={{objectFit: 'contain', width: '90%', height: '90%'}}/>
                        </div>

                        <div style={{position: 'absolute', zIndex: 1}}>
                            <div className="ability-name">{ability.name}</div>
                            <div className="ability-cost">Cost: {ability.cost}</div>
                            <div className="ability-count">{selectedCounts[ability.name] || 0}</div>
                        </div>*/}

                        {/* icon placement on top of text */}
                        <img src={`./assets/abilityIcons/${ability.name}.png`} alt={ability.name} 
                        style={{ width: '70%', height: '50%', objectFit: 'contain', marginBottom: '15%'}}/>

                        <div className="ability-name">{ability.name}</div>
                        <div className="ability-cost">Cost: {ability.cost}</div>
                        <div className="ability-count">{selectedCounts[ability.name] || 0}</div>
                    </button>
                ))}
            </div>
            <div className="button-container">
                <div className="button-row">
                    <button className="custom-button start-fresh-button" data-tooltip="Reset current selections" onClick={handleStartFresh}>Start Fresh</button>
                    {localStorage.getItem('userToken') && (
                        <>
                            <button className="custom-button save-button" data-tooltip="Update your default deck" onClick={handleSaveDeck}>Save</button>
                            <button className="custom-button my-deck-button" data-tooltip="Use your default deck" onClick={handleResetDeck}>My Deck</button>
                        </>
                    )}
                </div>
                <button className="custom-button ready-button" data-tooltip="Go to the home page" onClick={goHome}>Ready</button>
                {error && <p className="error-message">{error}</p>}
                <div className="salary-display">
                    <h2>Credits: {salary}</h2>
                </div>
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
            </div>
        </div>
    );
};

export default DeckBuilder;
