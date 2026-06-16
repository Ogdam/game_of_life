import { useEffect, useRef } from "react";

export function useGameSocket(url, onMessage) {
    const wsRef = useRef(null);
    const onMessageRef = useRef(onMessage);

    useEffect(() => {
        onMessageRef.current = onMessage;
    }, [onMessage]);

    useEffect(() => {
        const ws = new WebSocket(url);
        wsRef.current = ws;

        ws.onopen = () => console.log("WS connected");

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            onMessageRef.current(data);
        };

        ws.onclose = () => console.log("WS disconnected");

        return () => ws.close();
    }, [url]);

    const send = (msg) => {
        if (wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify(msg));
        }
    };

    return { send };
}