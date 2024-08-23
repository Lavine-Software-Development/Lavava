export interface EventVisual {
    name: string;
    desc: string;
    color: readonly [number, number, number]; 
}

export interface AbilityVisual {
    name: string;
    desc: string
    color: readonly [number, number, number]; 
    letter: string;
}

export function createEventVisual(name: string, desc: string, color: readonly [number, number, number] = [0, 0, 0]): EventVisual {
    return Object({ name, desc, color });
}

export function createAbilityVisual(name: string, desc: string, color: readonly [number, number, number] = [0, 0, 0], letter: string = ''): AbilityVisual {
    return Object({ name, desc, color, letter });
}