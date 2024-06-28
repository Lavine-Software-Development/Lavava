import { IDItem } from "./idItem";
import { OtherPlayer } from "./otherPlayer";
import {
    KeyCodes,
    MINIMUM_TRANSFER_VALUE,
    EventCodes,
    NUKE_RANGE,
} from "./constants";
import { ValidationFunction as ValidatorFunc, Point } from "./types";
import { Node } from "./node";
import { Edge } from "./edge";
import { ReloadAbility } from "./ReloadAbility";

function hasAnySame(
    num1: number,
    num2: number,
    num3: number,
    num4: number
): boolean {
    return num1 === num3 || num1 === num4 || num2 === num4 || num2 === num3;
}

function noClick(data: IDItem[]): boolean {
    return false;
}

function standardPortNode(data: IDItem[]): boolean {
    const node = data[0] as Node;
    return node.owner !== undefined && node.is_port && node.stateName !== "mine";
}

const standardNodeAttack = (data: IDItem, player: OtherPlayer): boolean => {
    const node = data as Node;
    return (
        node.owner !== player &&
        node.owner !== null &&
        node.stateName !== "capital" &&
        node.stateName !== "mine"
    );
};

const checkNewEdge = (nodeFrom: Node, nodeTo: Node, edges: Edge[]): boolean => {

    const newLine = new Phaser.Geom.Line(nodeFrom.pos.x, nodeFrom.pos.y, nodeTo.pos.x, nodeTo.pos.y);
    // Check for overlaps with all other edges
    for (let edge of edges) {
        if (!hasAnySame(nodeFrom.id, nodeTo.id, edge.from_node.id, edge.to_node.id) && Phaser.Geom.Intersects.LineToLine(newLine, edge.line)) {
            return false;
        }
    }
    return true;
};

function attackValidators(nodes: Node[], player: OtherPlayer) {
    return function capitalRangedNodeAttack(data: IDItem[]): boolean {
        const node = data[0] as Node;
        const capitals = nodes.filter(
            (node) => node.stateName === "capital" && node.owner === player
        );

        const inCapitalRange = (capital: Node): boolean => {
            const { x: x1, y: y1 } = node.pos;
            const { x: x2, y: y2 } = capital.pos;
            const distance = (x1 - x2) ** 2 + (y1 - y2) ** 2;
            const capitalNukeRange = (NUKE_RANGE * capital.value) ** 2;
            return distance <= capitalNukeRange;
        };

        return (
            standardNodeAttack(node, player) &&
            capitals.some((capital) => inCapitalRange(capital))
        );
    };
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

    // Validator that checks if a node belongs to the player
    const myNode = (data: IDItem[]): boolean => {
        const node = data[0] as Node; // Type casting to Node for TypeScript
        return node.owner === player;
    };

    // Validator that checks if either node of a dynamic edge belongs to the player
    const dynamicEdgeOwnEither = (data: IDItem[]): boolean => {
        const edge = data[0] as Edge; // Type casting to Edge for TypeScript
        return edge.dynamic && edge.from_node.owner === player;
    };

    const attackingEdge = (data: IDItem[]): boolean => {
        const edge = data[0] as Edge;
        return (
            edge.from_node.owner == player &&
            standardNodeAttack(edge.to_node, player)
        );
    };

    // Return an object mapping codes to their respective validator functions
    return {
        [KeyCodes.POISON_CODE]: attackingEdge,
        [KeyCodes.FREEZE_CODE]: dynamicEdgeOwnEither,
        [KeyCodes.ZOMBIE_CODE]: myNode,
        [KeyCodes.CANNON_CODE]: myNode,
        [KeyCodes.PUMP_CODE]: myNode,
    };
}

function newEdgeValidator(
    edges: Edge[],
    player: OtherPlayer
): ValidatorFunc {

    const newEdgeStandard = (data: Node[]): boolean => {
        if (data.length === 1) {
            const firstNode = data[0];
            return firstNode.owner === player && firstNode.is_port;
        } else {
            const firstNode = data[0];
            const secondNode = data[1];
            return (
                firstNode.id !== secondNode.id &&
                secondNode.is_port &&
                checkNewEdge(firstNode, secondNode, edges)
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
        [KeyCodes.BRIDGE_CODE]: newEdgeValidator(edges, player),
        [KeyCodes.D_BRIDGE_CODE]: newEdgeValidator(edges, player),
        [KeyCodes.BURN_CODE]: standardPortNode,
        [KeyCodes.RAGE_CODE]: noClick,
        [KeyCodes.CAPITAL_CODE]: capitalValidator(edges, player),
        [KeyCodes.NUKE_CODE]: attackValidators(nodes, player),
    };

    // Merge the validators from `player_validators` into `abilityValidators`
    const playerValidatorsMap = playerValidators(player);
    return { ...abilityValidators, ...playerValidatorsMap };
}

export function makeEventValidators(player: OtherPlayer, edges: Edge[]): {
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
            const firstNode = data[0] as Node;
            const secondNode = data[1] as Node;
            return !(secondNode.owner === player && secondNode.full) &&
            checkNewEdge(firstNode, secondNode, edges);
        }
        return false;
    }

    function pumpDrainValidator(data: IDItem[]): boolean {
        const node = data[0] as Node;
        if (data.length === 1) {
            return (
                node.owner === player &&
                node.stateName === "pump" &&
                node.full
            );
        } else if (data.length > 1) {
            const ability = data[1] as ReloadAbility;
            return ability.credits < 3;
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
        [EventCodes.PUMP_DRAIN_CODE]: pumpDrainValidator,
        [EventCodes.STANDARD_LEFT_CLICK]: edgeValidator,
        [EventCodes.STANDARD_RIGHT_CLICK]: edgeValidator,
    };
}

