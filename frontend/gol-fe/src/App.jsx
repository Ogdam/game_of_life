import { socket } from './hooks/socket'

import SideBar from './components/sidebar'
import Grid from './components/grid'
import initSocketBridge from './stores/subscribe'
import { useSimulationStore } from './stores/store'

initSocketBridge()
socket.connect('ws://localhost:8000/ws')
useSimulationStore.getState().setSend(socket.send.bind(socket))

function App() {
  return (
    <div className="container-fluid p-0">
      <div className="row g-0 vh-100">
        <div className="col-1 bg-dark">
          <SideBar />
        </div>
        <div className="col-11 d-flex justify-content-center align-items-center bg-secondary">
          <Grid gridWidth={900} gridHeight={900}></Grid>
        </div>
      </div>
    </div>
  )
}

export default App
