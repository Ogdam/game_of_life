import { useState } from "react";
import { useGameSocket } from "./hooks/useGameSocket";
import Controls from "./components/controls";
import Grid from "./components/grid";
import {cantor_calcul} from './utils/common';

function App() {
    const [generation, setGeneration] = useState(0);
    const [curentGrid, setCurentGrid] = useState(new Map());
    const [isRunning, setIsRunning] = useState(false);

    const { send } = useGameSocket(
      "ws://localhost:8000/ws",
      (message) => {
        if (!message) return;
        setGeneration(message?.tick ?? 0);
        setIsRunning(message.status === "running");
        if (message.grid?.birth) updateGridWithBirthDeath(message.grid?.birth, message.grid?.death)
        else updateFullGrid(message.grid.grid)
        console.log(curentGrid);
        }
    );

    const updateFullGrid = (grid) => {
        const newGrid = new Map()
        for (const c of grid) newGrid.set(cantor_calcul(c[0], c[1]), {'tick': generation, x:c[0], y:c[1] });
        setCurentGrid(newGrid)
    }

    const updateGridWithBirthDeath = (birth, death) => {
        for (const c of birth) curentGrid.set(cantor_calcul(c[0], c[1]), {'tick': generation, x:c[0], y:c[1] });
        for (const c of death) curentGrid.delete(cantor_calcul(c[0], c[1]));
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
                <Grid 
                    height={900} 
                    width={900}
                    grid={curentGrid}
                    generation={generation}
                    toggle_cell={(x,y) => send({ type: "toggle_cell", x:x, y:y})}
                ></Grid>
            </div>
        </>
    );
}

export default App;