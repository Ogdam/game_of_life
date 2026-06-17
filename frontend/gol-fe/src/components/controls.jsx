import "./controls.css";
import { useState } from "react";
import { useSimulationStore } from "../stores/store";

function Controls() {
    const start = useSimulationStore((s) => s.start);
    const stop = useSimulationStore((s) => s.stop);
    const reset = useSimulationStore((s) => s.reset);
    const isRunning = useSimulationStore((s) => s.isRunning);

    const [width, setWidth] = useState(50);
    const [height, setHeight] = useState(50);
    const [speed, setSpeed] = useState(1);

    const applyGridSize = () => {
        console.log("grid size", width, height);
    };

    const applySpeed = () => {
        console.log("speed", speed);
    };

    return (
        <div className="d-flex flex-column gap-4 p-2">

            {/* 1. PLAY CONTROLS */}
            <div className="d-flex flex-column gap-2">
                <button
                    className="btn btn-success"
                    onClick={start}
                    disabled={isRunning}
                >
                    <i className="bi bi-play-fill"></i> Start
                </button>

                <button
                    className="btn btn-warning"
                    onClick={stop}
                    disabled={!isRunning}
                >
                    <i className="bi bi-pause-fill"></i> Pause
                </button>

                <button
                    className="btn btn-danger"
                    onClick={reset}
                >
                    <i className="bi bi-arrow-counterclockwise"></i> Reset
                </button>
            </div>

            {/* 2. GRID SIZE */}
            <div className="d-flex flex-column gap-2">
                <input
                    type="number"
                    className="form-control"
                    value={width}
                    onChange={(e) => setWidth(Number(e.target.value))}
                    placeholder="Width"
                />

                <input
                    type="number"
                    className="form-control"
                    value={height}
                    onChange={(e) => setHeight(Number(e.target.value))}
                    placeholder="Height"
                />

                <button
                    className="btn btn-primary"
                    onClick={applyGridSize}
                >
                    Apply grid
                </button>
            </div>

            {/* 3. SPEED */}
            <div className="d-flex flex-column gap-2">
                <label className="form-label">
                    Speed ({speed}x)
                </label>

                <input
                    type="range"
                    className="form-range"
                    min="0.5"
                    max="2"
                    step="0.1"
                    value={speed}
                    onChange={(e) => setSpeed(Number(e.target.value))}
                />

                <button
                    className="btn btn-primary"
                    onClick={applySpeed}
                >
                    Apply speed
                </button>
            </div>

        </div>
    );
}

export default Controls;