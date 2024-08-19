import { MainScene } from "../scenes/main";
import { OtherPlayer } from "./otherPlayer";

export class MyCreditPlayer extends OtherPlayer {
    credits: number;
    capitalCount: number;
    constructor(name: string, color: readonly [number, number, number], ready: boolean = false, eliminated: boolean = false, victor: boolean = false) {
        super(name, color, ready, eliminated, victor);
        this.credits = 0;
        this.capitalCount = 0;
    }

    renderCapitalCount(scene: MainScene, position) {

        const { x, y } = this.calculateInitialLabelPosition(scene, position);

        //proposal: move rgbToHex to util class/file
        const playerColor = scene.rgbToHex(this?.color);

        // Display full capital count
        const capitalText = scene.add.text(
            x,
            y - 15,
            `Full Capitals: `,
            {
                fontFamily: "Arial",
                fontSize: "23px",
                color: playerColor,
            }
        );
        capitalText.setOrigin(0, 1);  // Align to bottom-left
        this.renderedText.push(capitalText);

        const capitalNumber = scene.add.text(
            capitalText.x + capitalText.width,
            y - 15,
            `${this.capitalCount || 0}`,
            {
                fontFamily: "Arial",
                fontSize: "23px",
                color: '#000000', // Black color for the number
            }
        );
        capitalNumber.setOrigin(0, 1);
        this.renderedText.push(capitalNumber);
    }
}

export class MyElixirPlayer extends OtherPlayer {
    elixir: number;

    constructor(name: string, color: readonly [number, number, number], ready: boolean = false, eliminated: boolean = false, victor: boolean = false) {
        super(name, color, ready, eliminated, victor);
        this.elixir = 0;
    }
}