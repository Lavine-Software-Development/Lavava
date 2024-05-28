import { ClickType } from "./enums";
import { State } from "./States";
import { Colors, GROWTH_STOP } from "./constants";
import { OtherPlayer } from "./PlayersObjects";

export class IDItem{
    id: number;
    type: ClickType;

    constructor(id: number, type: ClickType) {
        this.id = id;
        this.type = type;
    }
}

export class Node extends IDItem {
    pos: [number, number];
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
        this.pos = pos;
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
            return this.ports.length > 0 ? Colors.BROWN : Colors.BLACK;
        }
        return this.owner.color;
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
}

export class Edge extends IDItem {
    fromNode: Node;
    toNode: Node;
    dynamic: boolean;
    on: boolean;
    flowing: boolean;

    constructor(id: number, fromNode: Node, toNode: Node, dynamic: boolean, on = false, flowing = false) {
        super(id, ClickType.EDGE); // Example ID logic
        this.fromNode = fromNode;
        this.toNode = toNode;
        this.dynamic = dynamic;
        this.on = on;
        this.flowing = flowing;
    }

    get color(): readonly [number, number, number] {
        return this.on ? this.fromNode.color : [50, 50, 50];
    }

    controlledBy(player: OtherPlayer): boolean {
        return this.fromNode.owner === player || (this.dynamic && this.toNode.owner === player && this.toNode.full);
    }

    other(node: Node): Node {
        if (node === this.fromNode) {
            return this.toNode;
        } else if (node === this.toNode) {
            return this.fromNode;
        }
        throw new Error("Node not in edge");
    }
}