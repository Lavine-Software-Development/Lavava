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

# Lightsail

We host our servers on AWS Lighstail which is just a wrapper around ec2. There are two instances for each of our servers. The lightsail instances simply pull and run the docker containers you built and ran locally.

If there are any issues where you need to restart the servers, ssh into the appropriate server and run:

```
sudo docker stop user-backend && sudo docker rm user-backend
docker run -p 5001:5001 --name userbackend akashilangovan/userbackend
```

or

```
sudo docker stop gameserver && sudo docker rm gameserver
docker run -p 5553:5553 --name gameserver akashilangovan/gameserver
```

The container names might have changed when people restart so run:

```
sudo docker ps -a
```

to check the current running one and run the previous command accordingly

# Deploying a new version of either backend

Go to the directory of the server you want to deploy and change the names accordingly.

```
docker build -t userbackend .
docker tag userbackend akashilangovan/userbackend
docker tag akashilangovan/userbackend
```
