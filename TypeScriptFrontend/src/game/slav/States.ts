import { Colors, MineVisuals } from './constants';
import { random_equal_distributed_angles } from './utilities';  // Ensure you import the angles function

export class State {
    name: string;

    constructor(name: string) {
        this.name = name;
    }
}

export class MineState extends State {
    bubble: number;
    ringColor: readonly [number, number, number];
    unfilledColor: readonly [number, number, number];

    constructor(name: string, bubble: number, ringColor: readonly [number, number, number], unfilledColor: readonly [number, number, number] = Colors.GREY) {
        super(name);
        this.bubble = bubble;
        this.ringColor = ringColor;
        this.unfilledColor = unfilledColor;
    }
}

export class CapitalState extends State {
    capitalized: boolean;

    constructor(name: string, capitalized: boolean = false) {
        super(name);
        this.capitalized = capitalized;
    }
}

export class CannonState extends State {
    angle: number;

    constructor(name: string, angle: number = random_equal_distributed_angles(1)[0]) {
        super(name);
        this.angle = angle;
    }
}

export const stateDict: { [key: number]: State } = {
    0: new State('default'),
    1: new State('zombie'),
    2: new CapitalState('capital', true),
    3: new MineState('mine', MineVisuals.RESOURCE_BUBBLE, Colors.DARK_YELLOW),
    4: new MineState('mine', MineVisuals.ISLAND_RESOURCE_BUBBLE, Colors.YELLOW),
    5: new CannonState('cannon')
};
