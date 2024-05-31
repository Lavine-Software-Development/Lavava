import { Node } from "../slav/Objects/node";
import { Highlight } from "../slav/highlight";
import { stateDict } from "../slav/States";
import {
    Colors,
    KeyCodes,
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
import { Network } from "../slav/iansNetwork";
import { random_equal_distributed_angles } from "../slav/utilities";
import { AbilityVisual } from "../slav/immutable_visuals";

import { Scene } from "phaser";
import { Edge } from "../slav/Objects/edge";

export class MainScene extends Scene {
    private nodes: Node[] = [];
    private edges: Edge[] = [];
    private highlight: Highlight;
    private ps: PSE;
    private abilityManager: AbstractAbilityManager;
    private mainPlayer: MyPlayer;
    private otherPlayers: OtherPlayer[] = [];
    private network: Network;

    constructor() {
        super({ key: "MainScene" });
        this.mainPlayer = new MyPlayer("Player 1", Colors.BLUE);
        this.otherPlayers.push(this.mainPlayer);
        this.otherPlayers.push(new OtherPlayer("Player 2", Colors.RED));
        this.network = new Network();
    }

    create(): void {
        // Example of creating nodes
        this.nodes.push(
            new Node(
                this,
                0,
                [100, 100],
                true,
                1,
                random_equal_distributed_angles(4),
                stateDict[0],
                10,
                this.mainPlayer
            )
        );
        this.nodes.push(
            new Node(
                this,
                1,
                [200, 200],
                true,
                1,
                random_equal_distributed_angles(3),
                stateDict[0],
                GROWTH_STOP,
                this.otherPlayers[1]
            )
        );
        this.nodes.push(
            new Node(
                this,
                2,
                [300, 150],
                true,
                1,
                random_equal_distributed_angles(3),
                stateDict[0],
                10
            )
        );
        this.edges.push(
            new Edge(this, 4, this.nodes[0], this.nodes[1], true, true, false)
        );
        this.edges.push(
            new Edge(this, 5, this.nodes[1], this.nodes[2], false, true, true)
        );

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
        Object.values(KeyCodes).forEach((abk: number) => {
            abilities[abk] = new ReloadAbility(
                VISUALS[abk] as AbilityVisual,
                CLICKS[abk][0],
                CLICKS[abk][1],
                ab[abk],
                AbilityCredits[abk],
                AbilityReloadTimes[abk],
                1,
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
        this.checkHighlight();
        this.highlight.draw();
        this.abilityManager.draw(this);
        this.nodes.forEach((node) => node.draw(this));
        this.edges.forEach((edge) => edge.draw());
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
    }

    validHover(position: Phaser.Math.Vector2): [IDItem, number] | false {
        for (const node of this.nodes) {
            if (node.pos.distance(position) < 10) {
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
        this.network.pointless(this.highlight.sendFormat(items, code));
    }

    simple_send(code: number): void {
        this.network.pointless({ code: code, items: {} });
    }
}

