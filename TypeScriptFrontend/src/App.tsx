import { useRef, useState } from "react";
import React from "react";

import { IRefPhaserGame, PhaserGame } from "./game/PhaserGame";
import { MainMenu } from "./game/scenes/MainMenu";
import { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import WebSocketTest from "./websocketClient"; // Import your WebSocketTest component if not already done
import { Main } from "./game/slav/Objects/parse";
import board_data from "./game/slav/Objects/board_data.json";
function App() {
    // The sprite can only be moved in the MainMenu Scene
    const [canMoveSprite, setCanMoveSprite] = useState(true);

    //  References to the PhaserGame component (game and scene are exposed)
    const phaserRef = useRef<IRefPhaserGame | null>(null);
    const [spritePosition, setSpritePosition] = useState({ x: 0, y: 0 });
    // useEffect(() => {
    //     const ws = new WebSocket("ws://localhost:5553");
    //     ws.onopen = () => {
    //         console.log("Connected to server");
    //         ws.send('{"type": "HOST", "players":"1", "mode":"default"}');
    //     };

    //     ws.onmessage = (event) => {
    //         console.log("Received:", event.data);
    //         ws.send('{"type": "test", "players":"1", "mode":"default"}');
    //     };

    //     ws.onerror = (error) => {
    //         console.log("WebSocket error:", error);
    //     };

    //     ws.onclose = () => {
    //         console.log("Disconnected from server");
    //     };

    //     // Cleanup on unmount
    //     return () => {
    //         ws.close();
    //     };
    // }, []);
    const changeScene = () => {
        if (phaserRef.current) {
            const scene = phaserRef.current.scene as MainMenu;

            if (scene) {
                scene.changeScene();
            }
        }
    };
    const testMain = () => {
        const main = new Main();
        console.log("test");
        console.log(typeof board_data);
        main.setup(board_data);
        const updates = { "97": { on: true } };
        console.log(main.parse(main.edges, updates));
    };
    const moveSprite = () => {
        if (phaserRef.current) {
            const scene = phaserRef.current.scene as MainMenu;

            if (scene && scene.scene.key === "MainMenu") {
                // Get the update logo position
                scene.moveLogo(({ x, y }) => {
                    setSpritePosition({ x, y });
                });
            }
        }
    };

    const addSprite = () => {
        if (phaserRef.current) {
            const scene = phaserRef.current.scene;

            if (scene) {
                // Add more stars
                const x = Phaser.Math.Between(64, scene.scale.width - 64);
                const y = Phaser.Math.Between(64, scene.scale.height - 64);

                //  `add.sprite` is a Phaser GameObjectFactory method and it returns a Sprite Game Object instance
                const star = scene.add.sprite(x, y, "star");

                //  ... which you can then act upon. Here we create a Phaser Tween to fade the star sprite in and out.
                //  You could, of course, do this from within the Phaser Scene code, but this is just an example
                //  showing that Phaser objects and systems can be acted upon from outside of Phaser itself.
                scene.add.tween({
                    targets: star,
                    duration: 500 + Math.random() * 1000,
                    alpha: 0,
                    yoyo: true,
                    repeat: -1,
                });
            }
        }
    };

    // Event emitted from the PhaserGame component
    const currentScene = (scene: Phaser.Scene) => {
        setCanMoveSprite(scene.scene.key !== "MainMenu");
    };
    return (
        <Router>
            <div
                id="app"
                style={{ fontFamily: "Arial, sans-serif", lineHeight: "1.6" }}
            >
                <nav
                    style={{
                        backgroundColor: "#f0f0f0",
                        padding: "10px 0",
                        borderBottom: "2px solid #ccc",
                        marginBottom: "20px",
                    }}
                >
                    <div
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            gap: "20px",
                        }}
                    >
                        <button onClick={testMain}>Change Scene</button>
                        <Link
                            to="/"
                            style={{
                                padding: "10px 20px",
                                textDecoration: "none",
                                color: "#333",
                                fontWeight: "bold",
                            }}
                        >
                            Home
                        </Link>
                        <Link
                            to="/websocket-test"
                            style={{
                                padding: "10px 20px",
                                textDecoration: "none",
                                color: "#333",
                                fontWeight: "bold",
                            }}
                        >
                            WebSocket Test
                        </Link>
                    </div>
                </nav>
                <Routes>
                    <Route
                        path="/"
                        element={
                            <div>
                                <PhaserGame
                                    ref={phaserRef}
                                    currentActiveScene={currentScene}
                                />
                                <div>
                                    {/* Existing buttons and other UI components */}
                                </div>
                            </div>
                        }
                    />
                    <Route path="/websocket-test" element={<WebSocketTest />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;

