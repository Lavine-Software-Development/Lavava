import "../../styles/style.css";
import React, { useEffect, useState } from "react";
import { Link } from 'react-router-dom';

const slides = {
    basics: [
        [
            { type: "text", content: "Welcome to Durb.<br/>See all those dots on the screen?<br/>Your goal is to capture as many dots as you can." },
            { type: "image", content: "../assets/HowToPlay/start_nodes.png", style: { width: "80%" } }
        ],
        [
            { type: "text", content: "To begin the game, choose a starting dot." },
            { type: "image", content: "../assets/HowToPlay/cursor_on_node.png", style: { width: "30%" } },
            { type: "text", content: "Click on a dot to claim it as your own." },
            { type: "image", content: "../assets/HowToPlay/claim_node.png", style: { width: "30%" } },
            { type: "text", content: "Note: This is the only dot that you'll own just by clicking it." }
        ],
        [
            { type: "text", content: "Watch as this dot's energy grows." },
            { type: "gif", content: "../assets/HowToPlay/node-growing.gif" },
            { type: "text", content: "Each dot that is owned by a player will naturally grow energy on its own.<br/>Energy growth is constant." }
        ],
        [
            { type: "text", content: "However, after a while, dots stop growing. They become full, and a black ring forms around them." },
            { type: "image", content: "../assets/HowToPlay/full_node.png" }
        ],
        [
            { type: "text", content: "Each dot has some bridges surrounding it." },
            { type: "gif", content: "../assets/HowToPlay/bridge_on.gif" },
            { type : "text", content: "Bridges allow you to transfer energy from one dot to another." }
        ],
        [
            { type: "text", content: "Click a bridge to turn it on." },
            { type: "gif", content: "../assets/HowToPlay/edge_on.gif", style: { width: "280px", height: "auto" } },
            { type: "text", content: "Now energy flows in the direction it points." }
        ],
        [
            { type: "text", content: "There are two kinds of bridges: Standard bridges, made up of triangles,<br/>and Dynamic Bridges (D-Bridge) made up of mostly circles, and one green triangle." },
            { type: "image", content: "../assets/HowToPlay/standard_bridge.png", text: "Standard Bridge", sideBySide: true },
            { type: "image", content: "../assets/HowToPlay/dynamic_bridge.png", text: "Dynamic Bridge", sideBySide: true }
        ],
        [
            { type: "text", content: "If you own both dots, you can switch the direction of a Dynamic Bridge by right clicking on it." },
            { type: "gif", content: "../assets/HowToPlay/dynamic_bridge_flip.gif" }
        ],
    ],
    attacking: [
        [
            { type: "text", content: "To attack another player's dot, you need to send energy from your dot to theirs." },
            { type: "gif", content: "../assets/HowToPlay/attack.gif", style: { width: "280px", height: "auto" }}
        ],
        [
            { type: "text", content: "If your energy is greater than the target dot's energy, you will capture it." },
            { type: "image", content: "../assets/HowToPlay/capture_node.gif" },
        ]
    ],
    abilities: [
        [
            { type: "text", content: "Abilities are special actions you can use during the game.<br/>Here are five examples:" },
            { type: "image", content: "../assets/HowToPlay/freeze_ability.png", sideBySide: true },
            { type: "image", content: "../assets/HowToPlay/bridge_ability.png", sideBySide: true },
            { type: "image", content: "../assets/HowToPlay/d_bridge_ability.png", sideBySide: true },
            { type: "image", content: "../assets/HowToPlay/rage_ability.png", sideBySide: true },
            { type: "image", content: "../assets/HowToPlay/nuke_ability.png", sideBySide: true },
            { type: "text", content: "They let you do things like create new connections, claim distant points, boost energy transfer, or even destroy an opponent's point." },
        ],
        [
            { type: "text", content: "The cost for using abilities is measured in Elixir,<br/>a resource that accumulates gradually over time." },
            { type: "image", content: "../assets/HowToPlay/elixir_bar.png", style: { width: "1.5em", height: "auto" } },
        ],
        [
            { type: "text", content: "To use an ability, click on the ability icon on the right side of the screen." },
        ],
        // [
        //     { type: "image", content: "../assets/HowToPlay/freeze_ability.png"},
        //     { type: "text", content: "Changes a two-way bridge to a one-way bridge, preventing enemies from attacking you through it while you can still use it to transfer energy." },
        // ],
        [
            { type: "text", content: "This is the quintessential ability so we’ll tell you about it now. Lets leave the rest for later" },
            { type: "image", content: "../assets/HowToPlay/bridge_ability.png" },
            { type: "text", content: "Creates a new bridge between two dots, allowing you to transfer energy between them." },
        ],
        [
            { type: "text", content: "Some dots have walls around them. You CANNOT bridge to a wall but you CAN start at a wall." },
            { type: "image", content: "../assets/HowToPlay/walled_node.png" }
        ],
        // [
        //     { type: "image", content: "../assets/HowToPlay/d_bridge_ability.png" },
        //     { type: "text", content: "Creates a new two-way bridge between two dots, allowing you to control the direction of the flow of energy by flipping it." },
        // ],
        // [
        //     { type: "image", content: "../assets/HowToPlay/rage_ability.png" },
        //     { type: "text", content: "Temporarily boosts the speed at which all your dots transfer energy, allowing for rapid expansion or attacks." },
        // ],
        // [
        //     { type: "image", content: "../assets/HowToPlay/nuke_ability.png" },
        //     { type: "text", content: "Destroys a dot and all its connections, removing it from the map entirely." },
        // ],
    ],
    gameStages: [
        [
            { type: "text", content: "The game has several stages, each with different objectives and challenges." },
        ],
        [
            { type: "text", content: "There are 3 phases. Start, Main Game, OverTime." },
        ],
        [
            { type: "text", content: "In the Start phase, you can only claim a dot by clicking on it.<br/>This phase ends when everyone has claimed a dot." },
        ],
        [
            { type: "text", content: "In the Main Game phase, you have the real juicy stuff.<br/>You get to attack other players and claim territory." },
        ],
        [
            { type: "text", content: "Part way through the Main Game phase, all the grey walls come down.<br/>This makes way for creating more bridges" },
        ],
        [
            { type: "text", content: "In the OverTime phase, things heat up. Attacks become free.<br/><br/>What is free attacking?<br/>When you transfer energy into an opponent, you won't shrink at all. Only they will.<br/>This is meant to help finish the game." },
        ],
        [
            { type: "text", content: "Times up!<br/>If no one wins in overtime, the player who owns the most dots wins.<br/>" },
        ],
        // [
        //     { type: "text", content: "Here are some tips for each stage:" },
        // ],
        // [
        //     { type: "text", content: "In the early stages, focus on capturing as many dots as possible." },
        // ],
        // [
        //     { type: "text", content: "In the mid-game, start building your strategy and attacking other players." },
        // ],
        // [
        //     { type: "text", content: "In the late game, defend your territory and aim for the win." },
        // ]
    ],
    extraInfo: [
        [
            { type: "text", content: "In a contested situation, a dynamic bridge bends to the will of the bigger node, directing its flow away from it." },
        ],
        // [
        //     { type: "text", content: "That's it! You're ready to play Basic mode." },
        // ],
        // [
        //     { type: "text", content: "Remember, the goal is to capture as many dots as you can and defeat your opponents." },
        // ],
        // [
        //     { type: "text", content: "Here are some extra tips to help you win:" },
        // ],
        // [
        //     { type: "text", content: "Don't forget to use your abilities. They can be the difference between winning and losing." },
        // ],
        // [
        //     { type: "text", content: "Keep an eye on your elixir levels. If you run out, you won't be able to use abilities until it regenerates." },
        // ],
        // [
        //     { type: "text", content: "Don't be afraid to attack. The best defense is a good offense." },
        // ],
        // [
        //     { type: "text", content: "Watch your opponents. If they're getting too powerful, it might be time to take them down a peg." },
        // ],
        // [
        //     { type: "text", content: "Good luck!" },
        // ]
    ]
};

const renderContent = (item, index, array) => {
    if (item.sideBySide && index > 0 && array[index - 1].sideBySide) {
        return null; // Skip rendering this item as it will be handled by the previous item
    }

    if (item.sideBySide) {
        const sideBySideItems: { type: string; content: string; className?: string; style?: React.CSSProperties; text?: string; sideBySide?: boolean; }[] = [];
        let i = index;

        // Collect all consecutive sideBySide items
        while (i < array.length && array[i].sideBySide) {
            sideBySideItems.push(array[i]);
            i++;
        }

        return (
            <div key={index} className="side-by-side-container">
                {sideBySideItems.map((sideItem, sideIndex) => (
                    <div key={sideIndex} className="side-by-side-item">
                        <img src={sideItem.content} className={sideItem.className} style={{ ...sideItem.style, width: '100%' }} alt="Slide content" />
                        {sideItem.text && <div className="side-by-side-text">{sideItem.text}</div>}
                    </div>
                ))}
            </div>
        );
    }

    switch (item.type) {
        case "text":
            return <div key={index} className="slide-text" dangerouslySetInnerHTML={{ __html: item.content }} />;
        case "image":
            return <img key={index} src={item.content} alt="Slide content" style={item.style} />;
        case "gif":
            return <img key={index} src={item.content} alt="Slide content" style={item.style} />;
        default:
            return null;
    }
};

const HowToPlay: React.FC = () => {
    const [currentSection, setCurrentSection] = useState("basics");
    const [currentSlide, setCurrentSlide] = useState(0);
    const [activeButton, setActiveButton] = useState("basics");

    const handleNextSlide = () => {
        if (currentSlide < slides[currentSection].length - 1) {
            setCurrentSlide(currentSlide + 1);
        } else {
            const sectionKeys = Object.keys(slides);
            const currentSectionIndex = sectionKeys.indexOf(currentSection);
            const nextSectionIndex = (currentSectionIndex + 1) % sectionKeys.length;
            const nextSection = sectionKeys[nextSectionIndex];
            
            setCurrentSection(nextSection);
            setCurrentSlide(0);
            setActiveButton(nextSection);
        }
    };

    const handlePrevSlide = () => {
        if (currentSlide > 0) {
            setCurrentSlide(currentSlide - 1);
        } else {
            const sectionKeys = Object.keys(slides);
            const currentSectionIndex = sectionKeys.indexOf(currentSection);
            const prevSectionIndex = (currentSectionIndex - 1 + sectionKeys.length) % sectionKeys.length;
            const prevSection = sectionKeys[prevSectionIndex];
            
            setCurrentSection(prevSection);
            setCurrentSlide(slides[prevSection].length - 1);
            setActiveButton(prevSection);
        }
    };

    const handleSectionChange = (section: string) => {
        setCurrentSection(section);
        setCurrentSlide(0);
        setActiveButton(section);
    };

    const handleKeyDown = (event: KeyboardEvent) => {
        if (event.key === "ArrowLeft") {
            handlePrevSlide();
        } else if (event.key === "ArrowRight") {
            handleNextSlide();
        }
    };

    useEffect(() => {
        window.addEventListener("keydown", handleKeyDown);
        return () => {
            window.removeEventListener("keydown", handleKeyDown);
        };
    }, [currentSlide, currentSection]);

    const currentContent = slides[currentSection][currentSlide];

    return (
        <div className="scrollable-container">
            <h1>Basic Mode: How to Play</h1>
            <div className="htp-button-container">
                <button
                    onClick={() => handleSectionChange("basics")}
                    className="basics-button"
                    disabled={activeButton === "basics"}
                >
                    Basics
                </button>
                <button
                    onClick={() => handleSectionChange("attacking")}
                    className="attacking-button"
                    disabled={activeButton === "attacking"}
                >
                    Attacking
                </button>
                <button
                    onClick={() => handleSectionChange("abilities")}
                    className="abilities-button"
                    disabled={activeButton === "abilities"}
                >
                    Abilities
                </button>
                <button
                    onClick={() => handleSectionChange("gameStages")}
                    className="game-stages-button"
                    disabled={activeButton === "gameStages"}
                >
                    Game Stages
                </button>
                <button
                    onClick={() => handleSectionChange("extraInfo")}
                    className="extra-info-button"
                    disabled={activeButton === "extraInfo"}
                >
                    Extra Info
                </button>
            </div>
            <div className="slide-container">
                <div className="prev-slide-icon-btn slide-icon-btn">
                    {currentSlide > 0 && (
                            <img src="../assets/HowToPlay/left-arrow.png" alt="Slide Left" onClick={handlePrevSlide} />
                    )}
                </div>
                {currentContent.map((item, index, array) => renderContent(item, index, array))}
                <div className="next-slide-icon-btn slide-icon-btn">
                    <img src="../assets/HowToPlay/right-arrow.png" alt="Slide Right" onClick={handleNextSlide} />
                </div>
            </div>
        </div>
    );
};

export default HowToPlay;