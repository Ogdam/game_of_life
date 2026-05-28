async def ws_dispatcher(app):
    while True:
        event = await app.state.event_queue.get()

        client_id = event["client_id"]
        data = event["data"]

        try: 
            await app.state.ws_manager.send(client_id, data)
        except:
            app.state.ws_manager.disconnect(client_id)
            app.state.session_manager.remove(client_id)