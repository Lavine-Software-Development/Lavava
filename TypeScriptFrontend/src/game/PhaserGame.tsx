// import React from "react";

// import { forwardRef, useEffect, useLayoutEffect, useRef } from "react";
// import StartGame from "./main";
// import { EventBus } from "./EventBus";

// export interface IRefPhaserGame {
//     game: Phaser.Game | null;
//     scene: Phaser.Scene | null;
// }

// interface IProps {
//     currentActiveScene?: (scene_instance: Phaser.Scene) => void;
//     props?: any;
// }

// export const PhaserGame = forwardRef<IRefPhaserGame, IProps>(
//     function PhaserGame({ currentActiveScene, props }, ref) {
//         const game = useRef<Phaser.Game | null>(null!);

//         useLayoutEffect(() => {
//             if (game.current === null) {
//                 game.current = StartGame("game-container", props);

//                 if (typeof ref === "function") {
//                     ref({ game: game.current, scene: null });
//                 } else if (ref) {
//                     ref.current = { game: game.current, scene: null };
//                 }
//             }

//             return () => {
//                 if (game.current) {
//                     game.current.destroy(true);
//                     if (game.current !== null) {
//                         game.current = null;
//                     }
//                 }
//             };
//         }, [ref]);

//         useEffect(() => {
//             EventBus.on(
//                 "current-scene-ready",
//                 (scene_instance: Phaser.Scene) => {
//                     if (
//                         currentActiveScene &&
//                         typeof currentActiveScene === "function"
//                     ) {
//                         currentActiveScene(scene_instance);
//                     }

//                     if (typeof ref === "function") {
//                         ref({ game: game.current, scene: scene_instance });
//                     } else if (ref) {
//                         ref.current = {
//                             game: game.current,
//                             scene: scene_instance,
//                         };
//                     }
//                 }
//             );
//             return () => {
//                 EventBus.removeListener("current-scene-ready");
//             };
//         }, [currentActiveScene, ref]);

//         return <div id="game-container"></div>;
//     }
// );

import React, { forwardRef, useEffect, useLayoutEffect, useRef } from "react";
import { useLocation } from "react-router-dom";
import StartGame from "./main";
import { EventBus } from "./EventBus";

export interface IRefPhaserGame {
    game: Phaser.Game | null;
    scene: Phaser.Scene | null;
}

interface IProps {
    currentActiveScene?: (scene_instance: Phaser.Scene) => void;
    props?: any;
}

export const PhaserGame = forwardRef<IRefPhaserGame, IProps>(
    function PhaserGame({ currentActiveScene }, ref) {
        const game = useRef<Phaser.Game | null>(null!);
        const location = useLocation();
        const boardData = location.state?.boardData;
        console.log("location: ", boardData);
        useLayoutEffect(() => {
            if (game.current === null) {
                game.current = StartGame("game-container", boardData);

                if (typeof ref === "function") {
                    ref({ game: game.current, scene: null });
                } else if (ref) {
                    ref.current = { game: game.current, scene: null };
                }
            }

            return () => {
                if (game.current) {
                    game.current.destroy(true);
                    if (game.current !== null) {
                        game.current = null;
                    }
                }
            };
        }, [ref, boardData]);

        useEffect(() => {
            EventBus.on(
                "current-scene-ready",
                (scene_instance: Phaser.Scene) => {
                    if (
                        currentActiveScene &&
                        typeof currentActiveScene === "function"
                    ) {
                        currentActiveScene(scene_instance);
                    }

                    if (typeof ref === "function") {
                        ref({ game: game.current, scene: scene_instance });
                    } else if (ref) {
                        ref.current = {
                            game: game.current,
                            scene: scene_instance,
                        };
                    }
                }
            );
            return () => {
                EventBus.removeListener("current-scene-ready");
            };
        }, [currentActiveScene, ref]);

        return <div id="game-container"></div>;
    }
);

