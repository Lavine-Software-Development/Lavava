import { useRef, useState } from "react";
import React from "react";

import { IRefPhaserGame, PhaserGame } from "./game/PhaserGame";
import { MainMenu } from "./game/scenes/MainMenu";
import { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import WebSocketTest from "./websocketClient"; // Import your WebSocketTest component if not already done
import { Main } from "./game/slav/Objects/parse";
import board_data from "./game/slav/Objects/board_data.json";
import { BoardJSON } from "./game/slav/Objects/parse";
function App() {

    const phaserRef = useRef<IRefPhaserGame | null>(null);

    const testMain = () => {
        const main = new Main();
        console.log("test");
        console.log(typeof board_data);
        main.setup(board_data as BoardJSON);
        const updates = { "97": { on: true } };
        console.log(main.parse(main.edges, updates));
    };

    // Event emitted from the PhaserGame component
    const currentScene = (scene: Phaser.Scene) => {};

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

