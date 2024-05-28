export class OtherPlayer {
    name: string;
    color: [number, number, number]; // Assuming RGB tuple
    ready: boolean;
    eliminated: boolean;
    victor: boolean;

    constructor(name: string, color: [number, number, number], ready: boolean = false, eliminated: boolean = false, victor: boolean = false) {
        this.name = name;
        this.color = color;
        this.ready = ready;
        this.eliminated = eliminated;
        this.victor = victor;
    }
}

class MyPlayer extends OtherPlayer {
    score: number;

    constructor(name: string, color: [number, number, number], score: number = 0.0, ready: boolean = false, eliminated: boolean = false, victor: boolean = false) {
        super(name, color, ready, eliminated, victor);
        this.score = score;
    }
}