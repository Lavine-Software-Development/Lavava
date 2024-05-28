import { OtherPlayer } from "./otherPlayer";
import { IDItem } from "./idItem";
import { ClickType } from "./enums";
import { Node } from "./node";

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