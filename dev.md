# Running Locally

Make sure you have docker installed and runnnig and run the following commands for each server

##### User Backend

```
cd UserBackend/
docker build -t user-backend .
docker run -p 5553:5553 user-backend
```

##### Websocket Server

```
cd Backend/
docker build -t game-server .
docker run -p 5001:5001 game-server
```

# Lightsail Restarts

We host our servers on AWS Lighstail which is just a wrapper around ec2. There are two instances for each of our servers. The lightsail instances simply pull and run the docker containers you built and ran locally.

If there are any issues where you need to restart the servers, ssh into the appropriate server and run:

### User backend

```
sudo docker stop userbackend && sudo docker rm userbackend
sudo docker run -d -p 5001:5001 -v $(pwd)/game_data:/app/game_data --name userbackend akashilangovan/userbackend_deploy
```

## Game server

```
sudo docker stop gameserver && sudo docker rm gameserver
sudo docker run -p 5553:5553 --name gameserver akashilangovan/gameserver_deploy
```

Run this command after to ensure the proper container is running:

```
sudo docker ps -a
```
