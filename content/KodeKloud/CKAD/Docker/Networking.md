# Bridge
Default network the container is attached to

Private internal network created by the host.
All containers get an internal IP

To access any of the containers from the outside world, map the ip to the host

Another way is to associate with the `host`. This wont require any port mapping.

# None
None network containers are not attached to any network. They are an isolated network

---

How to create multiple internal network

```bash
docker network create \
	--driver bridge \
	--subnet ....
	custom-isolated-network
```

---

```bash
docker network ls
```

---

`docker inspect` to find out the network that it is attached to.

---

Container can reach each other using their name

For example, with `web` and `mysql` containers, we can use the IP. However, this is not suggested since the IP address may change on boot. Instead, use the name of the container.

---

Docker uses network namespaces that creates a separate namespaces for each container.

Uses virtual network ethernet to connect to each other.