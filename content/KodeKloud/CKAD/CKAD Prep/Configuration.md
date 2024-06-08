# Docker definitions

>[!note] Why create your own image?
>You cannot find a component or a service for your application and cannot find on Docker Hub.
>Ease of deployment

## Creating image
For example, to create an image for a simple web application in Flask,
- start with an OS
- Update `apt`
- Install dependencies using `apt`
- Install Python dependencies using `pip`
- Copy source code to `/opt` folder
- Run the web server using the `flask` command

```Dockerfile
FROM Ubuntu

RUN apt-get update
RUN apt-get install python

RUN pip install flask
RUN pip install flask-mysql

COPY . /opt/src

ENTRYPOINT FLASK_APP=/opt/src/app.py flask run
```

---

# Command and arguments

## Commands in Docker
Unlike virtual machines, containers are not meant to host an operating system. It is meant to host a task or a process. Once the task is completed, the container exits. The container only lives as long as the process lives.

In Dockerfile for Ubuntu,
```Dockerfile
CMD ["bash"]
```

`bash` is the default command. This is a shell that listens to the terminal. Since there is no terminal, it exits. Since the process is finished, the container exits as well.

```bash
docker run [IMAGE] [COMMAND]
```

`[COMMAND]` **overrides** the `CMD` in Dockerfile.

---

### Entrypoint
Entrypoint specifies the program that will be run when the container starts. Other arguments defined during `docker run` is appended to the `ENTRYPOINT`

In Dockerfile,
```Dockerfile
FROM Ubuntu
...

ENTRYPOINT ["sleep"]
```
```bash
docker run ubuntu-sleeper 5 # sleep for 5 seconds
```

---

#### Default arguments
```Dockerfile
FROM Ubuntu
ENTRYPOINT ["sleep"]
CMD ["5"]
```
- Defaults to `sleep 5`
- Arguments overrides `5`

---

## Commands in Pods
Suppose we have `unbuntu-sleeper` image as defined above.

```yaml
apiVersion: v1
kind: Pod
metadata:
	name: ubuntu-sleeper-pod
spec:
	containers:
		- name: ubuntu-sleeper
	      image: ubuntu-sleeper
	      args: ["10"]
```

- `command` in pod definition corresponds to `ENTRYPOINT` in Dockerfile
- `args` in pod defintion corresponds to `CMD` in Dockerfile

---

# Env vars

To **directly** set env vars in pod definitions,

```yaml
apiVersion: v1
kind: Pod
metadata:
	name: ubuntu-sleeper-pod
spec:
	containers:
		- name: ubuntu-sleeper
	      image: ubuntu-sleeper
	      args: ["10"]
	      env:
		      - name: APP_COLOR
		        value: pink
```

Else, use `configMaps` or `secrets`

---

# ConfigMaps
When there are a lot of pod definitions, it becomes harder to manage values.
`ConfigMap` contain key-value pairs

1. Create `ConfigMap`
2. Inject them into pods

## Creating `configMap`

Imperative approach

```bash
k create configmap \
	<CONFIG NAME> --from-literal=<KEY>=<VALUE> \
				  --from-literal=<KEY>=<VALUE>

k create configmap \
	<CONFIG NAME> --from-file=app_config.properties
```

Declarative approach
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
	name: app-config
data:
	APP_COLOR: blue
	APP_MODE: prod
```



View `ConfigMap`
```bash
k get configmaps

k describe configmaps
```

## Consuming `ConfigMap` in Pods
```yaml
apiVersion: v1
kind: Pod
metadata:
	name: ubuntu-sleeper-pod
spec:
	containers:
		- name: ubuntu-sleeper
	      image: ubuntu-sleeper
	      args: ["10"]
	      # envFrom is a list. Each item corresponds to a configmap
	      envFrom:
		      - configMapRef:
			      name: app-config
```

```yaml
apiVersion: v1
kind: Pod
metadata:
	name: ubuntu-sleeper-pod
spec:
	containers:
		- name: ubuntu-sleeper
	      image: ubuntu-sleeper
	      args: ["10"]
	      # envFrom is a list. Each item corresponds to a configmap
	      env:
		      - name: APP_COLOR
		        valueFrom:
			        configMapKeyRef:
				      name: app-config
				      key: APP_COLOR
```

---

# Secrets

`ConfigMap` stores variables in plaintext –> not suitable to store passwords

- Secrets are used to store secret information.
- They are stored in an encoded format

## Creating secrets
Imperative
```bash
k create secret generic \
	<secret-name> --from-literal=<key>=<value>

k create secret generic \
	<secret-name> --from-file=<path-to-files>
```

Declarative

For each secret,
```bash
echo -n <secret-value> | base64
```

```yaml
apiVersion: v1
kind: Secret
metadata:
	name: app-secret
data:
	DB_HOST: <value>
	DB_USER: <value>
	DB_PASSWORD: <value>
```

`get` and `describe` only shows encoded values.

To decode the values
```bash
echo -n <encoded-value> | base64 --decode
```

## Consuming secrets

Inject all secrets as an environment variable:

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
		  image: simple-webapp-image
		  ports:
			  - containerPort: 8080
		  envFrom:
			  - secretRef:
				  name: app-secret # name of the secret
```

---

Single env var:
```yaml
...
env:
	- name: DB_PASSWORD
	  valueFrom:
		  secretKeyRef:
		    name: app-secret
		    key: DB_PASSWORD
...
```

---

Inject secrets as file in a volume:

```yaml
volumes:
- name: app-secret-volume
  secret:
	  secretName: app-secret
```

>[!caution]
>Secrets are not encrypted. They are only encoded.
>
>Secrets are not encrypted in `etcd`. See Encryption at Rest
>
>Do not check-in `Secret` objects in Git along with the code
>
>Consider third party secrets store providers:
>- AWS Provider, Vault Provider etc

>[!note] How Kubernetes handle secrets
>- A secret is only sent to a node if a pod on that node requires it
>- Kubelet stores the secret into a `tmpfs` so that the secret is not written to disk storage
>- Once the pod that depends on the secret is deleted, kubelet will delete its local copy of the secret data as well

## Encrypting secret data at rest
```bash
apt-get install etcd-client
```

---

# Security Context
>[!note] Docker security – Process isolation
>Suppose there is a host with Docker running on it. The host has its own set of processes running. Processes created by Docker share the same kernel and are isolated by their own namespace.
>
>Within the Docker container, it sees its own process as `pid 1`

>[!note] User isolation
>Docker runs processes within the containers as the `root` user. Otherwise, specify the user in the Dockerfile or within `docker run --user`

Root user within the container is not the same as the root user within the host.

Docker runs a container with a limited set of capabilities. Therefore, it cannot reboot the host, etc. However, you can add these capabilities.

## Kubernetes Security Contexts
You can configure capabilities at a pod level or a container level

```yaml
apiVersion: v1
kind: Pod
metadata:
	name: web-pod
spec:
	# pod level security context
	securityContext:
		runAsUser: 1000
	containers:
		- name: ubuntu
		  image: ubuntu
		  command: ["sleep", "3600"]
```

```yaml
apiVersion: v1
kind: Pod
metadata:
	name: web-pod
spec:
	containers:
		- name: ubuntu
		  image: ubuntu
		  command: ["sleep", "3600"]
		  # container level security context
		  securityContext:
			runAsUser: 1000
			capabilities:
				add: ["MAC_ADMIN"]
```

>[!note]
>Capabilities are only supported at the container level and not at the pod level

---

# Resource requirements
Suppose there are 3 nodes in the Kubernetes cluster with configuration of CPU and RAM.

Each pod consumes CPU and RAM on the node.

`kube-scheduler` decides which node a pod goes to.

If nodes have no sufficient resources available, it avoids placing the pods into that node.

If all the nodes are filled, it will hold back the node and results in a pending state. (Insufficient CPU)

## Resource requests
Minimum amount of resources requested by a container

```yaml
apiVersion: v1
kind: Pod
metadata:
	name: simple-webapp-color
	labels:
		name: simple-webapp-color
spec:
	containers:
		- name: simple-webapp-color
		  image: simple-webapp-color
		  ports:
			  - containerPort: 8080
		  resources:
			  requests:
				  memory: 4
				  cpu: 2
```

Pods are guaranteed this amount of resources

#### Units for CPU
1 CPU is equivalent to
- 1 AWS vCPU
- 1 GCP Core
- 1 Azure Core
- 1 Hyperthread

0.1 CPU => 100m CPU

#### Units for RAM
Both `G` and `Gi` are acceptable

## Resource limits
By default there are no limits. However, you can set the limits. 

Requests and limits are set for containers within a pod. Each container can have different limits and requests.

---

## Exceeding limits
### CPU
A container cannot use CPU resources more than its limits => Kubernetes will throttle the container.

### Memory
A container can use more memory resources than its limits. However, the pod will be killed (OOMKiller)

---

## Default behavior
Any pod can consume as much resources by default and starve other pods or processes

### CPU
Suppose there are 2 pods competing for same resources within a cluster.

#### No requests, no limits
Without requests and limits, a pod can consume all the resources and starve the other pods

#### No requests, with limits
Kubernetes will set the requests to the same as limits if requests is not defined

#### Requests and limits
Each pod gets resources guaranteed by the requests but not more than the limit

>[!note] 
>However, this may not be ideal.
>
>Suppose there are 2 pods where a pod requires resources greater than the limits and another pod that is consuming substantially less resources. The first pod cannot use the available resources due to limit set despite having sufficient resources

#### Requests and no limits
A pod can consume as much CPU as it requires
- A good usecase for limits prevents misuse of infrastructure – such as extremely heavy workloads or mining

### Memory

#### No requests and no limits
If there are no limits and requests set, a pod can consume all the memory and starve the other pod

#### No requests and limits
requests = limits

#### Requests and limits

#### Requests and no limits

>[!note] Unlike CPU, we cannot throttle memory. It will kill the pod.


## LimitRange
Specifies the default resource limits without specifying the limits and requests within the pod:

```yaml
apiVersion: v1
kind: LimitRange
metadata:
	name: cpu-resource-constraint
spec:
	limits:
		- default:
			cpu: 500m # limit
		  defaultRequest:
		    cpu: 500m # request
		  max:
		    cpu: "1" # maximum limit that can be set on a pod/container
		  min:
		    cpu: 100m # minimum request a pod/container can make
		  type: Container
```

The LimitRange is enforced when a pod is created. It will not affect existing pods.

## Restricting total amount of resources
Create quota at namespace level to set hard limits for requests and limits for all the pods together:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
	name: my-resource-quota
spec:
	hard:
		requests.cpu: 4
		requests.memory: 4Gi
		limits.cpu: 10
		limits.memory: 10Gi
```

---

# Service accounts
Related to RBAC, authorisations

## User account
- Accounts used by humans
- Admin doing admin tasks
- Developer deploying applications

## Service account
Monitoring application like Prometheus uses service accounts
Jenkins use service accounts to deploy applications

`kube-api` requires service account

```bash
k create serviceaccount dashboard-sa
```

```bash
k get serviceaccount
```

When a service account is created, it creates a token automatically. This is for the API that is consumed by the third party application. It is stored as a `Secret` object

If the application is deployed on the cluster, the service token secret can be mounted in the pod instead of providing it manually

A `default` is automatically created for every namespace. However, this is very limited.

If service account is not defined in the pod definition, the default service account is used.

```yaml
apiVersion: v1
kind: Pod
metadata:
	name: my-kubernetes-dashboard
spec:
	containers:
		- name: my-k8s-dashboard
		  image: my-k8s-dashboard
	serviceAccountName: <your-service-account-name>
```

>[!caution]
>You cannot edit the service account of an existing pod. However, you can edit service account of deployments

>[!note] Service accounts
>When a pod is created it automatically associates the pod with the secret and mounts the secret.
>A process within the pod has access to the token and can make API calls to Kubernetes

>[!note] TokenRequestAPI
>Mechanism to provision tokens that are more secure and scalable
>- Audience bound
>- Time bound
>- Object bound

When a new pod is created, it no longer relies on directly mounting the secrets object. Rather, it creates a projected volume that actually communicates with the TokenRequest API to get the token for the pod

>[!note] v1.24
>Creating `ServiceAccount` no longer creates a secret token:
>```bash
>k create token # your-service-account
>```
>This creates a secret token with an expiry

To create secrets the old way:

```yaml
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
	name: mysecretname
	annotations:
		kubernetes.io/service-account.name: dashboard-sa
```

---

# Taints and tolerations

Consider multiple pods and multiple nodes on a cluster.

Taints and tolerations are used to set restriction on what pods can be scheduled on a node.

- Place a taint on node => none of the pods can be placed on the node
- Let pod $A$ and pod $B$ be tolerant to the taint
- Pod $A$ and $B$ can be deployed on the node, while other pods cannot be deployed

```bash
k taint nodes node-name key=value:taint-effect
```

For example
```bash
k taint nodes node-name app=webapps:NoSchedule
```

`taint-effect` is one of `NoSchedule | PreferNoSchedule | NoExecute`

>[!note] `NoExecute`
>New pods cannot be scheduled on the node. Existing pods will be evicted.


## Tolerations
Tolerations are added to a pod

```yaml
apiVersion: v1
kind: Pod
metadata:
	name: myapp
spec:
	containers:
	- name: nginx-container
	  image: nginx
	# add tolerations -- use values from taint
	tolerations:
	- key: "app"
	  operator: "Equal"
	  value: "webapps"
	  effect: "NoSchedule"
```

>[!note] Why Kubernetes scheduler does not schedule any pods on the master node
>When creating the cluster, Kubernetes immediately taints the master node with `NoSchedule`

---

# Node Selectors
Suppose we have 3 nodes with 3 different resources.

Ideally, we want to schedule workloads that require more resources to nodes with more resources

To ensure that the workload is always scheduled to the right node, there are 2 ways to do so:
1. Node Selectors
2. Node Affinity

## Selectors

```yaml
apiVersion: v1
kind: Pod
metadata:
	name: myapp-pod
spec:
	containers:
	- name: data-processor
	  image: data-processor
	nodeSelector:
		size: Large # Labels assigned to the node
```

>[!caution] Nodes must have been labelled

```bash
k label nodes <node-name> <label-key>=<label-value>
```

>[!caution] Limitations
>Single key to select the nodes => what if the criteria is more complex, such as:
>- Place pod on any nodes that are Medium or Large
>- Place pod on nodes NOT Small

# Node Affinity
- Ensures that pod is scheduled on a particular node
- Allows more specifications

```yaml
apiVersion: v1
kind: Pod
metadata:
	name: myapp-pod
spec:
	containers:
	- name: data-processor
	  image: data-processor
	affinity:
		nodeAffinity:
			requiredDuringSchedulingIgnoredDuringExecution:
				nodeSelectorTerms:
					- matchExpressions:
						- key: size
						  operator: In # NotIn Small
						  values:
						  - Large
						  - Medium
```

#### Operators
`In | NotIn | Exists`

**What if there are no nodes with the label?**
Node affinity types defines the behaviour of the scheduler and the stages in the lifecycle of the pod
`requiredDuringSchedulingIgnoredDuringExecution | preferredDuringSchedulingIgnoredDuringExecution`

If a node affinity type is `required`, the pod will never be scheduled if it cannot find the label.
If a node affinity type is `preferred`, the pod will be placed on any available nodes. The node affinity rules are ignored.

