import './controls.css'
import Controls from './controls'
import { useSimulationStore } from '../stores/store'

export default function SideBar() {
  const generation = useSimulationStore((s) => s.generation)

  return (
    <div className="gol-sidebar d-flex flex-column gap-4 p-2">
      <div className="gol-sidebar-header d-flex flex-column gap-1 text-center">
        <p className="gol-sidebar-title">Cornwell Game Of Life</p>
        <p className="m-0">{generation}</p>
      </div>
      <Controls />
    </div>
  )
}
