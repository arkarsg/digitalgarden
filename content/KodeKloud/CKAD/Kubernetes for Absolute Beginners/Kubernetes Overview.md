# Overview of Kubernetes
- Built by Google from their experience in running containers
- Popular open source container orchestration

## Containers
[Docker](Introduction%20to%20Docker.md) is one of the most popular container technology

>[!note] Recap
>Suppose we want to build an end-to-end application with Node.js, MongoDB database, Redis messaging and Ansible orchestration
>- These applications have different compatibilities with the OS.
>- There are also issues with dependencies, where a component is compatible with a version of a library but not another component.
>- This leads to *matrix from hell*
>- How to set up developer environment quickly (different OS → different environment)

Docker allows you to run each component as a separate container (environment) regardless of the OS and VM that is being run on.

>[!note] Containers are completely isolated environments
>Shares the same OS kernel but have isolated processes, networks, and mounts
>
>As long as the Docker container is based on a distribution that is the same as the OS kernel, it is okay.

>[!caution] Compared to VMs
>Docker is a software on top of the underlying OS. In the case of VMs, there is a hypervisor on top of the OS, which in turn, has their own OS.
>
>VMs are larger (GB) in size and takes longer to start as it needs to boot up the entire system
>
>However, Docker has less isolation than VMs as containers are sharing the underlying kernel.

To handle the load, run multiple containers and a load balancer. If the container fails, restart.

---

## Container orchestration

Suppose we have multiple containers on a Docker host.
- What if we need to deploy more containers?
- What if we need to scale up when there are more users?

There needs to be an underlying layer that can automatically deploy and manage containers → orchestration

---

# Kubernetes Architecture

## Node
- A node is a machine, physical or virtual on which Kubernetes is installed.
- A node is a worker machine that runs containers

>[!note] What if the node fails?
>Need to define `minNode`

A collection of nodes is called a **Cluster**. This allows you to balance workload or recover from failures.

---

## Master
A *master* node is a overwatches the nodes in the cluster and is responsible for the actual orchestration of the containers in the worker nodes.

---

## Components

### API Server
Allows interaction with the Kubernetes cluster

### etcd
Stores all data about cluster and nodes in a distributed manner
- key-value store

### Scheduler
Distributing work across multiple nodes. Looks for new containers and assigns them to nodes

### Controller
Brain behind the orchestration
Notices and responds to failure.
Makes decision to bring up new containers

### Container runtime
Underlying software that is used to run containers – Docker

### Kubelet
Agent that runs each node in the cluster
Ensures that nodes are running as expected

---

## Master vs Worker
- Worker nodes contains the ==Container runtime== (ie Docker) and ==kubelet==
- Master node contains the ==kube-apiserver==

kubelet interacts with the kube-apiserver about the health of the node and carry out actions requested by the master node.

All information are stored on the ==etcd== on the master node.
==controller== and ==scheduler== are also in the master node.

---

# CRI
Container Runtime Interface allows Kubernetes to work with other container runtime other than Docker.

CRI allows other vendors to work with Kubernetes as long as it follows *Open Container Initiative*

`imagespec` — how image should be built
`runtimespec` — how any container runtime should be developed
`dockershim` — introduced  by Docker to bypass OCI and CRI

**ContainerD** can be used separate from Docker because it is CRI compatible

K8s need to manage `dockershim` –> support for Docker was removed in the later versions


`crictl` — provides CLI for CRI compatible container runtimes.

- Works across different container runtimes
- Used to inspect and debug container runtimes
	- Not used to create containers ideally
- **`crictrl` is aware of pods**

---

# ContainerD
Can be used separately from Docker if you do not need other features
However, it has limited options and not very user friendly

- Used for debugging
- `nerdctl` provides Docker-like CLI for ContainerD to support more general purpose tasks
- Works very similar to `docker` CLI

---
