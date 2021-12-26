# Stablecoin rates notifier

Tool to scrape and report the stablecoin lending rates on various platforms.

## Building

```
docker build -t stablerates .
```

## Using from Docker

```
docker run -v $(pwd)/telegram_token.txt:/telegram_token.txt pietrodn/stablerates
```
