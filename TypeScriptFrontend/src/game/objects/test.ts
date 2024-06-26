// const GameNode = require("./node");
// // const State = require("./States"); // Uncomment if needed
// const Edge = require("./edge");
// const OtherPlayer = require("./otherPlayer");
// const MyPlayer = require("./myPlayer");
// // const ClickType = require("../enums"); // Uncomment if needed
// const { PlayerColors, PORT_COUNT } = require("../constants");
// const { stateDict } = require("./States");
// const { random_equal_distributed_angles } = require("../utilities");
import { Node } from "./node";
const board_data = require("./board_data.json");
function printFibonacci(n: number): void {
    let fibArray: number[] = [0, 1];

    for (let i = 2; i < n; i++) {
        fibArray[i] = fibArray[i - 1] + fibArray[i - 2];
    }

    console.log(fibArray.join(", "));
}
printFibonacci(10);

