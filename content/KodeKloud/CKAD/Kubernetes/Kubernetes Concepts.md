# Pods
>[!note] Pre-requisites
>Assume that the application is already in a Docker image and a Kubernetes cluster is already set up

Kubernetes does not deploy containers directly on the worker node.

A container is encapsulated in a *pod*

>[!note] A pod is the smallest unit that you can create in Kubernetes

When there are more users of the application, create a **new** pod instead of creating a new container.

If there are even more users, there will be a new node running the pods.

>[!note] 
>In other words, there is a one-to-one relationship between the container and a pod

## Multi-container pods
A single pod can have multiple containers. Except, they are not containers of the same kind.

- Helper containers that lives alongside the main container
	- Example: Processing files uploaded
	- Containers can communicate with each other since they exist within the same network
	- Helper container is started when the main container is started
	- Helper containers die if the main container die

>[!caution]
>Multi-container pods are a rare usecase

## Example
```
kubectl run nginx --image nginx
```

Deploys a Docker container by
- creating a pod
- with the image specified

```
kubectl get pods
```
Lists all the `pods`
- its `READY`
- and its `STATUS`

---

