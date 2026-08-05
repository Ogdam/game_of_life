import './controls.css'
import Controls from './controls'
import { useSimulationStore } from '../stores/store'

export default function SideBar() {
  const generation = useSimulationStore((s) => s.generation)

  return (
    <div className="sidebar">
      <div className="d-flex flex-column gap-2 text-center">
        <p>
          <strong>Cornwell Game Of Life</strong>
        </p>
        <p>{generation}</p>
      </div>
      <Controls />
    </div>
  )
}
