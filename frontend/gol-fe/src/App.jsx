import { useState } from "react";
import { useGameSocket } from "./hooks/useGameSocket";
import Controls from "./components/controls";
import Grid from "./components/grid";

function App() {
    const [generation, setGeneration] = useState(0);
    const [grid, setGrid] = useState({});
    const [curentGrid, setCurentGrid] = useState(new Map());
    const [isRunning, setIsRunning] = useState(false);

    const { send } = useGameSocket(
      "ws://localhost:8000/ws",
      (message) => {
        if (!message) return;
        
        setGrid(message.grid);
        setGeneration(message?.tick ?? 0);
        setIsRunning(message.status === "running");
        if (grid?.birth) updateGrid()
        
    }
    );

    const updateGrid = () => {
        for (const c of grid?.birth) curentGrid.set(cantor_calcul(c), generation);
        for (const c of grid?.death) curentGrid.delete(cantor_calcul(c));
    }

    const reset = () => {
        send({ type: "reset" });
        setCurentGrid(new Map());
    }

    return (
        <>
            <h1>Generation {generation}</h1>
            <Controls
                isRunning={isRunning}
                onStart={() => send({ type: "start" })}
                onPause={() => send({ type: "stop" })}
                onReset={() => reset()}
            />
            <div>
                <Grid></Grid>
            </div>
        </>
    );
}

export default App;