import { IDItem } from "./idItem"; // Assume these are defined in the conversation// Assumed imports based on prior context
import { ClickType } from "./enums"; // Assume this is defined
import { AbilityVisual } from "./immutable_visuals"; // Assume this is defined
import { VISUALS } from "./default_abilities"; // Assume this is defined
import { Colors, KeyCodes } from "./constants";

export class Highlight {
    item: IDItem | null = null;
    usage: number | null = null;

    wipe(): void {
        this.item = null;
        this.usage = null;
    }

    get color(): readonly [number, number, number] {
        if (this.usage && this.usage !== KeyCodes.SPAWN_CODE) {
            const visual = VISUALS[this.usage] as AbilityVisual; // Assuming AbilityVisual has a color property
            return visual.color;
        }
        return Colors.GREY;
    }

    get type(): ClickType {
        if (this.item) {
            return this.item.type;
        }
        return ClickType.BLANK;
    }

    sendFormat(items?: number[], code?: number): object {
        const coda = code ?? this.usage;
        items = items || (this.item ? [this.item.id] : []);
        return { code, items };
    }

    valueOf(): boolean {
        return Boolean(this.item);
    }
}