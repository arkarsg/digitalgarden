Kubernetes services enable communications between various components within and outside of the application.
- Connects applications with other applications or users
- Services enable connectivity between the groups of pods

![services](Screenshot%202024-05-12%20at%203.10.05%20PM.png)

Services enable loose coupling between microservices within the application

---

Suppose there is an instance of an application running in a node. The node has its own IP address.

A user exists within the same network

![simple-k8s-network](Screenshot%202024-05-12%20at%203.47.37%20PM.png)

Clearly, we cannot ping the pod as it is in a separate network. However, from the node, we can access the pod.

How can we access the pod from the user?

# Service

Service is an object listens to a port on the node and forwards requests on that port to the pod that is running the application. This is known as a NodePort service.

![nodeport|500](Screenshot%202024-05-12%20at%203.50.37%20PM.png)

## Service types
### NodePort
> Makes an internal port accessible from the node port

The ports are from the view point of the service.

There are multiple ports involved:
1. TargetPort
	- Where the Service forwards the requests to
	- The port where the actual application is running
2. Port
	- Exists on the Service
	- Has its own IP address — cluster IP of the service
3. NodePort
	- 30000 — 32767

![node-port|500](Screenshot%202024-05-12%20at%203.56.11%20PM.png)

```yaml
apiVersion: v1
kind: Service
metadata:
	name: myapp-service
	labels:
spec:
	type: NodePort
	# Specify the ports
	ports:
		- targetPort: 80
		  port: 80
		  nodePort: 30008
	# Specify the pod to connect the service to by using pod labels
	selector:
		app: myapp
		type: front-end
```

- The only mandatory field is `port`
- If a `targetPort` is not specified, it is assumed to be the same as `port`
- If `nodePort` is not specified, a free port within the valid range is automatically assigned

```
k get services
```

Acts as a LoadBalancer using random algorithm

>[!note]
>The service created spans across all nodes in the cluster

### ClusterIP
> Makes a virtual IP inside the cluster to enable communication between different services

Provides a single interface to access the other pods

Pods communicate with services instead of other pods directly

```yaml
apiVersion: v1
kind: Service
metadata:
	name: back-end
spec:
	type: ClusterIP
	ports:
		- targetPort: 80
		  port: 80
	# Link service to a set of pods
	selector:
		app: myapp
		type: back-end
```

### LoadBalancer
> Enable load balancing across different applications

Suppose for a front-end application that are hosted on worker nodes in a cluster. To make the application accessible to external user, we have created a NodePort

A user can use any of the IP addresses and port of the worker nodes

To allow users to access the application through a URL, configure a VM with a LoadBalancer with a proxy to the internal nodes.

For supported cloud providers, they have native LoadBalancers,
```yaml
apiVersion: v1
kind: Service
metadata:
	name: myapp-service
spec:
	type: LoadBalancer
	ports:
		- targetPort: 80
		  port: 80
		  nodePort: 30002
```

If the environment does not have a native LoadBalancer, this has the same effect as setting `type: NodePort`

