import React, { useState, useEffect } from 'react';
import '../../styles/style.css';

interface Ability {
    name: string;
    cost: number;
}

const DeckBuilder: React.FC = () => {
    const [abilities, setAbilities] = useState<Ability[]>([]);
    const [selectedCounts, setSelectedCounts] = useState<{ [key: string]: number }>({});

    useEffect(() => {
        const fetchAbilities = async () => {
            try {
                const response = await fetch('http://localhost:5001/abilities');
                const data = await response.json();
                if (response.ok) {
                    setAbilities(data.abilities);
                    const storedAbilities = sessionStorage.getItem('selectedAbilities');
                    if (storedAbilities) {
                        const parsedAbilities = JSON.parse(storedAbilities);
                        const initialCounts = parsedAbilities.reduce((counts: { [key: string]: number }, ability: { name: string; count: number }) => {
                            counts[ability.name] = ability.count;
                            return counts;
                        }, {});
                        setSelectedCounts(initialCounts);
                    } else {
                        const token = localStorage.getItem('userToken');
                        if (token) {
                            const userAbilitiesResponse = await fetch('http://localhost:5001/user_abilities', {
                                headers: {
                                    Authorization: `Bearer ${token}`,
                                },
                            });
                            const userAbilitiesData = await userAbilitiesResponse.json();
                            if (userAbilitiesResponse.ok) {
                                const userAbilities = userAbilitiesData.abilities;
                                const initialCounts = userAbilities.reduce((counts: { [key: string]: number }, ability: { name: string; count: number }) => {
                                    counts[ability.name] = ability.count;
                                    return counts;
                                }, {});
                                setSelectedCounts(initialCounts);
                                sessionStorage.setItem('selectedAbilities', JSON.stringify(userAbilities));
                            } else {
                                setSelectedCounts(data.abilities.reduce((counts: { [key: string]: number }, ability: Ability) => {
                                    counts[ability.name] = 0;
                                    return counts;
                                }, {}));
                            }
                        } else {
                            setSelectedCounts(data.abilities.reduce((counts: { [key: string]: number }, ability: Ability) => {
                                counts[ability.name] = 0;
                                return counts;
                            }, {}));
                        }
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

    const handleButtonClick = (abilityName: string, increment: boolean) => {
        setSelectedCounts(prevCounts => {
            const newCounts = {
                ...prevCounts,
                [abilityName]: Math.max((prevCounts[abilityName] || 0) + (increment ? 1 : -1), 0),
            };
    
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
                        onContextMenu={(e) => {
                            e.preventDefault();
                            handleButtonClick(ability.name, false);
                        }}
                    >
                        <div className="ability-name">{ability.name}</div>
                        <div className="ability-cost">Cost: {ability.cost}</div>
                        <div className="ability-count">{selectedCounts[ability.name] || 0}</div>
                    </button>
                ))}
            </div>
        </div>
    );
};

export default DeckBuilder;