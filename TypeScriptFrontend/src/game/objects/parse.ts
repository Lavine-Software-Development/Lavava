import { Node } from "./node";
import { Edge } from "./edge";
import { OtherPlayer } from "./otherPlayer";
import { MyPlayer } from "./myPlayer";
import { PlayerColors, PORT_COUNT } from "./constants";
import { stateDict } from "./States";
import { random_equal_distributed_angles } from "./utilities";
import { Scene } from "phaser";
import nodeData from "../data/nodeData.json";
interface NodeData {
    effects: any[]; // Define the type for effects if known, 'any' is a placeholder
    is_port: boolean;
    pos: number[];
    state: number;
    value: number;
}
interface Indexnode {
    [key: string]: NodeData;
}
// Define the Edge interface
interface EdgeData {
    dynamic: boolean;
    from_node: number;
    to_node: number;
}

interface Indexedge {
    [key: string]: EdgeData;
}

// Define the Abilities interface for individual ability
interface Ability {
    credits: number;
    reload: number;
}

// Define the Abilities storage structure
interface Abilities {
    values: { [key: string]: Ability };
    credits: number;
}

// Define the Board interface
interface Board {
    edges: { [key: string]: EdgeData };
    nodes: { [key: string]: NodeData };
}

// Define the main Game interface
export interface BoardJSON {
    board: Board;
    player_count: number;
    player_id: number;
    abilities: Abilities;
}

// Example JSON object based on these interfaces
export class Main {
    // ps: string;
    // timer: number;
    // highlight: Highlight;
    // effectVisuals: { [key: string]: any } = {};
    // canDraw: boolean = false;
    myPlayer: any;
    players: { [key: string]: any };
    nodes: { [key: string]: any };
    edges: { [key: string]: any };

    constructor() {}

    settings(): [any, number] {
        // Placeholder: replace with actual settings retrieval logic
        return [{}, 8080];
    }
    test(node: NodeData) {
        return node;
    }
    setup(startData: BoardJSON): void {
        this.test(nodeData["0"] as NodeData);
        console.log(startData);
        if (
            startData &&
            startData.board &&
            startData.board.nodes &&
            startData.board.edges &&
            startData.player_count &&
            // startData.player_id &&
            startData.abilities
        ) {
            console.log("trying to parse");
            const pi = Number(startData.player_id.toString());
            console.log("pi: ", pi);
            const pc = startData.player_count;
            const n = startData.board.nodes;
            const e = startData.board.edges;
            // const abi = startData.abilities.values;
            // const credits = startData.abilities.credits;

            this.myPlayer = new MyPlayer(String(pi), PlayerColors[pi]);
            this.players = Object.fromEntries(
                [...Array(pc).keys()]
                    .filter((id) => id !== pi)  // Use strict equality
                    .map((id) => [
                        String(id),  // Convert to string to be consistent
                        new OtherPlayer(
                            String(id),
                            PlayerColors[id]
                        ),
                    ])
            );
            const scene = new Scene();
            this.players[String(pi)] = this.myPlayer;  // Use string key
            this.players[pi] = this.myPlayer;
            console.log(this.players);
            this.nodes = Object.fromEntries(
                Object.keys(n).map((id) => [
                    id,
                    new Node(
                        Number(id),
                        n[id]["pos"] as [number, number],
                        n[id]["is_port"],
                        0.0, // Placeholder: replace with actual value of portPercent
                        n[id]["is_port"]
                            ? random_equal_distributed_angles(PORT_COUNT)
                            : [],
                        stateDict[n[id]["state"]](),
                        n[id]["value"],
                        null,
                        new Set(),
                        // scene
                    ),
                ])
            );

            this.edges = Object.fromEntries(
                Object.keys(e).map((id) => [
                    id,
                    new Edge(
                        Number(id),
                        this.nodes[e[id]["from_node"]],
                        this.nodes[e[id]["to_node"]],
                        e[id]["dynamic"]
                    ),
                ])
            );
        } else {
            console.log("not here");
        }
    }
}

