import "../../styles/style.css";
import React, { useState } from "react";
import abilityColors from "./ability_utils";

const lightenColor = (color: string, percent: number) => {
    let r: number, g: number, b: number;

    // Extract RGB values from color
    [r, g, b] = color.match(/\d+/g)!.map(Number);

    // Calculate the lightened color
    r = Math.min(255, Math.floor(r + (255 - r) * percent));
    g = Math.min(255, Math.floor(g + (255 - g) * percent));
    b = Math.min(255, Math.floor(b + (255 - b) * percent));

    return `rgb(${r}, ${g}, ${b})`;
};

type AbilityProps = {
    title: string;
    desc: string;
    extra: string;
    usage: string;
    image: string;
    onClick: () => void;
    colour: string;
    reusable: boolean;
    secondaryAbility: string | null;
};

const Ability: React.FC<AbilityProps> = ({ title, desc, extra, usage, image, onClick, colour, reusable, secondaryAbility }) => {
    const [showDropdown, setShowDropdown] = useState<boolean>(false);

    const handleMouseEnter = () => setShowDropdown(true);
    const handleMouseLeave = () => setShowDropdown(false);

    return (
        <div
            className="HtPability-window"
            onClick={onClick}
            style={{
                '--ability-color': colour,
                borderColor: colour,
                backgroundColor: `${colour}1A`,
                background: `linear-gradient(135deg, ${colour}1A 30%, rgba(255, 255, 255, 0.9) 100%)`,
                border: `2px solid ${colour}`,
                boxShadow: `0 2px 4px ${colour}1A`
            } as React.CSSProperties}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
        >
            <h1>{title}</h1>
            <img src={image} alt={title} className="ability-image" />
            
        </div>
    );
};


type AbilityData = {
    Name: string;
    Description: string;
    Extra_Description: string;
    Usage: string;
    Image: string;
    Gif: string;
    Stats: {
        ReloadTime: string;
        Credits: number;
        ClickTypeAndCount: string;
        Reusable: boolean;
        SecondaryAbility: string | null;
    };
};

type DataStructure = {
    [key: string]: AbilityData[];
};

const data: DataStructure = {  
    "1 Credit Abilities": [
        {
            Name: "Spawn",
            Description: "Claim an unclaimed node",
            Extra_Description: "Starting energy for a spawned node is 5",
            Usage: "Click on the node you want to spawn on.",
            Image: "/assets/abilityIcons/Spawn.png",
            Gif: "",
            Stats: {
                ReloadTime: "20 seconds",
                Credits: 1,
                ClickTypeAndCount: "1 click",
                Reusable: true,
                SecondaryAbility: "This is demo of the more information section"
            }
        },
        {
            Name: "Freeze",
            Description: "Make a dynamic edge directional",
            Extra_Description: "It'll swap and freeze in your advantage",
            Usage: "Click on the dynamic edge you want to freeze.",
            Image: "/assets/abilityIcons/Freeze.png",
            Gif: "",
            Stats: {
                ReloadTime: "4 seconds",
                Credits: 1,
                ClickTypeAndCount: "1 click",
                Reusable: false,
                SecondaryAbility: null
            }
        },
        {
            Name: "Burn",
            Description: "Convert a port node into a standard node",
            Extra_Description: "Not sure what to put here",
            Usage: "Click on the port node you want to burn.",
            Image: "/assets/abilityIcons/Burn.png",
            Gif: "",
            Stats: {
                ReloadTime: "1 second",
                Credits: 1,
                ClickTypeAndCount: "1 click",
                Reusable: false,
                SecondaryAbility: null
            }
        },
        {
            Name: "Zombie",
            Description: "Turn a node you own into a Zombie State.",
            Extra_Description: "Not sure what to put here",
            Usage: "Click on the node you want to turn into a Zombie State.",
            Image: "/assets/abilityIcons/Zombie.png",
            Gif: "",
            Stats: {
                ReloadTime: "2 seconds",
                Credits: 1,
                ClickTypeAndCount: "1 click",
                Reusable: false,
                SecondaryAbility: null
            }
        }
    ],
    "2 Credit Abilities": [
        {
            Name: "Bridge",
            Description: "Create an edge between two port-nodes",
            Extra_Description: "Not sure what to put here",
            Usage: "Click on the first node you want to bridge, then click on the second node you want to bridge to.",
            Image: "/assets/abilityIcons/Bridge.png",
            Gif: "",
            Stats: {
                ReloadTime: "2 seconds",
                Credits: 2,
                ClickTypeAndCount: "2 clicks",
                Reusable: false,
                SecondaryAbility: null
            }
        },
        {
            Name: "D-Bridge",
            Description: "Create a directional edge between two port-nodes",
            Extra_Description: "Not sure what to put here",
            Usage: "Click on the first node you want to D-Bridge, then click on the second node you want to D-Bridge to.",
            Image: "/assets/abilityIcons/D-Bridge.png",
            Gif: "",
            Stats: {
                ReloadTime: "8 seconds",
                Credits: 2,
                ClickTypeAndCount: "2 clicks",
                Reusable: false,
                SecondaryAbility: null
            }
        },
        {
            Name: "Rage",
            Description: "Increase energy transfer rate from your nodes by 2.5 times.",
            Extra_Description: "Not sure what to put here",
            Usage: "Once clicked, all nodes you own will be enraged for the next 10 seconds.",
            Image: "/assets/abilityIcons/Rage.png",
            Gif: "",
            Stats: {
                ReloadTime: "20 seconds",
                Credits: 2,
                ClickTypeAndCount: "1 click",
                Reusable: false,
                SecondaryAbility: null
            }
        },
        {
            Name: "Poison",
            Description: "Send poison along edges, edge loses energy over 20 seconds.",
            Extra_Description: "Not sure what to put here",
            Usage: "",
            Image: "/assets/abilityIcons/Poison.png",
            Gif: "",
            Stats: {
                ReloadTime: "5 seconds",
                Credits: 2,
                ClickTypeAndCount: "1 click",
                Reusable: false,
                SecondaryAbility: null
            }
        }
    ],
    "3 Credit Abilities": [
        {
            Name: "Nuke",
            Description: "Destroy all nodes in designated area surrounding the users capital node",
            Extra_Description: "Not sure what to put here",
            Usage: "Click on the node you want to nuke from. It cannot have a structure built on it.",
            Image: "/assets/abilityIcons/Nuke.png",
            Gif: "",
            Stats: {
                ReloadTime: "2 seconds",
                Credits: 3,
                ClickTypeAndCount: "1 click",
                Reusable: false,
                SecondaryAbility: null
            }
        },
        {
            Name: "Capital",
            Description: "Turn a full node into a capital.",
            Extra_Description: "Not sure what to put here",
            Usage: "Click on the node you want to turn into a capital. It cannot have a structure already built on it.",
            Image: "/assets/abilityIcons/Capital.png",
            Gif: "",
            Stats: {
                ReloadTime: "15 seconds",
                Credits: 3,
                ClickTypeAndCount: "1 click",
                Reusable: false,
                SecondaryAbility: null
            }
        },
        {
            Name: "Cannon",
            Description: "Fire a cannonball at an enemy node, dealing damage and reducing energy.",
            Extra_Description: "Not sure what to put here",
            Usage: "Click on one of your own nodes you want a cannon to be built on, then click on the enemy node you want to fire at.",
            Image: "/assets/abilityIcons/Cannon.png",
            Gif: "",
            Stats: {
                ReloadTime: "15 seconds",
                Credits: 3,
                ClickTypeAndCount: "2 clicks",
                Reusable: true,
                SecondaryAbility: "Can be captured and used by opponents."
            }
        },
        {
            Name: "Pump",
            Description: "Place on a node to replenish abilities once fully charged.",
            Extra_Description: "Not sure what to put here",
            Usage: "Click on the node you want the pump to be placed on. It cannot have a structure already built on it.",
            Image: "/assets/abilityIcons/Pump.png",
            Gif: "",
            Stats: {
                ReloadTime: "15 seconds",
                Credits: 3,
                ClickTypeAndCount: "1 click",
                Reusable: true,
                SecondaryAbility: "Can be drained to replenish abilities."
            }
        }
    ]
};

type AbilitiesListProps = {
    data: DataStructure;
    onAbilityClick: (ability: AbilityData) => void;
};

const AbilitiesList: React.FC<AbilitiesListProps> = ({ data, onAbilityClick }) => (
    <div className="HtPabilities-container">
        {Object.keys(data).map((category) =>
            data[category].map((ability, index) => (
                <Ability
                    key={`${category}-${index}`}
                    title={ability.Name}
                    desc={ability.Description}
                    extra={ability.Extra_Description}
                    usage={ability.Usage}
                    image={ability.Image}
                    onClick={() => onAbilityClick(ability)}
                    colour={abilityColors[ability.Name] || 'rgb(200, 200, 200)'}
                    reusable={ability.Stats.Reusable}
                    secondaryAbility={ability.Stats.SecondaryAbility}
                />
            ))
        )}
    </div>
);

type AbilityDetailProps = {
    ability: AbilityData | null;
    onClose: () => void;
};


const AbilityDetail: React.FC<AbilityDetailProps> = ({ ability, onClose }) => {
    const [showSecondary, setShowSecondary] = useState<boolean>(false);

    React.useEffect(() => {
        setShowSecondary(false); 
    }, [ability]);

    if (!ability) return null;

    const backgroundColor = abilityColors[ability.Name] || 'rgb(200, 200, 200)';
    const lightenedColor = lightenColor(backgroundColor, 0.7);

    const handleInfoClick = () => {
        if (ability.Stats.Reusable) {
            setShowSecondary(!showSecondary);
        }
    };

    return (
        <div
            className="HtPdetail-view"
            style={{
                backgroundColor: lightenedColor,
                padding: '20px',
                maxWidth: '600px',
            }}
        >
            <button className="HtPclose-button" onClick={onClose}>×</button>
            <h1>{ability.Name}</h1>
            <img src={ability.Image} alt={ability.Name} className="ability-image" />
            <h2>{ability.Description}</h2>
            <h3>{ability.Usage}</h3>
            <p>{ability.Extra_Description}</p>
            <div className="ability-stats">
                <h3>Stats:</h3>
                <ul>
                    <li><strong>Reload Time:</strong> {ability.Stats.ReloadTime}</li>
                    <li><strong>Credits:</strong> {ability.Stats.Credits}</li>
                    <li><strong>Click Type and Count:</strong> {ability.Stats.ClickTypeAndCount}</li>
                    <li>
                        <strong>Reusable:</strong> 
                        {ability.Stats.Reusable ? "Yes" : "No"}
                        {ability.Stats.Reusable && (
                            <button
                                onClick={handleInfoClick}
                                className="info-button"
                                title="Click to see more about the secondary ability"
                            >
                                <span className="info-icon">(i)</span>
                            </button>
                        )}
                    </li>
                    {showSecondary && ability.Stats.SecondaryAbility && (
                        <li><strong>Secondary Ability:</strong> {ability.Stats.SecondaryAbility}</li>
                    )}
                </ul>
            </div>
        </div>
    );
};


const HowToPlay: React.FC = () => {
    const [selectedAbility, setSelectedAbility] = useState<AbilityData | null>(null);
    const [showGif, setShowGif] = useState<boolean>(false);

    const handleAbilityClick = (ability: AbilityData) => {
        setSelectedAbility(ability);
        setShowGif(true);
    };

    const handleClose = () => {
        setSelectedAbility(null);
    };

    return (
        <div className="scrollable-container">
            <h1>How To Play</h1>
            <section className="space">
                <h2>Welcome to the game!</h2>
                <p>
                    This real-time strategy game is a thrilling twist on the classic board game Risk, built around the principles of graph theory. Here’s how to dive in and start playing:
                </p>
            </section>
            <section className="space">
                <h2>Game Overview</h2>
                <ul>
                    <li>
                        <strong>Nodes and Edges:</strong> Instead of countries, you'll control nodes, and instead of borders, nodes are connected by edges. These edges determine the flow of energy and attacks.
                    </li>
                    <li>
                        <strong>Energy Growth:</strong> Each node you own generates energy at a constant rate automatically. This energy is visually represented by the size of the nodes.
                    </li>
                    <li>
                        <strong>Real-Time Actions:</strong> Both attacking and reallocating energy occur in real time across the map.
                    </li>
                </ul>
            </section>
            <section className="space">
                <h2>Gameplay Mechanics</h2>
                <h3>1. Energy Growth</h3>
                <ul>
                    <li>Nodes you control will naturally grow in energy over time without any action needed from you.</li>
                    <li>The growth rate is constant and contributes to the node's size, indicating its energy level.</li>
                </ul>
                <h3>2. Attacking and Energy Transfer</h3>
                <ul>
                    <li><strong>Directional Edges:</strong> Each edge connecting nodes is directional and can be turned on or off by the owner of the "from-node".</li>
                    <li><strong>Energy Transfer Between Teammate Nodes:</strong> If an edge is turned on between two nodes you own (same color), energy will transfer in the direction the edge points.</li>
                    <li><strong>Attacking Opponent Nodes:</strong> If an edge is turned on between your node and an opponent's node, energy will be deducted equally from both nodes.</li>
                    <li><strong>Node Capture:</strong> If the attacked node’s energy drops to zero before the attacking node’s energy, the attacked node changes ownership to the attacker, adopting the attacker's color.</li>
                </ul>
                <p>Nodes continue to grow and transfer energy throughout the game until only one player remains with nodes of their color.</p>
            </section>
            <section className="space">
                <h2>Abilities</h2>
                <p>In addition to the basic gameplay mechanics, you can use abilities to gain an advantage over your opponents. Here are some of the abilities you can use:</p>
                <div style={{ display: 'flex', gap: '20px', height: 'auto' }}>
                    <div className="HtPabilities-container" style={{ width: selectedAbility ? '50%' : '100%', height: selectedAbility ? 'auto' : '100vh' }}>
                        <AbilitiesList data={data} onAbilityClick={handleAbilityClick} />
                    </div>
                    {selectedAbility && (
                        <AbilityDetail ability={selectedAbility} onClose={handleClose} />
                    )}
                </div>
                {showGif && (
                    <img src="/assets/animatedAbilities/Blue+West.gif" alt="Ability Animation" className="HtPability-gif" />
                )}
            </section>
        </div>
    );
};

export default HowToPlay;