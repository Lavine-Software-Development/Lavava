import { OtherPlayer } from "./otherPlayer";

class MyPlayer extends OtherPlayer {
    score: number;

    constructor(name: string, color: [number, number, number], score: number = 0.0, ready: boolean = false, eliminated: boolean = false, victor: boolean = false) {
        super(name, color, ready, eliminated, victor);
        this.score = score;
    }
}