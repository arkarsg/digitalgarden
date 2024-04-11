Docker engine refers to Docker installed on the host.

There are 3 parts

- Docker CLI
- REST API
- Docker Daemon

Docker Daemon manages containers, images, volumes and networks.

You can access a remote Docker engine

```bash
docker -H=remote-docker-engine:2375 run nginx
```

## How are applications containerized?

Uses namespace to isolate containers. This isolates:
1. Process ID
2. Network
3. InterProcess communication
4. Mount
5. Unix timesharing

## Docker storage
By default, Docker stores files related to containers and images in:

```
/var/lib/docker
	aufs
	containers
	image
	volumes
```

### Layers
Each line of instruction creates a new layer. If there are layers that are the same, it uses layers from the cache to rebuild and update