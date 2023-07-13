# iposter
Tiny Discord bot in a Docker container for determining WAN IP address changes and notifying the owner

# Installation:
Build the docker image:
```
cd iposter
docker build -t iposter .
```

Create iposter_token.txt and paste your Discord token inside of it.

Run the container
```
docker compose up -d
```

# Notes/Quirks:
- If the container is restarted, the bot will message the owner with an IP, as the variable is stored within the script.
- The docker compose config is set to restart if the container crashes for some reason.