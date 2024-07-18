import { Node } from "../objects/node";
import { Highlight } from "../objects/highlight";
import { CannonState, stateDict } from "../objects/States";
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
    MINI_BRIDGE_RANGE, 
} from "../objects/constants";
import { PlayerStateEnum as PSE, GameStateEnum as GSE} from "../objects/enums";
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
    cannonAngle,
    phaserColor,
    random_equal_distributed_angles,
} from "../objects/utilities";
import { AbilityVisual } from "../objects/immutable_visuals";

import { NONE, Scene } from "phaser";

import { Edge } from "../objects/edge";
export class MainScene extends Scene {
    
    private nodes: { [key: string]: Node } = {};
    private edges: { [key: string]: Edge } = {};
    private highlight: Highlight;
    private ps: PSE;
    private gs: GSE;
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
    private eliminatedText: Phaser.GameObjects.Text;
    private eloText: Phaser.GameObjects.Text;
    private eloDifference: Phaser.GameObjects.Text;
    private leaveMatchButton: Phaser.GameObjects.Text;
    private navigate: Function;
    private reconnectionEvent: Phaser.Time.TimerEvent | null = null;
    private ratio: [number, number];

    private rainbowColors: string[] = [
        '#B8860B',  // Dark Goldenrod
        '#8B4513',  // Saddle Brown
        '#006400',  // Dark Green
        '#800000',  // Maroon
        '#4B0082'   // Indigo
    ];
    private rainbowIndex: number = 0;

    constructor(config, props, network: Network, navigate: Function) {
        super({ key: "MainScene" });
        this.board = props;
        this.network = network;
        this.navigate = navigate;
        this.network.updateCallback = this.update_data.bind(this);
        this.network.leaveGameCallback = this.leaveMatchDirect.bind(this);
        this.burning = [];
        const storedAbilities = sessionStorage.getItem("selectedAbilities");

        const abilitiesFromStorage = storedAbilities
            ? JSON.parse(storedAbilities)
            : [];

        // Create a map from ability code to count using the NameToCode mapping
        this.abilityCounts = abilityCountsConversion(abilitiesFromStorage);

        this.countdown = 0;
        this.full_capitals = [0, 0];
    }

    preload() {
        //  load ability icon assets
        this.load.setPath("assets/abilityIcons/");

        this.load.image("Bridge", "Bridge.png");
        this.load.image("Burn", "Burn.png");
        this.load.image("Cannon", "Cannon.png");
        this.load.image("Capital", "Capital.png");
        this.load.image("D-Bridge", "D-Bridge.png");
        this.load.image("Mini-Bridge", "D-Bridge.png");
        this.load.image("Freeze", "Freeze.png");
        this.load.image("Nuke", "Nuke.png");
        this.load.image("Poison", "Poison.png");
        this.load.image("Rage", "Rage.png");
        this.load.image("Spawn", "Spawn.png");
        this.load.image("Zombie", "Zombie.png");
        this.load.image('Pump', 'Pump.png');
    }
    
    create(): void {
        this.graphics = this.add.graphics();
        
        this.initialize_data();

        this.highlight = new Highlight(this, this.mainPlayer.color);
        this.ps = PSE.START_SELECTION;
        this.gs = GSE.START_SELECTION
        
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
        // this.setupNavigationHandlers();


        Object.values(this.nodes).forEach((node) => node.draw());
        Object.values(this.edges).forEach((edge) => edge.draw());

    }

    private createAbilityManager() {
        const ev = makeEventValidators(this.mainPlayer, Object.values(this.edges));
        const ab = makeAbilityValidators(
            this.mainPlayer,
            this.ratio,
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

    private getRainbowColor(): string {
        const color = this.rainbowColors[this.rainbowIndex];
        this.rainbowIndex = (this.rainbowIndex + 1) % this.rainbowColors.length;
        return color;
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

    forfeit(code: number): void {
        console.log("Forfeiting")
        this.simple_send(code);
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


    private drawScaledCircle(node: Node, radius: number, color: readonly [number, number, number]): void {
        const [ratioX, ratioY] = this.ratio;
        this.graphics.lineStyle(3, phaserColor(color), 1);
    
        // Draw the ellipse, scaling it appropriately
        this.graphics.strokeEllipse(
            node.pos.x,
            node.pos.y,
            radius * 2 * ratioX, // radus * 2 to get diameter
            radius * 2 * ratioY
        );
    }

    update(): void {
        this.graphics.clear();
        this.abilityManager.draw(this);
    
        // Iterate over the values of the dictionary to draw each node
    
        if (this.abilityManager.getMode() === KeyCodes.NUKE_CODE) {
            const capitals = Object.values(this.nodes).filter(
                (node) =>
                    node.stateName === "capital" &&
                    node.owner === this.mainPlayer
            );

            capitals.forEach((node) => {
                this.drawScaledCircle(node, node.value * NUKE_RANGE, Colors.PINK);
            });
        } else if (this.highlight.usage == KeyCodes.CAPITAL_CODE) {
            const highlightedNode = this.highlight.item as Node;
            this.drawScaledCircle(highlightedNode, highlightedNode.value * NUKE_RANGE, Colors.PINK);
        } else if (this.highlight.usage == KeyCodes.MINI_BRIDGE_CODE && this.abilityManager.clicks.length == 0)  {
            const node = this.highlight.item as Node;
            this.drawScaledCircle(node, MINI_BRIDGE_RANGE, Colors.PINK);
        } else if (this.abilityManager.getMode() == KeyCodes.MINI_BRIDGE_CODE && this.abilityManager.clicks.length > 0) {
            const node = this.abilityManager.clicks[0] as Node;
            this.drawScaledCircle(node, MINI_BRIDGE_RANGE, Colors.PINK);
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
        else { // added this else
            let key = this.abilityManager.clickSelect(this.input.activePointer.position);
            if (key && this.ps === PSE.PLAY) {
                this.abilitySelection(key);
            }
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

    // private setupNavigationHandlers(): void {
        // Handles both back navigation and tab close events
        // window.addEventListener('popstate', this.handleNavigationEvent.bind(this));
        // window.addEventListener('beforeunload', this.handleNavigationEvent.bind(this));
    // }
    
    // private handleNavigationEvent(event: PopStateEvent | BeforeUnloadEvent): void {
    //     event.preventDefault();
    //     this.leaveMatchDirect();
    // }
    

    private createLeaveMatchButton(): void {
        this.leaveMatchButton = this.add.text(10, 10, 'Forfeit', {
            fontFamily: 'Arial',
            fontSize: '20px',
            backgroundColor: this.rgbToHex(this.mainPlayer.color),
            padding: { x: 10, y: 5 },
            color: '#fff'
        });
        this.leaveMatchButton.setInteractive({ useHandCursor: true });
        this.leaveMatchButton.on('pointerdown', () => this.leaveMatch());
    }



    private leaveMatch(code: number = stateCodes.FORFEIT_CODE): void {
        if (this.ps < PSE.ELIMINATED) {
            this.forfeit(code);
        }
        else {
            this.leaveMatchDirect();
        }
    }

    private leaveMatchDirect(): void {
        console.log('Leaving match...');
        this.network.disconnectWebSocket();
        this.navigate("/home");
    }

    initialize_data(): void {

        this.ratio = [this.sys.game.config.width as number / 1000, this.sys.game.config.height as number / 700];

        let startData = this.board;
        const pi = Number(startData.player_id.toString());
        const pc = startData.player_count;
        const n = startData.board.nodes;
        const e = startData.board.edges;

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

        VISUALS[NameToCode["Spawn"]].color = this.mainPlayer.color;

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

                if (this.gs != new_data["gs"]) {
                    this.gs = new_data["gs"] as GSE;
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

                    let timerColor: string;
                    let timerWords: string;

                    if (this.ps < PSE.PLAY) {
                        timerColor = this.rgbToHex(this.mainPlayer.color);
                        timerWords = `Choose Start: ${this.countdown}`;
                    } else if (this.gs >= GSE.END_GAME) {
                        timerColor = this.getRainbowColor();
                        timerWords = `Overtime - Free Attack: ${this.countdown}`;
                    } else {
                        timerColor = this.rgbToHex(Colors.BLACK);
                        timerWords = `Standard Time: ${this.countdown}`;
                    }

                    this.timerText = this.add.text(
                        450, 
                        10, 
                        timerWords, 
                        { fontFamily: 'Arial', fontSize: '24px', color: timerColor }
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


                if ('extra_info' in new_data) {
                    new_data['extra_info'].forEach((tuple) => { this.parse_extra_info(tuple); });
                }

                this.parse(this.nodes, new_data["board"]["nodes"], true);
                this.parse(this.edges, new_data["board"]["edges"]);
                this.parse(this.abilityManager.abilities, new_data["player"]["abilities"]);
                Object.values(this.edges).forEach((edge) => edge.draw());
            } else {
                
            }
        }
    }

    private parse_extra_info(tuple: [string, any]) {
        if (tuple[0] === "cannon_shot") {
            let cannon = this.nodes[tuple[1][0]] as Node;
            let target = this.nodes[tuple[1][1]] as Node;
            this.cannonShot(cannon, target, tuple[1][2])
        }
        else if (tuple[0] == "player_elimination") {
            let player1 = tuple[1][0];
            let player2 = tuple[1][1];

            let eliminationText = this.add.text(
                this.sys.game.config.width as number / 2,
                this.sys.game.config.height as number / 2,
                `${player2} killed ${player1}`,
                { fontFamily: 'Arial', fontSize: '32px', color: '#FF0000' }
            );
            eliminationText.setOrigin(0.5);
            
            //Make the text fade out after a few seconds
            this.tweens.add({
                targets: eliminationText,
                alpha: 0,
                duration: 6000,
                ease: 'Power2',
                onComplete: () => {
                    eliminationText.destroy();
                }
            });
        }
    }

    private cannonShot(cannon: Node, target: Node, size: number) {

        cannonAngle(cannon, target.pos.x, target.pos.y);
        target.delayChange = true;

        let ball_size = 5 + Math.max(Math.log10(size / 10) / 2 + size / 1000 + 0.15, 0) * 18;
        
        // Create a Graphics object for the projectile
        const projectile = this.add.graphics();
        
        // Calculate the angle between cannon and target
        const angle = Phaser.Math.Angle.Between(cannon.pos.x, cannon.pos.y, target.pos.x, target.pos.y);
        
        // Draw the diamond-shaped projectile
        projectile.fillStyle(cannon.phaserColor, 1);
        projectile.beginPath();
        projectile.moveTo(0, -ball_size); // Top point
        projectile.lineTo(ball_size * 0.6, 0); // Right point
        projectile.lineTo(0, ball_size); // Bottom point
        projectile.lineTo(-ball_size * 0.6, 0); // Left point
        projectile.closePath();
        projectile.fillPath();
        
        // Rotate the projectile to point in the direction of travel
        projectile.rotation = angle + Math.PI / 2; // Add PI/2 because the default orientation is upward
        
        // Set the initial position to the cannon's position
        projectile.setPosition(cannon.pos.x, cannon.pos.y);
        
        // Calculate the distance between cannon and target
        const distance = Phaser.Math.Distance.Between(cannon.pos.x, cannon.pos.y, target.pos.x, target.pos.y);
        
        // Create a tween to move the projectile
        this.tweens.add({
            targets: projectile,
            x: target.pos.x,
            y: target.pos.y,
            duration: distance * 2, // Adjust this multiplier to change the speed
            ease: 'Linear',
            onComplete: () => {
                // Destroy the projectile when it reaches the target
                projectile.destroy();
                target.endDelay();
            }
        });
    }

    private rgbToHex(color: readonly [number, number, number]): string {
        return '#' + color.map(x => {
            const hex = x.toString(16);
            return hex.length === 1 ? '0' + hex : hex;
        }).join('');
    }

    parse(this, items, updates, redraw=false) {

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

