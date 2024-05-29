import { ClickType } from "../enums";

export class IDItem{
    id: number;
    type: ClickType;

    constructor(id: number, type: ClickType) {
        this.id = id;
        this.type = type;
    }
}



