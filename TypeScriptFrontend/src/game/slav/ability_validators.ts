import { IDItem } from "./Objects/idItem";
import { OtherPlayer } from "./Objects/otherPlayer";
import { KeyCodes, MINIMUM_TRANSFER_VALUE, EventCodes } from "./constants";
import { ValidationFunction as ValidatorFunc, Point } from "./types";
import { Node } from "./Objects/node";
import { Edge } from "./Objects/edge";

function onSegment(p: Point, q: Point, r: Point): boolean {
    return (
        q[0] <= Math.max(p[0], r[0]) &&
        q[0] >= Math.min(p[0], r[0]) &&
        q[1] <= Math.max(p[1], r[1]) &&
        q[1] >= Math.min(p[1], r[1])
    );
}

function orientation(p: Point, q: Point, r: Point): number {
    const val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1]);
    if (val === 0) return 0; // Collinear
    return val > 0 ? 1 : 2; // Clock or counterclockwise
}

function doIntersect(p1: Point, q1: Point, p2: Point, q2: Point): boolean {
    const o1 = orientation(p1, q1, p2);
    const o2 = orientation(p1, q1, q2);
    const o3 = orientation(p2, q2, p1);
    const o4 = orientation(p2, q2, q1);

    return (
        (o1 !== o2 && o3 !== o4) ||
        (o1 === 0 && onSegment(p1, p2, q1)) ||
        (o2 === 0 && onSegment(p1, q2, q1)) ||
        (o3 === 0 && onSegment(p2, p1, q2)) ||
        (o4 === 0 && onSegment(p2, q1, q2))
    );
}

function noClick(data: IDItem[]): boolean {
    return false;
}

function standardPortNode(data: IDItem[]): boolean {
    const node = data[0] as Node;
    return node.owner !== undefined && node.isPort && node.stateName !== "mine";
}

function capitalValidator(edges: Edge[], player: OtherPlayer): ValidatorFunc {
    const neighbors = (node: Node): Node[] => {
        const neighbors: Node[] = [];
        edges.forEach((edge) => {
            try {
                const neighbor = edge.other(node);
                if (neighbor) neighbors.push(neighbor);
            } catch (error) {}
        });
        return neighbors;
    };

    return (data: IDItem[]): boolean => {
        const node = data[0] as Node; // Assuming data[0] is always a Node
        if (
            node.owner === player &&
            node.stateName !== "capital" &&
            node.full
        ) {
            let neighborCapital = false;
            for (const neighbor of neighbors(node)) {
                if (neighbor.stateName === "capital") {
                    neighborCapital = true;
                    break;
                }
            }
            return !neighborCapital;
        }
        return false;
    };
}

export function unownedNode(data: IDItem[]): boolean {
    const node = data[0] as Node;
    return node.owner === null && node.stateName === "default";
}

function playerValidators(player: OtherPlayer): {
    [key: string]: ValidatorFunc;
} {
    // Validator that checks if a node is attackable
    const standardNodeAttack = (data: IDItem[]): boolean => {
        const node = data[0] as Node; // Type casting to Node for TypeScript
        return (
            node.owner !== player &&
            node.owner !== undefined &&
            node.stateName !== "capital" &&
            node.stateName !== "mine"
        );
    };

    // Validator that checks if a node belongs to the player
    const myNode = (data: IDItem[]): boolean => {
        const node = data[0] as Node; // Type casting to Node for TypeScript
        return node.owner === player;
    };

    // Validator that checks if either node of a dynamic edge belongs to the player
    const dynamicEdgeOwnEither = (data: IDItem[]): boolean => {
        const edge = data[0] as Edge; // Type casting to Edge for TypeScript
        return edge.dynamic && edge.fromNode.owner === player;
    };

    // Return an object mapping codes to their respective validator functions
    return {
        [KeyCodes.POISON_CODE]: standardNodeAttack,
        [KeyCodes.NUKE_CODE]: standardNodeAttack,
        [KeyCodes.FREEZE_CODE]: dynamicEdgeOwnEither,
        [KeyCodes.ZOMBIE_CODE]: myNode,
        [KeyCodes.CANNON_CODE]: myNode,
    };
}

function newEdgeValidator(
    nodes: Node[],
    edges: Edge[],
    player: OtherPlayer
): ValidatorFunc {
    const checkNewEdge = (nodeFromId: number, nodeToId: number): boolean => {
        const edgeSet = new Set(
            edges.map((edge) => `${edge.fromNode.id}-${edge.toNode.id}`)
        );
        if (
            edgeSet.has(`${nodeToId}-${nodeFromId}`) ||
            edgeSet.has(`${nodeFromId}-${nodeToId}`)
        ) {
            return false;
        }

        // Check for overlaps with all other edges
        for (let edge of edges) {
            if (
                doIntersect(
                    [nodes[nodeFromId].pos.x, nodes[nodeFromId].pos.y],
                    [nodes[nodeToId].pos.x, nodes[nodeToId].pos.y],
                    [
                        nodes[edge.fromNode.id].pos.x,
                        nodes[edge.fromNode.id].pos.y,
                    ],
                    [nodes[edge.toNode.id].pos.x, nodes[edge.toNode.id].pos.y]
                )
            ) {
                return false;
            }
        }
        return true;
    };

    const newEdgeStandard = (data: Node[]): boolean => {
        if (data.length === 1) {
            const firstNode = data[0];
            return firstNode.owner === player;
        } else {
            const firstNode = data[0];
            const secondNode = data[1];
            return (
                firstNode.id !== secondNode.id &&
                checkNewEdge(firstNode.id, secondNode.id)
            );
        }
    };

    return (data: IDItem[]): boolean => {
        const nodes = data as Node[]; // Assert all data items are Nodes
        return (
            nodes.every((node) => node.portCount > 0) && newEdgeStandard(nodes)
        );
    };
}

export function makeAbilityValidators(
    player: OtherPlayer,
    nodes: Node[],
    edges: Edge[]
): { [key: string]: ValidatorFunc } {
    const abilityValidators: { [key: string]: ValidatorFunc } = {
        [KeyCodes.SPAWN_CODE]: unownedNode,
        [KeyCodes.BRIDGE_CODE]: newEdgeValidator(nodes, edges, player),
        [KeyCodes.D_BRIDGE_CODE]: newEdgeValidator(nodes, edges, player),
        [KeyCodes.BURN_CODE]: standardPortNode,
        [KeyCodes.RAGE_CODE]: noClick,
        [KeyCodes.CAPITAL_CODE]: capitalValidator(edges, player),
    };

    // Merge the validators from `player_validators` into `abilityValidators`
    const playerValidatorsMap = playerValidators(player);
    return { ...abilityValidators, ...playerValidatorsMap };
}

export function makeEventValidators(player: OtherPlayer): {
    [key: number]: (data: IDItem[]) => boolean;
} {
    function cannonShotValidator(data: IDItem[]): boolean {
        if (data.length === 1) {
            const firstNode = data[0] as Node;
            return (
                firstNode.owner === player &&
                firstNode.stateName === "cannon" &&
                firstNode.value > MINIMUM_TRANSFER_VALUE
            );
        } else if (data.length > 1) {
            const secondNode = data[1] as Node;
            return !(secondNode.owner === player && secondNode.full);
        }
        return false;
    }

    function edgeValidator(data: IDItem[]): boolean {
        if (
            data instanceof Array &&
            data.length > 0 &&
            data[0] instanceof Edge
        ) {
            const edge = data[0] as Edge;
            return edge.controlledBy(player);
        }
        return false;
    }

    return {
        [EventCodes.CANNON_SHOT_CODE]: cannonShotValidator,
        [EventCodes.STANDARD_LEFT_CLICK]: edgeValidator,
        [EventCodes.STANDARD_RIGHT_CLICK]: edgeValidator,
    };
}

