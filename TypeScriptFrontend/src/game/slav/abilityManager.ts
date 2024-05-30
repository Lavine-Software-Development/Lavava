import { ReloadAbility } from "./Objects/ReloadAbility";
import { IDItem } from "./Objects/idItem";
import { Highlight } from "./highlight";
import { Event } from "./Objects/event";

export class AbstractAbilityManager {
    private abilities: { [key: number]: ReloadAbility };
    private events: { [key: number]: Event };
    private mode: number | null = null;
    private backupMode: number | null = null;
    private clicks: IDItem[] = [];

    constructor(abilities: { [key: number]: ReloadAbility }, events: { [key: number]: Event }) {
        this.abilities = abilities;
        this.events = events;
    }

    inAbilities(key: number): boolean {
        return key in this.abilities;
    }

    useEvent(highlight: Highlight): number[] | false {
        if (this.mode && this.mode !== highlight.usage) {
            this.backupReset();
        }
        this.mode = highlight.usage;
        this.clicks.push(highlight.item!);  // Assuming item is always present
        if (this.completeCheck(highlight.usage)) {
            const clicks = this.clicks.map(click => click.id);
            this.backupReset();
            return clicks;
        }
        return false;
    }

    useAbility(highlight: Highlight): boolean {
        if (this.ability && highlight.usage === this.mode && highlight.type === this.ability.clickType && highlight.item) {
            this.clicks.push(highlight.item);
            return true;
        }
        return false;
    }

    completeAbility(): number[] | false {
        if (this.completeCheck()) {
            const clicks = this.clicks.map(click => click.id);
            this.reset();
            return clicks;
        }
        return false;
    }

    backupReset(): void {
        if (this.backupMode) {
            this.mode = this.backupMode;
            this.backupMode = null;
            this.wipe();
        } else {
            if (this.ability) {
                this.backupMode = this.mode;
            }
            this.reset();
        }
    }

    reset(): void {
        this.wipe();
        this.mode = null;
    }

    wipe(): void {
        this.clicks = [];
    }

    switchTo(key: number): boolean {
        this.mode = key;
        if (this.completeCheck()) {
            this.reset();
            return true;
        }
        return false;
    }

    completeCheck(event?: number | null): boolean {
        if (this.ability) {
            return this.ability.clickCount === this.clicks.length;
        } else if (event) {
            return this.events[event].clickCount === this.clicks.length;
        }
        console.error("ERROR, No ability or event");
        return false;
    }

    select(key: number): boolean {
        if (this.mode) {
            this.wipe();
        }
        if (this.mode === key) {
            this.mode = null;
        } else if (this.abilities[key].selectable) {
            return this.switchTo(key);
        }
        return false;
    }

    validate(item: IDItem): [IDItem, number] | false {
        if (this.event && item.type === this.event.clickType && this.event.verificationFunc(this.clicks.concat([item]))) {
            return [item, this.mode!];  // Assuming mode is set
        } else if (this.ability && item.type === this.ability.clickType && this.ability.verificationFunc(this.clicks.concat([item]))) {
            return [item, this.mode!];  // Assuming mode is set
        } else {
            for (const code in this.events) {
                const ev = this.events[code];
                if (item.type === ev.clickType && ev.verificationFunc([item])) {
                    return [item, parseInt(code)];
                }
            }
        }
        return false;
    }

    get ability(): ReloadAbility | null {
        if (this.mode !== null && this.abilities[this.mode]) {
            return this.abilities[this.mode];
        }
        return null;
    }

    get event(): Event | null {
        if (this.mode !== null && this.events[this.mode]) {
            return this.events[this.mode];
        }
        return null;
    }
}
