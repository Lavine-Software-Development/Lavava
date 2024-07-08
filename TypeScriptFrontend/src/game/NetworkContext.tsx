import React, { createContext, ReactNode, FC } from "react";
import { Network } from "./objects/network";
import config from "../env-config";

interface MyServiceProviderProps {
    children: ReactNode;
}

const NetworkContext = createContext<Network | null>(null);

const NetworkProvider: FC<MyServiceProviderProps> = ({ children }) => {
    const networkInstance = new Network(config.gameBackend, () => {
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

