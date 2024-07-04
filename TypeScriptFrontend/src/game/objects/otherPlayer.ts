export class OtherPlayer {
    name: string;
    _color: readonly [number, number, number];
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

    get color(): readonly [number, number, number] {
        return this._color;
    }

    set color(color: readonly [number, number, number]) {
        this._color = color;
    }
}

