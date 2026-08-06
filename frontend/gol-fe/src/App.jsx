import { socket } from './hooks/socket'

import SideBar from './components/sidebar'
import Grid from './components/grid'
import initSocketBridge from './stores/subscribe'
import { useSimulationStore } from './stores/store'
import './App.css'

initSocketBridge()
socket.connect('ws://localhost:8000/ws')
useSimulationStore.getState().setSend(socket.send.bind(socket))

function App() {
  return (
    <div className="container-fluid p-0">
      <div className="row g-0 flex-column flex-md-row min-vh-100">
        <div className="col-12 col-md-4 col-lg-3 col-xl-2 gol-sidebar-col">
          <SideBar />
        </div>
        <div className="col-12 col-md-8 col-lg-9 col-xl-10 d-flex justify-content-center align-items-center gol-stage-col">
          <Grid gridWidth={900} gridHeight={900}></Grid>
        </div>
      </div>
    </div>
  )
}

export default App
