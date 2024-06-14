import { Boot } from "./scenes/Boot";
import { GameOver } from "./scenes/GameOver";
import { Game as MainGame } from "./scenes/Game";
import { MainMenu } from "./scenes/MainMenu";
import { MainScene } from "./scenes/main";
// import { SpriteCreatorScene } from "./scenes/creator";
import { AUTO, Game } from "phaser";
import { Preloader } from "./scenes/Preloader";
const createScene = (SceneClass, sceneProps) =>
    new SceneClass({ key: SceneClass.name }, sceneProps);
//  Find out more information about the Game Config at:
//  https://newdocs.phaser.io/docs/3.70.0/Phaser.Types.Core.GameConfig

const StartGame = (parent: string, props: any) => {
    const config: Phaser.Types.Core.GameConfig = {
        type: AUTO,
        width: 1424,
        height: 768,
        parent: "game-container",
        backgroundColor: "#ffffff",
        scene: [createScene(Preloader, props), createScene(MainScene, props)],
        input: {
            keyboard: true,
            mouse: true,
            touch: true,
            gamepad: false,
        },
    };
    return new Game({ ...config, parent });
};

export default StartGame;

