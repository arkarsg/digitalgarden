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

## Pods with YAML

Every Kubernetes definition file always contain and require the following definition fields:

```yaml
apiVersion: v1
kind: Pod
metadata:
	name: myapp-pod
	labels:
		app: myapp
		type: front-end
spec:
	containers:
		- name: nginx-container
		  image: nginx
```

- `apiVersion` : Kubernetes API version to create the object
	- Pod: v1, Service: v1, ReplicaSet: apps/v1, Deployment: apps/v1
- `kind` : type of object we are trying to create
	- `ReplicaSet | Deployment | Service | Pod`
- `metadata` : Metadata about the object
	- A dictionary
	- `label` can have any key-value as you wish
- `spec`
	- Lists of containers

Once the definition is created, create the pod with
```
kubectl create -f pod-definition.yml
```

---

# Controllers
Controllers are processes that monitors Kubernetes objects and spawns accordingly

## Replication Controller

>[!note] What is a replica?
>If a pod fails, a *replica* pod running is still running → users do not lose access to application –> high availability
>
>Replication controller can also bring up a new pod if a pod fails


### Load balancing
Multiple pods are created to load balance. When the number of users increase a new pod is created to balance the load across 2 pods.

Replication controller can span across multiple clusters to balance between pods in different nodes

### ReplicaSet
Both have the same purpose but not the same

`ReplicaSet` replaces Replication Controller in newer versions of Kubernetes

---
### Replication controller YAML

```yaml
apiVersion: v1
kind: ReplicationController
metadata:
	name: myapp-rc
	labels:
		app: myapp
		type: frontend
spec:
	- template:
		metadata:
			name: myapp-pod
			labels:
				app: myapp
				type: front-end
		spec:
			containers:
				- name: nginx-container
				  image: nginx
replicas: 3
```

- `template` defines what pod is being replicated
- `replicas` defines how many replicas should be created

```
kubectl create -f rc-definition.yml
```

View the replication controller
```
kubectl get replicationcontroller
```

View pods created by replication controller
```
kubectl get pods
```

## ReplicaSet

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
	name: myapp-replicaset
	labels:
		app: myapp
		type: front-end
spec:
	template:
		metadata:
			name: myapp-pod
			labels:
				app: myapp
				type: front-end
		spec:
			containers:
				- name: nginx-container
				  image: nginx
	selector:
		matchLabels:
			type: front-end
	replicas: 3
```

>[!caution]
>ReplicaSet requires a `selector` which defines what pods fall under it

ReplicaSet can also manage pods that are not created as part of the ReplicaSet creation with the `selector` field

---

# Labels and Selectors
Suppose we create 3 pods for our front-end. We want to ensure that there are 3 pods running at the same time at all times.

If they are not created, `ReplicaSet` will create them for you

How does `ReplicaSet` know what pod to monitor?
- `labels` are used as a filter for `ReplicaSet`

# Scale
Suppose we have a ReplicaSet definition with 3 replicas and we wish to scale up to 6

## Changing the definition
```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
	name: myapp-replicaset
	labels:
		app: myapp
		type: front-end
spec:
	- template:
		metadata:
			name: myapp-pod
			labels:
				app: myapp
				type: front-end
		spec:
			containers:
				- name: nginx-container
				  image: nginx
replicas: 6
selector:
	matchLabels:
		type: front-end
```

Then, run
```
kubectl replace -f replicaset-definition.yml
```

## Scale command
```
kubectl scale --replicas=6 -f replicaset-definition.yml
```

```
kubectl scale --replicas=6 replicaset myapp-replicaset
```

Note that this does not change the definition of the ReplicaSet

---

# Deployments

How might you deploy an application in a production environment?

For example, we may need multiple instances of the web server. When there are newer versions of the images available, how to upgrade Docker instances seamlessly?

- Upgrading all at once may impact users. Updating instances one by one is called a *rolling update*
- Revert → rollback
- If there are multiple changes, `pause`, apply all changes, then `resume`

Kubernetes Deployments are higher in the hierarchy:
A ReplicaSet is automatically created with a Deployment
![k8s-deployment](Screenshot%202024-05-09%20at%2010.44.51%20PM.png)

>[!note]
>Deployment definitions are similar to ReplicaSet

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
	name: myapp-deployment
	labels:
		tier: frontend
		app: nginx
spec:
	template:
		metadata:
			name:
			labels:
		spec:
			containers:

	replicas:
	selector:
		matchLabels:
```

Create a deployment:

```
k create -f deployment-definition.yml
```

Observe the deployment
```
k get deployments
```

Deployment automatically creates a ReplicaSet:
```
k get replicaset
```

ReplicaSet create pods
```
k get pods
```

---

To see all the objects created,
```
k get all
```

```
k describe deployment myapp-deployment
```

---

## Updates and Rollback

### Rollout
When a deployment is first created, it triggers a *rollout*. Suppose it is called `revision 1`.

When the container version is updated to a new one, a new rollout is triggered and a new revision is created.

This helps us keep track of the deployment and enables us to rollback.

To see the status of the rollout by running the command
```
kubectl rollout status deployment/myapp-deployment
```

To see the revisions and history of rollout,
```
kubectl rollout history deployment/myapp-deployment
```

### Deployment strategies
Suppose there are 5 instances of the application

1. Destroy all instances and deploy 5 new instances

However, the problem is that between the period, the application is down and users cannot access the application. This approach is known as `Recreate`

Old `ReplicaSet` is scaled down to 0 then scaled up again.

2. Take down the older instances one by one and update.

This upgrade is seamless and is known as `RollingUpdate`. This is the default update strategy.

### How to update?

Since we have the definition file, we can simply update the definition and,
```
kubectl apply -f deployment-definition.yaml
```

Alternatively, we can
```
kubectl set image deployment/myapp-deployment nginx-container=nginx:1.9.1
```
However, doing it this way result in deployment having different definition from definition file

### Under the hood
1. When a Deployment is created, Kubernetes automatically creates a ReplicaSet and deploy the pods
2. When there is an update, Kubernetes create a new ReplicaSet and deploy pods. Simultaneously, it takes down the pods in the old ReplicaSet.

### Rollback
To undo a change
```
kubectl rollout undo deployment/myapp-deployment
```
1. Kubernetes destroy the pods in the new ReplicaSet
2. Kubernetes brings up the pods in the old ReplicaSet

Note that this creates a new Revision which is also equivalent to the previous revision.




