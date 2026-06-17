import { useEffect, useRef } from "react";

class useGameSocket {
    ws = null;
    listeners = new Set();

    connect(url) {
        if (this.ws) return;

        this.ws = new WebSocket(url);

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.listeners.forEach((fn) => fn(data));
        };
    }

    subscribe(fn) {
        this.listeners.add(fn);
        return () => this.listeners.delete(fn);
    }

    send(msg) {
        if (this.ws?.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(msg));
        }
    }
}

export const socket = new useGameSocket();