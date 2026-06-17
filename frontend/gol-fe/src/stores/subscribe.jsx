import { socket } from "../hooks/socket";
import { useSimulationStore } from "../stores/store";

export default function initSocketBridge() {
    socket.subscribe((message) => {
        console.log(message);
        
        const store = useSimulationStore.getState();

        const tick = message.tick ?? 0;

        store.setGeneration(tick);
        store.setIsRunning(message.status === "running");

        if (message.grid?.birth) {
            store.applyBirthDeath(
                message.grid.birth,
                message.grid.death,
                tick
            );
        } else {
            store.setFullGrid(message.grid.grid, tick);
        }
    })
}