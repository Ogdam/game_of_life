import "./controls.css";
import Controls from "./controls";
import { useSimulationStore } from "../stores/store";

export default function SideBar() {
    const generation = useSimulationStore((s) => s.generation);
    
    return (
        <div className="sidebar">
            <p><strong>Cornwell Game Of Life</strong></p>
            <p>{generation}</p>
            <Controls/>
        </div>
    );
}