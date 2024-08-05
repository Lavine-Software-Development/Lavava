import { OtherPlayer } from "./otherPlayer";

export class MyCreditPlayer extends OtherPlayer {
    credits: number;

    constructor(name: string, color: readonly [number, number, number], ready: boolean = false, eliminated: boolean = false, victor: boolean = false) {
        super(name, color, ready, eliminated, victor);
        this.credits = 0;
    }
}

export class MyElixirPlayer extends OtherPlayer {
    elixir: number;

    constructor(name: string, color: readonly [number, number, number], ready: boolean = false, eliminated: boolean = false, victor: boolean = false) {
        super(name, color, ready, eliminated, victor);
        this.elixir = 0;
    }
}