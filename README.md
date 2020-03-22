# Simple flask-based API for OpenVPN server management (inside docker)

## Requirements
1. Docker
2. kylemanna/openvpn running container
3. CA **WITHOUT** password

## Running

### Start kylemanna/openvpn

There are instructions from official repo:

```
OVPN_DATA=openvpn-data
URL=<YOUR_URL>

docker volume create --name $OVPN_DATA

docker run \
    -v $OVPN_DATA:/etc/openvpn \
    --log-driver=none \
    --rm \
    kylemanna/openvpn \
    ovpn_genconfig -u udp://$URL -C 'AES-256-CBC' -a 'SHA384' -z

docker run \
    -v $OVPN_DATA:/etc/openvpn \
    --log-driver=none \
    --rm -it \
    -e EASYRSA_KEY_SIZE=2048 \
    kylemanna/openvpn \
    ovpn_initpki nopass

docker run \
    -v $OVPN_DATA:/etc/openvpn \
    -d -p 1194:1194/udp \
    --name=myvpn \
    --cap-add=NET_ADMIN \
    kylemanna/openvpn
```

### Start vpn service
Get openvpn container id (or name) using `docker ps -a`
Run API: 
```
docker run \
    -e CONTAINER=myvpn \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -p 8080:8080 \
    cr.yandex/crpnjr9i2f2ggh9opdjh/hf_vpn:latest
```

#### Danger! This container uses docker daemon sock to communicate with openvpn CLI. Use it for your own risk!
