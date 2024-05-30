import { Node } from '../slav/Objects/node';
import { Highlight } from '../slav/highlight';
import { stateDict } from '../slav/States';
import { KeyCodes, stateCodes } from '../slav/constants';
import { PlayerStateEnum as PSE } from '../slav/enums';
import { ReloadAbility } from '../slav/Objects/ReloadAbility';
import { Event } from '../slav/Objects/event';
import { AbstractAbilityManager } from '../slav/abilityManager';

import { Scene } from 'phaser';


export class MainScene extends Scene {
    private nodes: Node[] = [];
    private highlight: Highlight;
    private ps: PSE;
    private abilityManager: AbstractAbilityManager;

    constructor(abilities: { [key: number]: ReloadAbility }, events: { [key: number]: Event }) {
        super({ key: 'MainScene' });
        this.abilityManager = new AbstractAbilityManager(abilities, events);
    }

    create(): void {
        // Example of creating nodes
        this.nodes.push(new Node(1, [100, 100], false, 0, [], stateDict[0], 10));
        this.nodes.push(new Node(1, [200, 200], true, 0, [], stateDict[0], 10));
        this.highlight = new Highlight(this);
        this.ps = PSE.START_SELECTION;


        this.input.on('pointerdown', (pointer: Phaser.Input.Pointer) => {
            if (pointer.leftButtonDown()) {
                this.mouseButtonDownEvent(KeyCodes.STANDARD_LEFT_CLICK);
            } else if (pointer.rightButtonDown()) {
                this.mouseButtonDownEvent(KeyCodes.STANDARD_RIGHT_CLICK); 
            }
        });

        this.input.keyboard!.on('keydown', (event: KeyboardEvent) => {
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

        this.nodes.forEach(node => node.draw(this));
        this.highlight.draw();
    }

    checkHighlight(): void {
        let pointer = this.input.activePointer;
        let found = false;
        this.nodes.forEach(node => {
            if (node.pos.distance(new Phaser.Math.Vector2(pointer.x, pointer.y)) < 10) {
                this.highlight.set(node, KeyCodes.SPAWN_CODE);
                found = true;
            }
            if (!found) {
                this.highlight.wipe();
            }
        });
    }

    mouseButtonDownEvent(button: number): void {
        if (this.highlight.highlighted) {

            if (this.ps === PSE.START_SELECTION) {
                this.send(this.highlight.sendFormat());
            } else {
                if (this.abilityManager.useAbility(this.highlight)) {
                    const completion = this.abilityManager.completeAbility();
                    if (completion !== false) {
                        this.send(this.highlight.sendFormat(completion));
                }
                } else {
                    const event_data = this.abilityManager.useEvent(this.highlight);
                    if (event_data !== false) {
                        if (button === KeyCodes.STANDARD_RIGHT_CLICK && this.highlight.usage === KeyCodes.STANDARD_LEFT_CLICK) {
                            this.send(this.highlight.sendFormat(event_data, KeyCodes.STANDARD_RIGHT_CLICK));
                        } else {
                            this.send(this.highlight.sendFormat(event_data));
                        }
                    }
                }
            }
        }
    }

    send(str: any): void {
       
    }

    simple_send(str: any): void {

    }
}
