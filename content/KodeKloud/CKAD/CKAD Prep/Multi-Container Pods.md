# Multi-Container Pod Patterns

Decouple monolithic application into microservice:
- Scale each microservice
- Develop microservice independently

However, there may be a need to run two services together. For example, a logging service for a web server which is also in a microservice.

We do not want to bloat the web server microservice code with the logging service. We still want to develop and deploy independently, but deployed together.

We want multi-container pods that share the same
- lifecycle
- network
- volume sharing

## Ambassador

Suppose there are different environments such as `dev`, `test`, `prod`. A container needs to configure the connection to send the log info.

Outsource the logic to another container such that when an application sends logging info to localhost, the ambassador container proxies to the right server.

## Adapter

Suppose different services use different formats of logging. A central logging server will not be able to parse and consume these logs. To format to the same format, use adapter pattern. The adapter container processes the log before sending to the central logging server.


## Sidecar

Deploy a logging service together with an application

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
	- name: log-agent # sidecar
	  image: log-agent
```

# `InitContainers`

Suppose we wish to run a process that runs to completion in a container before the main container starts.

When a pod is first created, `initContainer` is run and the processes in `initContainer` must run to completion before the real container hosting the application starts.

When there are multiple `initContainers`, each container is run one at a time in sequential order.

If any `initContainer` fails, Kubernetes restarts the pod until the `initContainer` succeeds.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox:1.28
    command: \['sh', '-c', 'echo The app is running! && sleep 3600'\]
  initContainers:
  - name: init-myservice
    image: busybox:1.28
    command: \['sh', '-c', 'until nslookup myservice; do echo waiting for myservice; sleep 2; done;'\]
  - name: init-mydb
    image: busybox:1.28
    command: \['sh', '-c', 'until nslookup mydb; do echo waiting for mydb; sleep 2; done;'\]
```