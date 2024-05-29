import { State } from "../States";
import { Colors, GROWTH_STOP } from "../constants";
import { OtherPlayer } from "./otherPlayer";
import { IDItem } from "./idItem";
import { ClickType } from "../enums";

export class Node extends IDItem {
    pos: Phaser.Math.Vector2;
    isPort: boolean;
    portPercent: number;
    ports: Array<number>; 
    state: State;
    value: number;
    effects: Set<string>; 
    owner: OtherPlayer | null;

    constructor(
        id: number, pos: [number, number], isPort: boolean,
        portPercent: number, ports: Array<any>, state: State, value: number,
        effects = new Set<string>(), owner: OtherPlayer | null = null
    ) {
        super(id, ClickType.NODE);
        this.pos = new Phaser.Math.Vector2(pos[0], pos[1]);
        this.isPort = isPort;
        this.portPercent = portPercent;
        this.ports = ports;
        this.state = state;
        this.value = value;
        this.effects = effects;
        this.owner = owner;
    }

    get color(): readonly [number, number, number] {
        if (!this.owner) {
            return this.isPort ? Colors.BROWN : Colors.BLACK;
        }
        return this.owner.color;
    }

    get phaserColor(): number {
        const col = this.color;
        return Phaser.Display.Color.GetColor(col[0], col[1], col[2]);
    }

    get size(): number {
        return 5 + this.sizeFactor * 18;
    }

    get sizeFactor(): number {
        if (this.value < 5) return 0;
        return Math.max(Math.log10(this.value / 10) / 2 + this.value / 1000 + 0.15, 0);
    }

    get stateName(): string {
        return this.state.name;
    }

    get full(): boolean {
        return this.value >= GROWTH_STOP;
    }

    get portCount(): number {
        return this.ports.length;
    }

    draw(scene: Phaser.Scene): void {
        let graphics = scene.add.graphics({ fillStyle: { color: this.phaserColor } });
        graphics.fillCircle(this.pos.x, this.pos.y, this.value);
    }
}