import "./controls.css";

function Controls({
    onStart,
    onPause,
    onReset,
    isRunning,
}) {
    
    return (
        <div className="controls">
            <button
                onClick={onStart}
                disabled={isRunning}
            >
                Start
            </button>

            <button
                onClick={onPause}
                disabled={!isRunning}
            >
                Pause
            </button>

            <button onClick={onReset}>
                Reset
            </button>
        </div>
    );
}

export default Controls;