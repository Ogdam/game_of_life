from fastapi import APIRouter, Request

router = APIRouter()

# @router.get("/healthcheck")
# def start(request: Request):
#     request.app.state.controller.run()
#     return {"status":  request.app.state.controller.get_status()}

# @router .get("/sessions")
# def pause(request: Request):
#     request.app.state.controller.pause()
#     return {"status":  request.app.state.controller.get_status()}

# @router .get("/session/{client_id}")
# def reset(request: Request):
#     request.app.state.controller.reset()
#     return {"status":  request.app.state.controller.get_status()}


# @router .post("/ws/connections")
# def set_size(request: Request, height: int, width: int):
#     request.app.state.controller.game.set_size(height, width)
#     return {"grid":  request.app.state.controller.game.get_grid_state()}
