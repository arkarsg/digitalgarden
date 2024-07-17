# Labels, selectors, annotations

#### Labels and selectors
- Used to group or filter based on different criteria
- Labels are properties attached to each item
- Selectors help to filter these items

In Kubernetes, group objects by:
- types
- functionalities
- application

For each object, attach `label` as per your need.

While selecting, specify a condition to filter objects

```yaml
apiVersion: v1
kind: Pod
metadata:
	name: simple-webapp
	labels:
		app: App1
		function: server

...

```

Once the pod is created, to select the pod with the labels:
```bash
k get pods --selector app=App1
```

Kubernetes use labels and selectors to create a `ReplicaSet`. Selector matches labels in the pods.

## Annotations
Annotations are used to record other details for information purpose

---

# Updating Kubernetes deployment
1. Create a simple deployment
```bash
k create deployment nginx --image=nginx:1.16
```
2. Inspect the rollout status and rollout history
```bash
k rollout status deployment nginx
```
```bash
k rollout history deployment nginx
```

When a deployment is created, the deployment will have `version 1`.

To view the status of each version,

```bash
k rollout history deployment nginx --revision=1
```

The `--record` flag saves the *command* used to create or update a deployment against the revision number

#### Undo a change
To *rollback* to the previous version,
```bash
k rollout undo deployment nginx --to-revision=1
```

to rollback to specific revision

---
# Deployment strategies

>[!note]
>**Recreate** : destroy all pods and create pods with new version
>
>**RollingUpdate** : Takes down older version and brings up newer version one by one
>This is the default strategy

## Blue/Green
A new version deployed along side the old version. 100% of the traffic is still routed to the old version (blue). Once all tests are passed, all traffic are routed to the green version.

![blue-setup](Screenshot%202024-06-19%20at%2010.51.47%20PM.png)

Then, create a new deployment `green` with the new label

![green-setup](Screenshot%202024-06-19%20at%2010.52.30%20PM.png)

Then, switch the selector of the service to `v2`

#### Blue deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
	name: myapp-blue
	labels:
		app: myapp
		type: front-end
spec:
	template:
		metadata:
			name: myapp-pod
			labels:
				version: v1 # used by service as a selector
		spec:
			containers:
				- name: app-container
				  image: myapp-image:1.0
	replicas: 5
	selector:
		matchLabels:
			version: v1
```

#### Service
```yaml
apiVersion: v1
kind: Service
metadata:
	name: my-service
spec:
	selector:
		version: v1
```

#### Green deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
	name: myapp-blue
	labels:
		app: myapp
		type: front-end
spec:
	template:
		metadata:
			name: myapp-pod
			labels:
				version: v2 # used by service as a selector
		spec:
			containers:
				- name: app-container
				  image: myapp-image:2.0
	replicas: 5
	selector:
		matchLabels:
			version: v2
```

Once all tests for the `green` deployment passes, change the selector in the service to `v2`.

All traffic will now be redirected to `green` deployment

## Canary
- Deploy the new version and route only a small percentage of the traffic to the new version
- Run tests and if all ok, update the original deployment with a suitable deployment strategy

![](Screenshot%202024-06-19%20at%2010.58.45%20PM.png)

![](Screenshot%202024-06-19%20at%2010.59.48%20PM.png)

To reduce the traffic to Canary deployment, we can simply reduce the number of pods to `1`

#### Service
```yaml
apiVersion: v1
kind: Service
metadata:
	name: my-service
spec:
	selector:
		app: front-end # a selector that is common between the 2 deployments
```

#### Primary deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
	name: myapp-primary
	labels:
		app: myapp
		type: front-end
spec:
	template:
		metadata:
			name: myapp-pod
			labels:
				version: v1
				app: front-end
			spec:
				containers:
					- name: app-container
					  image: myapp-image:1.0
	replicas: 5
	selector:
		matchLabels:
			app: front-end
```

#### Canary deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
	name: myapp-canary
	labels:
		app: myapp
		type: front-end
spec:
	template:
		metadata:
			name: myapp-pod
			labels:
				version: v1
				app: front-end
			spec:
				containers:
					- name: app-container
					  image: myapp-image:2.0
	replicas: 1 # reduced number of pods to limit traffic
	selector:
		matchLabels:
			app: front-end
```

---
# Jobs
There are different types of workloads that a container can serve. There are pods that are meant to carry out a certain task and finish.

For example,
- Computation
- Processing an image
- Analytics on a large dataset, generate report

These are workloads that are meant to live for a short period of time.

#### Simple pod
```yaml
apiVersion: v1
kind: Pod
metadata:
	name: math-pod
spec:
	containers:
		- name: math-add
		  image: ubuntu
		  command: ['expr', '3', '+', '2']
```

When a pod is created, it runs the command and exits. Kubernetes attempts to keep the container alive by bringing it up again and reruns the expression.

>[!note]
>Kubernetes wants to keep pods alive forever → define `restartPolicy`

```yaml
apiVersion: v1
kind: Pod
metadata:
	name: math-pod
spec:
	containers:
		- name: math-add
		  image: ubuntu
		  command: ['expr', '3', '+', '2']
	restartPolicy: Never # OnFailure
```

---

What if there needs to be multiple pods, such as batch processing?

```yaml
apiVersion: batch/v1
kind: Job
metadata:
	name: math-add-job
spec:
	completions: 3 # number of jobs to be successful completions
	parallelism: 3 # creates 3 pods in parallel
	template:
		spec:
			containers:
				- name: math-add
				  image: ubuntu
				  command: ['expr', '3', '+', '2']
			restartPolicy: Never # OnFailure
```

#### Getting the output

```bash
k logs math-add-job
```

---

# CronJobs

A Cron Job is a job that can be scheduled

```yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
	name: reporting-cron-job
spec:
	schedule: "*/1 * * * *"
	jobTemplate:
		spec:
			completions: 3
			parallelism: 3
			template:
				spec:
					containers:
						- image: reporting-tool
						  image: reporting-tool
					restartPolicy: Never
```

![](Screenshot%202024-06-19%20at%2011.28.17%20PM.png)