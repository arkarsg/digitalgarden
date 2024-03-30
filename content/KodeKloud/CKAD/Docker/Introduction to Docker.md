# Docker

Suppose there is an end-to-end application stack with
- `node.js`
- `MongoDB`
- `Redis` messaging
- `Ansible` orchestration

1. These libraries have dependencies with the underlying OS
	1. Some versions may not be compatible with the OS
2. Check the compatibility between libraries (the Matrix from hell)
3. Difficult to set up a new environment — test, dev environments, new developers etc
4. Ensure the application runs the same way on different environments

This causes difficulties in building, developing and shipping the application

Docker allows you to run each component in a separate container with its own libraries within its own environment.
- Containerise applications
- Run each service with its own dependencies in separate containers

---

## Containers

>[!important] Main purpose
>Package and containerize applications to ship them. And run them anywhere, anytime.

Isolated environments that share the **same** OS kernel but have their own *processes*, *network* interfaces and *mounts*.

**Docker** uses LXC containers. Setting up the container environments is hard as it is very low-level. Docker provides a high-level API.

### OS
OS consists of:
1. OS kernel
2. A set of software

OS kernel remains the same, but the *software* is what makes different OS different (ie Ubuntu, CentOS etc)

>[!note] What does it mean to *share* the kernel?
>Suppose we have an Ubuntu OS (Linux kernel + Ubuntu software) with Docker installed.
>
>Docker can run any flavour of OS on top of it as long as they are all based on Linux kernel. Therefore, you can run other distributions of Linux.

>[!note] What if the OS does not share the same kernel as Docker-host?
>For example, Windows container will not be able to run on a Docker-host with Linux kernel, and requires a Docker with Windows server.
>
>>When you install Linux container on Windows, Windows run a Linux virtual machine which runs a Linux container

Unlike hypervisors, Docker is not meant to virtualize to run different kernels and OS on the same hardware.

- Docker has less isolation as it is sharing the same resources.

### Containers and VMs
> It is not an either or situation

In large environments,
- containers are provisioned on a virtual Docker host

![containers-and-vm|500](Screenshot%202024-03-30%20at%204.24.52%20PM.png)

## Image vs Containers
### Image
An image is a package or template to create one or more containers

### Containers
Running instances of the image that are isolated and have their own environments and processes.

---

# Docker hub

Most commonly used applications are already are containerised and pushed to public Docker registry.

Multiple instances → add many instances and configure a load balancer
- if `fail`, destroy and provision another container

---







