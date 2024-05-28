import asyncio
import websockets

async def ping_pong(websocket, path):
    try:
        while True:
            # Send a ping message to the client
            await websocket.send("ping")
            print("Ping sent to the client")
            
            # Wait for a pong response
            response = await websocket.recv()
            print(f"Received message from client: {response}")
            
            # Wait for 10 seconds before sending the next ping
            await asyncio.sleep(1)
    except websockets.ConnectionClosed:
        print("Connection closed by client")
    except Exception as e:
        print(f"An error occurred: {e}")

start_server = websockets.serve(ping_pong, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
