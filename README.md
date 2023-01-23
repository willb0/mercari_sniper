# mercari-sniper

my project to build a mercari JP scraper/notification system

setup:
```sh
docker compose build
docker compose up
```

youll have search api at `0.0.0.0:80/docs`
UI to search it @ `0.0.0.0:81`


You also need to have twilio creds to run the backend with text notifs.
Add your client id and secret to the docker-compose file under environment for the backend
