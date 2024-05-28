import { IDItem, Node, Edge, OtherPlayer } from "./Objects";
import { KeyCodes } from "./constants";

type ValidatorFunc = (data: IDItem[]) => boolean;

function noClick(data: IDItem[]): boolean {
    return false;
}

function standardPortNode(data: IDItem[]): boolean {
    const node = data[0] as Node;
    return node.owner !== undefined && node.isPort && node.stateName !== "mine";
}

function capitalValidator(neighbors: (node: Node) => Node[], player: OtherPlayer): ValidatorFunc {
    return function capitalLogic(data: IDItem[]): boolean {
        const node = data[0] as Node;
        if (node.owner === player && node.stateName !== "capital" && node.full) {
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

function unownedNode(data: IDItem[]): boolean {
    const node = data[0] as Node;
    return node.owner === undefined && node.stateName === "default";
}

function playerValidators(player: OtherPlayer): { [key: string]: ValidatorFunc } {

    // Validator that checks if a node is attackable
    const standardNodeAttack = (data: IDItem[]): boolean => {
        const node = data[0] as Node;  // Type casting to Node for TypeScript
        return node.owner !== player &&
               node.owner !== undefined &&
               node.stateName !== "capital" &&
               node.stateName !== "mine";
    };

    // Validator that checks if a node belongs to the player
    const myNode = (data: IDItem[]): boolean => {
        const node = data[0] as Node;  // Type casting to Node for TypeScript
        return node.owner === player;
    };

    // Validator that checks if either node of a dynamic edge belongs to the player
    const dynamicEdgeOwnEither = (data: IDItem[]): boolean => {
        const edge = data[0] as Edge;  // Type casting to Edge for TypeScript
        return edge.dynamic && (edge.fromNode.owner === player);
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

function newEdgeValidator(checkNewEdge: (firstNodeId: number, secondNodeId: number) => boolean, player: OtherPlayer): ValidatorFunc {
    const newEdgeStandard = (data: Node[]): boolean => {
        if (data.length === 1) {
            const firstNode = data[0];
            return firstNode.owner === player;
        } else {
            const firstNode = data[0];
            const secondNode = data[1];
            return firstNode.id !== secondNode.id && checkNewEdge(firstNode.id, secondNode.id);
        }
    };

    return (data: IDItem[]): boolean => {
        const nodes = data as Node[];  // Assert that all data items are Nodes
        return nodes.every(node => node.portCount > 0) && newEdgeStandard(nodes);
    };
}

function makeAbilityValidators(logic: Logic, player: OtherPlayer): {[key: string]: ValidatorFunc} {
    const abilityValidators: {[key: string]: ValidatorFunc} = {
        SPAWN_CODE: unownedNode,
        BRIDGE_CODE: newEdgeValidator(logic.checkNewEdge, player),
        D_BRIDGE_CODE: newEdgeValidator(logic.checkNewEdge, player),
        BURN_CODE: standardPortNode,
        RAGE_CODE: noClick,
        CAPITAL_CODE: capitalValidator(logic.neighbors, player)
    };

    // Merge the validators from `player_validators` into `abilityValidators`
    const playerValidatorsMap = playerValidators(player);
    return {...abilityValidators, ...playerValidatorsMap};
}
