import { MainScene } from "../scenes/main";

//proposal: rename 'OtherPlayer' to 'PlayerBase'
export class OtherPlayer {
    name: string;
    _color: readonly [number, number, number];
    ready: boolean;
    eliminated: boolean;
    victor: boolean;
    nodeCount: number;

    protected renderedText: Array<Phaser.GameObjects.Text> = [];

    constructor(id: string, color: readonly [number, number, number], ready: boolean = false, eliminated: boolean = false, victor: boolean = false) {
        this.name = id;
        this.color = color;
        this.ready = ready;
        this.eliminated = eliminated;
        this.victor = victor;
        this.nodeCount = 0;
    }

    get color(): readonly [number, number, number] {
        return this._color;
    }

    set color(color: readonly [number, number, number]) {
        this._color = color;
    }

    destroyRenderedText() {
        this.renderedText.forEach((text) => text.destroy())
    }

    //proposal: remove 'scene' parameter and require 'scene' in constructor
    renderNodeCount(scene: MainScene, position) {
        const { x, y } = this.calculateInitialLabelPosition(scene, position);

        let count_y = y - 20;
        if (scene.readonlySettings.starting_structures) {
            count_y = y - 40;
        }

        //proposal: move rgbToHex to special utils class/file
        const playerColor = scene.rgbToHex(this.color);
        const countText = scene.add.text(
            x,
            count_y,
            `Count: `,
            {
                fontFamily: "Arial",
                fontSize: "19px", // Slightly smaller font
                color: playerColor,
            }
        );
        countText.setOrigin(0, 1);  // Align to bottom-left
        this.renderedText.push(countText);

        const countNumber = scene.add.text(
            countText.x + countText.width,
            count_y,
            `${this.nodeCount}`,
            {
                fontFamily: "Arial",
                fontSize: "19px",
                color: '#000000', // Black color for the number
            }
        );
        countNumber.setOrigin(0, 1);
        this.renderedText.push(countNumber);
    }

    protected calculateInitialLabelPosition(scene: MainScene, position): { x: number, y: number } {
        const x = (position.xPercent / 100) * (scene.sys.game.config.width as number);
        const y = (position.yPercent / 100) * (scene.sys.game.config.height as number);

        let count_y = y - 20;
        if (scene.readonlySettings.starting_structures) {
            count_y = y - 40;
        }
        return { x, y }
    }
}

