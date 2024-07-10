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
    NUKE_RANGE,
    PlayerColors, 
} from "../objects/constants";
import { PlayerStateEnum as PSE} from "../objects/enums";
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
    abilityCountsConversion,
    phaserColor,
    random_equal_distributed_angles,
} from "../objects/utilities";
import { AbilityVisual } from "../objects/immutable_visuals";

import { NONE, Scene } from "phaser";

import { Edge } from "../objects/edge";
// import { NetworkContext } from "../NetworkContext";
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

    private graphics: Phaser.GameObjects.Graphics;
    private board: any;
    private countdown: number;
    private full_capitals: number[];
    private timerText: Phaser.GameObjects.Text;
    private capitalsText: Phaser.GameObjects.Text;
    private statusText: Phaser.GameObjects.Text;
    private eloText: Phaser.GameObjects.Text;
    private eloDifference: Phaser.GameObjects.Text;
    private leaveMatchButton: Phaser.GameObjects.Text;
    private navigate: Function;
    private userToken: string;
    private reconnectionEvent: Phaser.Time.TimerEvent | null = null;
    private isLeavingMatch: boolean = false;

    constructor(config, props, network: Network, navigate: Function) {
        super({ key: "MainScene" });
        this.board = props;
        console.log("just set board");
        console.log(config)
        console.log(this.board);
        console.log(network);
        console.log(navigate);
        this.network = network;
        this.navigate = navigate;
        this.network.updateCallback = this.update_data.bind(this);
        this.burning = [];
        const storedAbilities = sessionStorage.getItem("selectedAbilities");

        const abilitiesFromStorage = storedAbilities
            ? JSON.parse(storedAbilities)
            : [];

        // Create a map from ability code to count using the NameToCode mapping
        this.abilityCounts = abilityCountsConversion(abilitiesFromStorage);

        this.countdown = 0;
        this.full_capitals = [0, 0];
        console.log("MainScene constructor finished");
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
        this.load.image('Pump', 'Pump.png');
    }
    
    create(): void {
        console.log("CREATE called");
        this.graphics = this.add.graphics();
        
        this.initialize_data();

        this.highlight = new Highlight(this, this.mainPlayer.color);
        this.ps = PSE.START_SELECTION;
        
        this.createAbilityManager();

        this.createLeaveMatchButton();

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


        this.scale.on('resize', this.handleResize, this);

        this.startReconnectionCheck();
        this.setupBackButtonHandler();

        Object.values(this.nodes).forEach((node) => node.draw());
        Object.values(this.edges).forEach((edge) => edge.draw());

    }

    private createAbilityManager() {
        const ev = makeEventValidators(this.mainPlayer, Object.values(this.edges));
        const ab = makeAbilityValidators(
            this.mainPlayer,
            Object.values(this.nodes),
            Object.values(this.edges)
        );
        const events: { [key: number]: Event; } = {};
        const abilities: { [key: number]: ReloadAbility; } = {};
        Object.values(EventCodes).forEach((eb: number) => {
            events[eb] = new Event(
                VISUALS[eb],
                EVENTS[eb][0],
                EVENTS[eb][1],
                ev[eb]
            );
        });

        let y_position = 20;
        const squareSize = 150; // Size of each square
        const spacing = 15; // Spacing between squares
        const x_position = this.scale.width - squareSize - 10;

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
                abilityCode,
                count, // Use the count from abilityCounts
                1,
                x_position,
                y_position,
                this
            );

            y_position += squareSize + spacing;
        });

        this.abilityManager = new AbstractAbilityManager(
            this,
            abilities,
            events
        );
    }

    startReconnectionCheck(): void {
        // Clear any existing event first
        if (this.reconnectionEvent) {
            this.reconnectionEvent.remove();
        }

        // Use Phaser's time events instead of setInterval
        this.reconnectionEvent = this.time.addEvent({
            delay: 1000, // Check every 5 seconds
            callback: this.checkConnection,
            callbackScope: this,
            loop: true
        });
    }

    checkConnection(): void {
        if (!this.network.socket || this.network.socket.readyState === WebSocket.CLOSED) {
            console.log("Detected disconnection, attempting to reconnect...");
            this.network.attemptReconnect();
        }
    }

    forfeit(): void {
        console.log("Forfeiting")
        this.simple_send(stateCodes.FORFEIT_CODE);
        this.abilityManager.forfeit(this);
    }

    keydown(key: number): void {
        if (key === stateCodes.OVERRIDE_RESTART_CODE) {
            this.simple_send(stateCodes.RESTART_CODE);
        } else if (this.ps === PSE.VICTORY && key === stateCodes.RESTART_CODE) {
            this.simple_send(stateCodes.RESTART_CODE);
        } else if (this.ps === PSE.PLAY) {
            this.abilitySelection(key);
            if (key === stateCodes.FORFEIT_CODE) {
                this.simple_send(stateCodes.FORFEIT_CODE);
            }
        } else {
            console.log("Not playing");
        }
    }

    handleResize(gameSize) {
        console.log("Resizing");
    }
    

    abilitySelection(key: number): void {
        if (this.abilityManager.inAbilities(key)) {
            if (this.abilityManager.select(key)) {
                this.simple_send(key);
            }
        }
    }

    update(): void {
        this.graphics.clear();
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
                this.graphics.lineStyle(3, phaserColor(Colors.PINK), 1);
                this.graphics.strokeCircle(node.pos.x, node.pos.y, (node.value * NUKE_RANGE));
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
        if (this.ps > PSE.PLAY) {
            return;
        }
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

        if (this.ps === PSE.PLAY) {
            let ability = this.abilityManager.triangle_validate(position);
            if (ability) {
                return ability;
            }
        }

        return false;
    }

    shutdown(): void {
        // Clear the reconnection event when the scene is shut down
        this.network.disconnectWebSocket()
        if (this.reconnectionEvent) {
            this.reconnectionEvent.remove();
            this.reconnectionEvent = null;
        }
        window.removeEventListener('popstate', this.handleHistoryChange);
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
                    // console.log("event data: ", event_data);
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
        let key = this.abilityManager.clickSelect(this.input.activePointer.position);
        if (key && this.ps === PSE.PLAY) {
            this.abilitySelection(key);
        }
    }

    send(items?: number[], code?: number): void {
        this.network.sendMessage(
            this.highlight.sendFormat(items, code)
        );
    }
    simple_send(code: number): void {
        this.network.sendMessage(
            {code: code,
                items: {},
            }
        );
    }

    private setupBackButtonHandler(): void {
        window.addEventListener('popstate', this.handleHistoryChange.bind(this));
    }

    private handleHistoryChange(event: PopStateEvent): void {
        this.leaveMatchDirect();
    }

    private createLeaveMatchButton(): void {
        this.leaveMatchButton = this.add.text(10, 10, 'Forfeit', {
            fontFamily: 'Arial',
            fontSize: '20px',
            backgroundColor: this.rgbToHex(this.mainPlayer.color),
            padding: { x: 10, y: 5 },
            color: '#fff'
        });
        this.leaveMatchButton.setInteractive({ useHandCursor: true });
        this.leaveMatchButton.on('pointerdown', this.leaveMatch, this);
    }

    private leaveMatch(): void {
        if (this.ps < PSE.ELIMINATED) {
            this.forfeit();
        }
        else {
            console.log('Leaving match...');
            this.network.disconnectWebSocket();
            this.navigate("/home");
        }
    }

    private leaveMatchDirect(): void {
        if (this.ps < PSE.ELIMINATED) {
            this.forfeit();
        }
        // wait 0.2 seconds
        // setTimeout(() => {
            console.log('Leaving match...');
            // this.network.disconnectWebSocket();
            this.navigate("/home");
        // }, 200);
    }

    initialize_data(): void {
        let startData = this.board;
        const pi = Number(startData.player_id.toString());
        const pc = startData.player_count;
        const n = startData.board.nodes;
        const e = startData.board.edges;
        // const abi = startData.abilities.values;
        // const credits = startData.abilities.credits;

        this.mainPlayer = new MyPlayer(String(pi), PlayerColors[pi]);
        this.otherPlayers = Array.from({ length: pc }, (_, index) => {
            const id = index.toString();
            return id !== pi.toString() ? new OtherPlayer(id, PlayerColors[index]) : this.mainPlayer;
        })

        this.nodes = Object.fromEntries(
            Object.keys(n).map((id) => [
                id,
                new Node(
                    Number(id),
                    n[id]["pos"] as [number, number],
                    n[id]["is_port"],
                    stateDict[n[id]["state"]](),
                    n[id]["value"],
                    this
                ),
            ])
        );


        this.parse(this.edges, e);

        // 555 is default value for suggesting this abilities color should be determined by players color
        // currently only needed for spawn ability
        for (const [key, visual] of Object.entries(VISUALS)) {
            if (visual.color[0] === 555) {
                visual.color = this.mainPlayer.color;
            }
        }

}

    delete_data(): void {
        Object.values(this.nodes).forEach((node) => node.delete());
        Object.values(this.edges).forEach((edge) => edge.delete());
        this.abilityManager.delete();
        this.nodes = {};
        this.edges = {};
    }
 
    update_data(new_data) {
        if (new_data != "Players may join") {
            if (!("abilities" in new_data)) {

                if (this.ps != new_data["player"]["ps"]) {
                    this.ps = new_data["player"]["ps"] as PSE;
                    if (this.statusText) this.statusText.destroy();
                    if (this.ps >= PSE.ELIMINATED) {
                        this.leaveMatchButton.setText('Leave Match');
                    } 
                    if (this.ps > PSE.ELIMINATED) {
                        this.delete_data();
                        this.statusText = this.add.text(
                            this.sys.game.config.width as number - 100, 
                            0, 
                            `${PSE[this.ps]}`, 
                            { fontFamily: 'Arial', fontSize: '48px', color: this.rgbToHex(this.mainPlayer.color) }
                        );
                        this.statusText.setOrigin(1, 0);
                    }
                }

                if ((!this.eloText) && new_data.hasOwnProperty("new_elos")) {
                    let difference = Number(new_data["new_elos"][1]) - Number(new_data["new_elos"][0]);
                    let color = difference > 0 ? Colors.GREEN : Colors.RED;
                    let symbol = difference > 0 ? "+" : "";
                    this.eloText = this.add.text(
                        300, 
                        400, 
                        `Elo: ${new_data["new_elos"][0]} -> ${new_data["new_elos"][1]}`, 
                        { fontFamily: 'Arial', fontSize: '24px', color: '#000000' }
                    );
                    this.eloText.setOrigin(0, 0);
                    this.eloDifference = this.add.text(
                        310, 
                        360, 
                        `(${symbol}${difference})`, 
                        { fontFamily: 'Arial', fontSize: '24px', color: this.rgbToHex(color) }
                    );
                }

                if (this.countdown != new_data["countdown_timer"].toFixed(0)) {
                    // make into integer
                    this.countdown = new_data["countdown_timer"].toFixed(0);

                    if (this.timerText) this.timerText.destroy();

                    let timerColor = this.ps < PSE.PLAY ? this.mainPlayer.color : Colors.BLACK;
                    let timerWords = this.ps < PSE.PLAY ? `Choose Start: ${this.countdown}` : `Time Remaining: ${this.countdown}`;
                    this.timerText = this.add.text(
                        400, 
                        10, 
                        timerWords, 
                        { fontFamily: 'Arial', fontSize: '24px', color: this.rgbToHex(timerColor) }
                    );
                    this.timerText.setOrigin(1, 0);
                }

                if ('full_player_capitals' in new_data['board'] &&
                    this.full_capitals[this.mainPlayer.name] !== new_data['board']["full_player_capitals"][this.mainPlayer.name]) {
                    this.full_capitals = new_data['board']["full_player_capitals"];

                    if (this.capitalsText) this.capitalsText.destroy();

                    if (this.full_capitals[this.mainPlayer.name] > 0) {
                        this.capitalsText = this.add.text(
                            600, 
                            10, 
                            `Capitals: ${this.full_capitals[this.mainPlayer.name]}`, 
                            { fontFamily: 'Arial', fontSize: '24px', color: this.rgbToHex(this.mainPlayer.color) }
                        );
                        this.capitalsText.setOrigin(1, 0);
                    }
                }

                this.parse(this.nodes, new_data["board"]["nodes"], true);
                this.parse(this.edges, new_data["board"]["edges"]);
                this.parse(this.abilityManager.abilities, new_data["player"]["abilities"]);
                Object.values(this.edges).forEach((edge) => edge.draw());
            } else {
                
            }
        }
    }

    private rgbToHex(color: readonly [number, number, number]): string {
        return '#' + color.map(x => {
            const hex = x.toString(16);
            return hex.length === 1 ? '0' + hex : hex;
        }).join('');
    }

    parse(this, items, updates, redraw=false) {

        // if redraw is true and the length of updates is larger than 20, print the length of updates
        if (redraw && Object.keys(updates).length > 20) {
            console.log(Object.keys(updates).length);
        }

        for (const u in updates) {
            if (!items.hasOwnProperty(u)) {

                let new_edge = new Edge(Number(u) , this.nodes[updates[u]["from_node"]], this.nodes[updates[u]["to_node"]], updates[u]["dynamic"], this)
                this.edges[Number(u)] = new_edge;
            }

            if (updates[u] === "Deleted") {
                items[u].delete();
                delete items[u];
                continue;
            }

            let obj = items[u];
            if (typeof obj !== "object" || obj === null) {
                console.error(`Invalid item at key ${u}; expected an object.`);
                continue;
            }

            for (const [key, val] of Object.entries(updates[u])) {
                if (typeof obj[key] === "undefined") {
                    continue;
                }

                let updateVal;
                try {
                    updateVal = this.getObject(obj, key, val);
                } catch (error) {
                    console.error(
                    );
                    continue;
                }
                    obj[key] = updateVal;
                
            }
            if (redraw) {
                obj.draw();
            }
        }
    }
    getObject(object, attribute, value) {
        if (object[attribute] instanceof Node) {
            return this.nodes[value];
            
        } else if (object[attribute] instanceof Edge) {
            return this.edges[value];
            
        } else if (attribute === "owner") {
            return this.otherPlayers[value] || null;
        }
        else if (attribute === "state") {
            return stateDict[value]();
        }
        else if (attribute === "effects") {
            return new Set(value);
        }
        else {
            return value;
        }
    }
}

