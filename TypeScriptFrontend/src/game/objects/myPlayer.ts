import { OtherPlayer } from "./otherPlayer";

export class MyPlayer extends OtherPlayer {
    score: number;
    credits: number;

    constructor(name: string, color: readonly [number, number, number], score: number = 0.0, ready: boolean = false, eliminated: boolean = false, victor: boolean = false) {
        super(name, color, ready, eliminated, victor);
        this.score = score;
        this.credits = 0;
    }
}