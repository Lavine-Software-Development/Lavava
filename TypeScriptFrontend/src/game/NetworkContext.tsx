import React, { createContext, ReactNode, FC } from "react";
import { Network } from "./objects/network";

interface MyServiceProviderProps {
    children: ReactNode;
}

const NetworkContext = createContext<Network | null>(null);

const NetworkProvider: FC<MyServiceProviderProps> = ({ children }) => {
    const networkInstance = new Network("http://3.142.142.56:5553", () => {
        console.log("Callback function not yet configured");
    });
    // networkInstance.connectWebSocket();

    return (
        <NetworkContext.Provider value={networkInstance}>
            {children}
        </NetworkContext.Provider>
    );
};

export { NetworkContext, NetworkProvider };

