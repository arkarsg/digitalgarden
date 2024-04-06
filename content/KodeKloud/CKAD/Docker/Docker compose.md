We want to run multiple containers as services.

Instead of `docker run` multiple times,

```yml
services:
	web:
		image: <image>
	database:
		image: <image>
	messaging:
		image: <image>
	orchestration:
		image: <image>
```

Then,
```bash
docker-compose up
```

All the services run within the same Docker host.

---

