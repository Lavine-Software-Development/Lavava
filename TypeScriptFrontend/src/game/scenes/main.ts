import { Node } from "../slav/Objects/node";
import { Highlight } from "../slav/highlight";
import { stateDict } from "../slav/Objects/States";
import {
    Colors,
    KeyCodes,
    NameToCode,
    stateCodes,
    EventCodes,
    GROWTH_STOP,
    AbilityCredits,
    AbilityReloadTimes,
} from "../slav/constants";
import { PlayerStateEnum as PSE } from "../slav/enums";
import { ReloadAbility } from "../slav/Objects/ReloadAbility";
import { Event } from "../slav/Objects/event";
import { AbstractAbilityManager } from "../slav/abilityManager";
import { OtherPlayer } from "../slav/Objects/otherPlayer";
import { MyPlayer } from "../slav/Objects/myPlayer";
import {
    makeEventValidators,
    unownedNode,
    makeAbilityValidators,
} from "../slav/ability_validators";
import { IDItem } from "../slav/Objects/idItem";
import { CLICKS, EVENTS, VISUALS } from "../slav/default_abilities";
import { Network } from "../slav/network";
import { random_equal_distributed_angles } from "../slav/utilities";
import { AbilityVisual } from "../slav/immutable_visuals";

import { NONE, Scene } from "phaser";
import { Edge } from "../slav/Objects/edge";
import { Main } from "../slav/Objects/parse";
import board_data from "../slav/Objects/board_data.json";
import { BoardJSON } from "../slav/Objects/parse";
export class MainScene extends Scene {
    private nodes: Node[] = [];
    private edges: Edge[] = [];
    private highlight: Highlight;
    private ps: PSE;
    private abilityManager: AbstractAbilityManager;
    private mainPlayer: MyPlayer;
    private otherPlayers: OtherPlayer[] = [];
    private network: Network;
    private burning: Node[] = [];
    private abilityCounts: { [key: string]: number };

    constructor() {
        super({ key: "MainScene" });
        this.mainPlayer = new MyPlayer("Player 1", Colors.BLUE);
        this.otherPlayers.push(this.mainPlayer);
        this.otherPlayers.push(new OtherPlayer("Player 2", Colors.RED));
        this.network = new Network("ws://localhost:5553");
        this.burning = [];
        const storedAbilities = sessionStorage.getItem('selectedAbilities');
        const abilitiesFromStorage = storedAbilities ? JSON.parse(storedAbilities) : [];

        // Create a map from ability code to count using the NameToCode mapping
        this.abilityCounts = abilitiesFromStorage.reduce((acc: { [x: string]: any; }, ability: { name: string ; count: number; }) => {
            const code = NameToCode[ability.name];
            if (code) {
                acc[code] = ability.count;
            }
            return acc;
        }, {});

        this.network.setupUser()
    }

    create(): void {
        const main = new Main();
        main.setup(board_data as BoardJSON);
        for (let i in main.nodes) {
            console.log(main.nodes[i].pos);
            let node = main.nodes[i];
            node.scene = this;
            this.nodes.push(node);
        }
        for (let i in main.edges) {
            let edge = main.edges[i];
            edge.scene = this;
            this.edges.push(edge);
        }
        this.network.connectWebSocket();
        this.highlight = new Highlight(this, this.mainPlayer.color);
        this.ps = PSE.PLAY;
        const ev = makeEventValidators(this.mainPlayer);
        const ab = makeAbilityValidators(
            this.mainPlayer,
            this.nodes,
            this.edges
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
                count,  // Use the count from abilityCounts
                1
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
        });
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
        //refresh board state
        this.checkHighlight();
        this.abilityManager.draw(this);
        this.nodes.forEach((node) => node.draw());
        this.highlight.draw();
        this.edges.forEach((edge) => edge.draw());
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
            console.log("Hovering over: ", hoverResult[0].id, hoverResult[1]);
            this.highlight.set(hoverResult[0], hoverResult[1]);
        } else {
            this.highlight.wipe();
        }
    }

    validHover(position: Phaser.Math.Vector2): [IDItem, number] | false {
        for (const node of this.nodes) {
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

        for (const edge of this.edges) {
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
        this.network.sendMessage(JSON.stringify({ code: code, items: {} }));
    }
    update_board(new_data) {
        //call parse on new data
    }
    parse(items, updates) {
        if (!items || typeof items !== "object" || Array.isArray(items)) {
            throw new Error("Invalid 'items' parameter; expected an object.");
        }
        if (!updates || typeof updates !== "object" || Array.isArray(updates)) {
            throw new Error("Invalid 'updates' parameter; expected an object.");
        }

        for (const u in updates) {
            if (!items.hasOwnProperty(u)) {
                console.error(`No item found for key ${u}`);
                continue;
            }

            let obj = items[u];
            if (typeof obj !== "object" || obj === null) {
                console.error(`Invalid item at key ${u}; expected an object.`);
                continue;
            }

            for (const [key, val] of Object.entries(updates[u])) {
                if (typeof obj[key] === "undefined") {
                    console.error(`Key ${key} not found in item ${u}.`);
                    continue;
                }

                console.log("before: " + obj[key]);
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
                console.log("updated key: ", key, " with value: ", val);
                console.log("after: " + obj[key]);
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

