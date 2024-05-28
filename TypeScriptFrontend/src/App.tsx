import { useRef, useState, useEffect } from "react";
import { IRefPhaserGame, PhaserGame } from "./game/PhaserGame";
import { MainMenu } from "./game/scenes/MainMenu";

function App() {
    const [canMoveSprite, setCanMoveSprite] = useState(true);
    const phaserRef = useRef<IRefPhaserGame | null>(null);
    const [spritePosition, setSpritePosition] = useState({ x: 0, y: 0 });

    useEffect(() => {
        const ws = new WebSocket("ws://localhost:8765");

        ws.onopen = () => {
            console.log("Connected to server");
            ws.send("Hello, server!");
        };

        ws.onmessage = (event) => {
            console.log("Received:", event.data);
            ws.send("pong");
            // Handle incoming messages and update the state if necessary
            // const data = JSON.parse(event.data);
            // if (data.type === "spritePosition") {
            //     setSpritePosition({ x: data.x, y: data.y });
            // }
        };

        ws.onerror = (error) => {
            console.log("WebSocket error:", error);
        };

        ws.onclose = () => {
            console.log("Disconnected from server");
        };

        // Cleanup on unmount
        return () => {
            ws.close();
        };
    }, []);

    const changeScene = () => {
        if (phaserRef.current) {
            const scene = phaserRef.current.scene as MainMenu;

            if (scene) {
                scene.changeScene();
            }
        }
    };

    const moveSprite = () => {
        if (phaserRef.current) {
            const scene = phaserRef.current.scene as MainMenu;

            if (scene && scene.scene.key === "MainMenu") {
                scene.moveLogo(({ x, y }) => {
                    setSpritePosition({ x, y });

                    // Optionally send the new position to the server
                    ws.send(JSON.stringify({ type: "spritePosition", x, y }));
                });
            }
        }
    };

    const addSprite = () => {
        if (phaserRef.current) {
            const scene = phaserRef.current.scene;

            if (scene) {
                const x = Phaser.Math.Between(64, scene.scale.width - 64);
                const y = Phaser.Math.Between(64, scene.scale.height - 64);
                const star = scene.add.sprite(x, y, "star");

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

    const currentScene = (scene: Phaser.Scene) => {
        setCanMoveSprite(scene.scene.key !== "MainMenu");
    };

    return (
        <div id="app">
            <PhaserGame ref={phaserRef} currentActiveScene={currentScene} />
            <div>
                <div>
                    <button
                        disabled={canMoveSprite}
                        className="button"
                        onClick={moveSprite}
                    >
                        Toggle Movement
                    </button>
                </div>
                <div className="spritePosition">
                    Sprite Position:
                    <pre>{`{\n  x: ${spritePosition.x}\n  y: ${spritePosition.y}\n}`}</pre>
                </div>
                <div>
                    <button className="button" onClick={addSprite}>
                        Add New Sprite
                    </button>
                </div>
            </div>
        </div>
    );
}

export default App;

