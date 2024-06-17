import { Node } from "../objects/node";
import { Highlight } from "../objects/highlight";
import { stateDict } from "../objects/States";
import {
    Colors,
    KeyCodes,
    NameToCode,
    stateCodes,
    EventCodes,
    GROWTH_STOP,
    AbilityCredits,
    AbilityReloadTimes,
} from "../objects/constants";
import { PlayerStateEnum as PSE, PlayerStateEnum } from "../objects/enums";
import { ReloadAbility } from "../objects/ReloadAbility";
import { Event } from "../objects/event";
import { AbstractAbilityManager } from "../objects/abilityManager";
import { OtherPlayer } from "../objects/otherPlayer";
import { MyPlayer } from "../objects/myPlayer";
import {
    makeEventValidators,
    unownedNode,
    makeAbilityValidators,
} from "../objects/ability_validators";
import { IDItem } from "../objects/idItem";
import { CLICKS, EVENTS, VISUALS } from "../objects/default_abilities";
import { Network } from "../objects/network";
import {
    phaserColor,
    random_equal_distributed_angles,
} from "../objects/utilities";
import { AbilityVisual } from "../objects/immutable_visuals";

import { NONE, Scene } from "phaser";
import { Edge } from "../objects/edge";
import { Main } from "../objects/parse";
import board_data from "../data/board_data.json";
import { BoardJSON } from "../objects/parse";
export class MainScene extends Scene {
    private nodes: { [key: string]: Node } = {};
    private edges: { [key: string]: Edge } = {};
    private highlight: Highlight;
    private ps: PSE;
    private abilityManager: AbstractAbilityManager;
    private mainPlayer: MyPlayer;
    private otherPlayers: OtherPlayer[] = [];
    private network: Network;
    private burning: Node[] = [];
    private abilityCounts: { [key: string]: number };
    private timer: number;
    private playerCount: number;
    private gameType: string;
    private graphics: Phaser.GameObjects.Graphics;
    private board: BoardJSON;

    constructor(config, props) {
        super({ key: "MainScene" });
        console.log("config: ", config);
        console.log("props yeaaa: ", props);
        this.board = props;
        this.mainPlayer = new MyPlayer("Player 1", Colors.BLUE);
        this.otherPlayers.push(this.mainPlayer);
        this.otherPlayers.push(new OtherPlayer("Player 2", Colors.RED));
        this.network = new Network(
            "ws://localhost:5553",
            this.update_board.bind(this)
        );
        this.burning = [];
        const storedAbilities = sessionStorage.getItem("selectedAbilities");
        this.gameType = String(sessionStorage.getItem("type"));
        this.playerCount = Number(sessionStorage.getItem("player_count")) || 0;
        const abilitiesFromStorage = storedAbilities
            ? JSON.parse(storedAbilities)
            : [];

        // Create a map from ability code to count using the NameToCode mapping
        this.abilityCounts = abilitiesFromStorage.reduce(
            (
                acc: { [x: string]: any },
                ability: { name: string; count: number }
            ) => {
                const code = NameToCode[ability.name];
                if (code) {
                    acc[code] = ability.count;
                }
                return acc;
            },
            {}
        );
    }

    preload() {
        //  load ability icon assets
        this.load.setPath("assets/abilityIcons/");

        this.load.image("Bridge", "Bridge.png");
        this.load.image("Burn", "Burn.png");
        this.load.image("Cannon", "Cannon.png");
        this.load.image("Capital", "Capital.png");
        this.load.image("D-Bridge", "D-Bridge.png");
        this.load.image("Freeze", "Freeze.png");
        this.load.image("Nuke", "Nuke.png");
        this.load.image("Poison", "Poison.png");
        this.load.image("Rage", "Rage.png");
        this.load.image("Spawn", "Spawn.png");
        this.load.image("Zombie", "Zombie.png");
    }
    create(): void {
        this.graphics = this.add.graphics();
        const main = new Main();
        main.setup(this.board);
        for (let i in main.nodes) {
            // console.log(main.nodes[i].pos);
            let node = main.nodes[i];
            // randomly select an owner from the other players
            // node.owner =
            //     this.otherPlayers[
            //         Math.floor(Math.random() * this.otherPlayers.length)
            //     ];
            node.scene = this;
            // node.owner = this.mainPlayer;
            this.nodes[i] = node;
        }
        for (let i in main.edges) {
            let edge = main.edges[i];
            edge.scene = this;
            this.edges[i] = edge;
        }
        this.highlight = new Highlight(this, this.mainPlayer.color);
        this.ps = PSE.START_SELECTION;
        const ev = makeEventValidators(this.mainPlayer);
        const ab = makeAbilityValidators(
            this.mainPlayer,
            Object.values(this.nodes),
            Object.values(this.edges)
        );
        const events: { [key: number]: Event } = {};
        const abilities: { [key: number]: ReloadAbility } = {};
        Object.values(EventCodes).forEach((eb: number) => {
            events[eb] = new Event(
                VISUALS[eb],
                EVENTS[eb][0],
                EVENTS[eb][1],
                ev[eb]
            );
        });

        Object.entries(this.abilityCounts).forEach(([abk, count]) => {
            // abk here is the ability code (converted from the name via NameToCode)
            const abilityCode = parseInt(abk); // Ensure the key is treated as a number if needed

            abilities[abilityCode] = new ReloadAbility(
                VISUALS[abilityCode] as AbilityVisual,
                CLICKS[abilityCode][0],
                CLICKS[abilityCode][1],
                ab[abilityCode],
                AbilityCredits[abilityCode],
                AbilityReloadTimes[abilityCode],
                count, // Use the count from abilityCounts
                1,
                this
            );
        });

        this.abilityManager = new AbstractAbilityManager(
            this,
            abilities,
            events
        );

        this.input.on("pointerdown", (pointer: Phaser.Input.Pointer) => {
            if (pointer.leftButtonDown()) {
                this.mouseButtonDownEvent(EventCodes.STANDARD_LEFT_CLICK);
            } else if (pointer.rightButtonDown()) {
                this.mouseButtonDownEvent(EventCodes.STANDARD_RIGHT_CLICK);
            }
        });

        this.input.keyboard!.on("keydown", (event: KeyboardEvent) => {
            this.keydown(event.key.charCodeAt(0));
            this.checkHighlight();
        });

        this.input.on("pointermove", (pointer: Phaser.Input.Pointer) => {
            this.checkHighlight();
        });
        Object.values(this.nodes).forEach((node) => node.draw());
        Object.values(this.edges).forEach((edge) => edge.draw());
        this.network.connectWebSocket();
        this.network.setupUser(this.abilityCounts);
    }

    keydown(key: number): void {
        if (key === stateCodes.OVERRIDE_RESTART_CODE) {
            this.simple_send(stateCodes.RESTART_CODE);
        } else if (this.ps === PSE.VICTORY && key === stateCodes.RESTART_CODE) {
            this.simple_send(stateCodes.RESTART_CODE);
        } else if (this.ps === PSE.PLAY) {
            if (this.abilityManager.inAbilities(key)) {
                if (this.abilityManager.select(key)) {
                    this.simple_send(key);
                }
            } else if (key === stateCodes.FORFEIT_CODE) {
                this.simple_send(stateCodes.FORFEIT_CODE);
            }
        } else {
            console.log("Not playing");
        }
    }

    update(): void {
        this.abilityManager.draw(this);

        // Iterate over the values of the dictionary to draw each node

        if (this.abilityManager.ability?.visual.name == "Nuke") {
            // Filter the dictionary values to find the capitals
            const capitals = Object.values(this.nodes).filter(
                (node) =>
                    node.stateName === "capital" &&
                    node.owner === this.mainPlayer
            );

            // For each node in capitals, draw a pink hollow circle on the node of the size of its this.value
            capitals.forEach((node) => {
                this.graphics.lineStyle(6, phaserColor(Colors.PINK), 1);
                this.graphics.strokeCircle(
                    node.pos.x,
                    node.pos.y,
                    node.size + 4
                );
            });
        }
    }

    tick(): void {
        this.burning = this.burning.filter((node) => !node.burn());
    }

    addToBurn(node: Node): void {
        this.burning.push(node);
    }

    checkHighlight(): void {
        let pointer = this.input.activePointer;
        let hoverResult = this.validHover(
            new Phaser.Math.Vector2(pointer.x, pointer.y)
        );

        if (hoverResult !== false) {
            this.highlight.set(hoverResult[0], hoverResult[1]);
        } else {
            this.highlight.wipe();
        }
        this.highlight.draw();
    }

    validHover(position: Phaser.Math.Vector2): [IDItem, number] | false {
        for (const node of Object.values(this.nodes)) {
            if (node.pos.distance(position) < node.size) {
                // Assuming a proximity check
                if (this.ps === PSE.START_SELECTION) {
                    if (unownedNode([node])) {
                        return [node, KeyCodes.SPAWN_CODE];
                    }
                } else if (this.ps === PSE.PLAY) {
                    let validation = this.abilityManager.validate(node);
                    if (validation) {
                        return validation;
                    }
                }
            }
        }

        for (const edge of Object.values(this.edges)) {
            if (edge.isNear(position)) {
                // You need to define how to check proximity to an edge
                if (this.ps === PSE.PLAY) {
                    return this.abilityManager.validate(edge);
                }
            }
        }

        return false;
    }

    mouseButtonDownEvent(button: number): void {
        if (this.highlight.highlighted) {
            if (this.ps === PSE.START_SELECTION) {
                this.send();
            } else {
                if (this.abilityManager.useAbility(this.highlight)) {
                    const completion = this.abilityManager.completeAbility();
                    if (completion !== false) {
                        this.send(completion);
                    }
                } else {
                    const event_data = this.abilityManager.useEvent(
                        this.highlight
                    );
                    console.log("event data: ", event_data);
                    if (event_data !== false) {
                        if (
                            button === EventCodes.STANDARD_RIGHT_CLICK &&
                            this.highlight.usage ===
                                EventCodes.STANDARD_LEFT_CLICK
                        ) {
                            this.send(
                                event_data,
                                EventCodes.STANDARD_RIGHT_CLICK
                            );
                        } else {
                            this.send(event_data);
                        }
                    }
                }
            }
        }
    }

    send(items?: number[], code?: number): void {
        this.network.sendMessage(
            JSON.stringify(this.highlight.sendFormat(items, code))
        );
    }
    simple_send(code: number): void {
        console.log("trying to send simple message", code);
        this.network.sendMessage(
            JSON.stringify({
                code: code,
                items: {},
            })
        );
    }

    update_board(new_data) {
        // console.log("update");
        if (new_data != "Players may join") {
            // console.log(new_data);
            // new_data = JSON.parse(new_data);
            if (!("abilities" in new_data)) {
                // this.ps = new_data["player"]["ps"];
                // console.log("after");
                this.timer = new_data["countdown_timer"];
                this.parse(this.nodes, new_data["board"]["nodes"]);
                this.parse(this.edges, new_data["board"]["edges"]);
            } else {
                // console.log(new_data);
            }
        }
    }

    parse(this, items, updates) {
        for (const u in updates) {
            // console.log("here");
            if (!items.hasOwnProperty(u)) {
                console.error(`No item found for key ${u}`);
                continue;
            }

            let obj = items[u];
            // console.log("obj: ", obj, " key: ", u, " updates: ", updates[u]);
            if (typeof obj !== "object" || obj === null) {
                console.error(`Invalid item at key ${u}; expected an object.`);
                continue;
            }

            for (const [key, val] of Object.entries(updates[u])) {
                if (typeof obj[key] === "undefined") {
                    console.error(`Key ${key} not found in item ${u}.`);
                    continue;
                }

                // console.log("before: " + obj[key]);
                let updateVal;
                try {
                    updateVal = this.getObject(obj, key, val);
                } catch (error) {
                    console.error(
                        `Error updating key ${key} in item ${u}: ${error.message}`
                    );
                    continue;
                }

                obj[key] = updateVal;
                // console.log("updated key: ", key, " with value: ", val);
                // console.log("after: " + obj[key]);
            }
        }
    }
    getObject(object, attribute, value) {
        if (object[attribute] instanceof Node) {
            return this.nodes[value];
        } else if (object[attribute] instanceof Edge) {
            return this.edges[value];
        }
        //TODO: check for State and OtherPlayer types after adding those
        else {
            return value;
        }
    }
}

