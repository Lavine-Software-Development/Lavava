export interface EventVisual {
    name: string;
    color: readonly [number, number, number]; 
}

export interface AbilityVisual {
    name: string;
    shape: string;
    color: readonly [number, number, number]; 
    letter: string;
}

export function createEventVisual(name: string, color: readonly [number, number, number]): EventVisual {
    return Object.freeze({ name, color });
}

export function createAbilityVisual(name: string, shape: string, color: readonly [number, number, number], letter: string = ''): AbilityVisual {
    return Object.freeze({ name, shape, color, letter });
}