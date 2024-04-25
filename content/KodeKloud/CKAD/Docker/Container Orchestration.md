- Docker runs a single instance of the application with `docker run` command on a single docker host

**What if the users of the application increases and a single instance is not sufficient to handle the load?**

Need to deploy additional instances.

**What if the container fails?**
Detect the failed instance and run `docker run`

**What if the host crashes?**
All the containers hosted on the Docker host becomes unavailable too.

---

For a large application with 10s - 1000s of containers, it is no longer feasible to manage these containers manually.

---

>[!note]
>A set of tools and scripts that can help host containers in a production environment
>
>Consists of multiple docker host that can host containers

Easily allow you to deploy thousands of instances with a single command.
- Scaling with number of users
- Adding additional hosts on additional load
- Advanced networking between containers across different hosts
- Sharing storage between hosts
- Config management and security

There are various container orchestration tools:
1. Docker swarm
	1. Lacks advanced features
2. Kubernetes
	1. A lot of options for config
	2. Support from a lot of cloud providers
3. Mesos
	1. Difficult to set up and get started

---

# Docker Swarm

> An introduction to Docker swarm

With Docker swarm, combine multiple Docker machines into a single cluster.

Docker manages distributing your services into separate hosts for high availability and load balancing.

1. Set up multiple Docker host
2. Designate 1 host as the `SwarmManager`
	1. `docker swarm init`
3. Remaining Docker hosts join the swarm –> becomes a worker node

## Docker services
- One or more instances of a single application that runs across the nodes in the swarm cluster
- `docker service create --replicas=3 my-application` run on `SwarmManager`
- Get 3 instances of `my-application` on 3 Docker host

---

# Basic Kubernetes
