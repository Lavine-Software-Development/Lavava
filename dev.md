# Local Dev Setup

### Client

```
cd TypeScriptFrontend/
npm run dev
```

### Servers

```
cd Lavava/
docker-compose up --build
```

You might have to manually navigate to http://localhost:5001 and click "accept and continue" if you are getting
issues logging in.

Once you click "accept and continue" you will see a 404 not found page. This means this worked and you can go back to the client to test if login etc. works.

You might also have to manually navigate to https://localhost:5553 and click "accept and continue" if you are having issues starting games.

Once you click "accept and continue" you should see a "failed to open Websocket connection" message. This means this step works and you can go back to the client to start a game.
