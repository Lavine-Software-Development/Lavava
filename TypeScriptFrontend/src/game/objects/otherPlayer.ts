export class OtherPlayer {
    name: string;
    color: readonly [number, number, number];
    ready: boolean;
    eliminated: boolean;
    victor: boolean;

    constructor(name: string, color: readonly [number, number, number], ready: boolean = false, eliminated: boolean = false, victor: boolean = false) {
        this.name = name;
        this.color = color;
        this.ready = ready;
        this.eliminated = eliminated;
        this.victor = victor;
    }
}

