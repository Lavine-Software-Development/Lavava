import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import fs from "fs";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
    base: "./",
    plugins: [react()],
    server: {
        https: {
            key: fs.readFileSync(path.resolve(__dirname, "../key.pem")),
            cert: fs.readFileSync(path.resolve(__dirname, "../cert.pem")),
        },
        port: 8080,
    },
});

