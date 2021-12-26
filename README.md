# Stablecoin rates notifier

Tool to scrape and report the stablecoin lending rates on various platforms.

## Building

```
docker build -t stablerates .
```

## Using from Docker

The container is deployed [on Docker Hub](https://hub.docker.com/r/pietrodn/stablerates).
```
docker run -v $(pwd)/telegram_token.txt:/telegram_token.txt pietrodn/stablerates
```

