# Local Dev Setup

### Client

```
cd TypeScriptFrontend/
npm run dev
```

### User Backend

```
cd UserBackend/
docker build -t user-backend.
docker run -p 5001:5001 user-backend
```

You might have to manually navigate to http://localhost:5001 and click "accept and continue" if you are getting connection issues and it is your first time setting things up.

### Game Server

```
cd Backend/
docker build -t game-server .
docker run -p 5553:5553 game-server
```

You might have to manually navigate to https://localhost:5553 and click "accept and continue" if you are getting connection issues and it is your first time setting things up.
