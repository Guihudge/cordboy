# CordBoy

A gameboy emulator in Discord!

**YOU MUST PROVIDE YOUR OWN LEGAL ROMS**

## Usage
### Docker
Requirment:
- Docker
- Internet Access
- GameBoy rom
- Doscord Bot Token
- A way to expose a folder to internet (appache/nginx servers for exemple)

Step 1 : Build docker image 

`docker build -t cordboy .`

Step 2 : Fill the config

```sh
cp config-sample.py config.py
nano config.py
```

Step 3 : Launch docker

```bash
docker run \
    -v ./config.py:/usr/src/app/config.py:ro \ # Config file
    -v ./roms:/usr/src/app/roms \ # default roms dir
    -v ./public:/usr/src/app/public \ # Default gif output
    cordboy
```

Step 4: Playing !

Go in your discord server, type "!gameboy" and Tada!