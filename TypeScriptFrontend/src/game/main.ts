import { MainScene } from "./scenes/main";
// import { SpriteCreatorScene } from "./scenes/creator";
import { AUTO, Game } from "phaser";
import { Preloader } from "./scenes/Preloader";
import { Network } from "./objects/network";
const createScene = (SceneClass, sceneProps, network, navigate) =>
    new SceneClass({ key: SceneClass.name }, sceneProps, network, navigate);
import ENV_CONFIG from '../env-config';
//  Find out more information about the Game Config at:
//  https://newdocs.phaser.io/docs/3.70.0/Phaser.Types.Core.GameConfig

const StartGame = (parent: string, props: any, network: Network, navigate: Function) => {
    console.log("Starting game");
    console.log(network);
    const config: Phaser.Types.Core.GameConfig = {
        type: AUTO,
        width: window.innerWidth,
        height: window.innerHeight,
        parent: "game-container",
        backgroundColor: "#ffffff",
        scene: [
            createScene(Preloader, props, network, navigate),
            createScene(MainScene, props, network, navigate),
        ],
        input: {
            keyboard: true,
            mouse: {
                target: window,
                preventDefaultMove: false // This allows right clicks to be detected
            },
            touch: true,
            gamepad: false,
        },
        disableContextMenu: ENV_CONFIG.disableContextMenu,
    };
    const game = new Game({ ...config, parent });

    return game;

};

export default StartGame;

