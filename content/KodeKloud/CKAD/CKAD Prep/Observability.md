>[!note] Recap
>Pod lifecycle → A pod has a status and condition
>1. When a pod is first created, it is in a `Pending` state until a scheduler finds a node to place the pod on
>2. When a pod is created, it goes into `ContainerCreating` state.
>3. When all the containers are started, it goes into `Running` state.

Conditions complements pod status. It is an array of `true` or `false` values

# Readiness Probes
Containers can be running different kinds of applications. The applications and scripts may take a few seconds to get ready.

>[!example]
>Jenkins UI takes about 10-15 seconds to start up and a few more seconds to warm up the server

Therefore, we need to tie the `Ready` condition to the actual state of the application inside the container.

To check if the application is up and ready. You can set up:
- tests or probes
	- HTTP test, TCP test
	- Custom script to exit when the application is ready

```yaml
apiVersion: v1
kind: Pod
metadata:
	name: simple-webapp
	labels:
		name: simple-webapp
spec:
	containers:
		- name: simple-webapp
		  image: simple-webapp
		  ports:
			  - containerPort: 8080
		  readinessProbe:
			  httpGet: #tcpSocket #exec
				  path: /api/ready
				  port: 8080
			  intialDelaySeconds: 10
			  periodSeconds: 5
			  failureThreshold: 8
```

- When the container is created, Kubernetes does not immediately set the ready condition to `True`.
- It performs a test to see if API responds positively

# Liveness Probes

Every time a pod crashes, Kubernetes makes an attempt to restore service to users by restarting the pod.
What if the application is not really working but the container stays alive? From Kubernetes’ perspective, the container is up. Therefore, there is no need to restart the container.

To periodically check if the application within the container is actually healthy, a liveness probe is used.

```yaml
apiVersion: v1
kind: Pod
metadata:
	name: simple-webapp
	labels:
		name: simple-webapp
spec:
	containers:
		- name: simple-webapp
		  image: simple-webapp
		  ports:
			  - containerPort: 8080
		  livenessProbe:
			  httpGet: #tcpSocket #exec
				  path: /api/ready
				  port: 8080
			  intialDelaySeconds: 10
			  periodSeconds: 5
			  failureThreshold: 8
```

# Logging

For a single container:
```
docker logs -f <docker-container-id>
```

In Kubernetes:
```
k logs -f pod-name
```

The logs are specific to containers specific to the pod.

If there are more than 1 container in the pod, you have to specify the name of the container inside the command

```
k logs -f pod-name container-name
```

# Monitoring

How to monitor resource consumption in Kubernetes.
- Node level metrics
- Performance metrics
- Pod level and its performance metrics

How to record and store for analytics?
- Metrics Server
- Prometheus
- Elastic Stack
- Datadog

- One metrics server per kubernetes cluster
- In-memory storage solution
- Cannot store historical performance data

## How are the metrics generated?
Kubelet contains sub component known as `cAdvisor` which exposes pod performances.

```bash
k top node
```

gives usage of the nodes

```bash
k top pod
```

gives performance of pods.