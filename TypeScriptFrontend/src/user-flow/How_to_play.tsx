import "../../styles/style.css";
import React, { useEffect, useState } from "react";
import { Link } from 'react-router-dom';

const slides = {
    basics: [
        [
            { type: "text", content: "Welcome to Durb.<br/>See all those dots on the screen?<br/>Your goal is to capture as many dots as you can." },
            { type: "image", content: "../assets/HowToPlay/start_nodes.png" }
        ],
        [
            { type: "text", content: "To begin the game, choose a starting dot." },
            { type: "image", content: "../assets/HowToPlay/cursor_on_node.png" },
            { type: "text", content: "Click on a dot to claim it as your own." },
            { type: "image", content: "../assets/HowToPlay/claim_node.png" },
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
            { type: "image", content: "../assets/HowToPlay/bridges_around_nodes.png" },
            { type : "text", content: "Bridges allow you to transfer energy from one dot to another." }
        ],
        [
            { type: "text", content: "Some dots have walls around them. You cannot bridge to a wall but you can start at a wall." },
            { type: "image", content: "../assets/HowToPlay/walled_node.png" }
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
        ]
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
            { type: "text", content: "In the OverTime phase, things heat up. Walls come down and attacks become free." },
        ],
        [
            { type: "text", content: "What is free attacking?<br/>When you transfer energy into an opponent, you won't shrink at all. Only they will.<br/>This is meant to help finish the game." },
        ],
        [
            { type: "text", content: "Times up!<br/>If no one wins in overtime, the player who owns the most dots wins.<br/>" },
        ],
        [
            { type: "text", content: "Here are some tips for each stage:" },
        ],
        [
            { type: "text", content: "In the early stages, focus on capturing as many dots as possible." },
        ],
        [
            { type: "text", content: "In the mid-game, start building your strategy and attacking other players." },
        ],
        [
            { type: "text", content: "In the late game, defend your territory and aim for the win." },
        ]
    ]
};

const renderContent = (item, index, array) => {
    if (item.sideBySide && index > 0 && array[index - 1].sideBySide) {
        return null; // Skip rendering this item as it will be handled by the previous item
    }

    if (item.sideBySide && index < array.length - 1 && array[index + 1].sideBySide) {
        return (
            <div key={index} className="side-by-side-container">
                <div className="side-by-side-item">
                    <img src={item.content} className={item.className} style={{ ...item.style, width: '100%' }} alt="Slide content" />
                    {item.text && <div className="side-by-side-text">{item.text}</div>}
                </div>
                <div className="side-by-side-item">
                    <img src={array[index + 1].content} className={array[index + 1].className} style={{ ...array[index + 1].style, width: '100%' }} alt="Slide content" />
                    {array[index + 1].text && <div className="side-by-side-text">{array[index + 1].text}</div>}
                </div>
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
            <h1>Royale Mode: How to Play</h1>
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
                    onClick={() => handleSectionChange("gameStages")}
                    className="game-stages-button"
                    disabled={activeButton === "gameStages"}
                >
                    Game Stages
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