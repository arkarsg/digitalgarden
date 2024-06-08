>[!caution] 
>This is a recap of Kubernetes for Absolute Beginners


# Nodes
>[!note]
>A node is a machine, *physical or virtual*, in which Kubernetes is installed

A node is a worker machine and where containers are spawned.

>[!caution] What if the node fails?
>There needs to be more than 1 node

Multiple nodes creates a cluster. This also ensures that load is balanced.

## Master node
How are the nodes monitored?
How are the workload of a failed load moved to another node?

Master node watches over the nodes in the cluster and is responsible for the actual orchestration of containers in the worker nodes.

## Master vs Worker nodes
### Worker nodes
- Container runtime, for example, Docker
- `kubelet` – interacts with master to provide health information

### Master node
- `kube-apiserver`
- `etcd`
- `controller`
- `scheduler`
---

# Container runtime
Most popular : Docker

There is also `containerd`
- requires `nerdctl`

## Container runtime interface
From kubernetes, for debugging containers

---

# Pods

## Edit Pods

#### A Note on Editing Existing Pods

In any of the practical quizzes, if you are asked to **edit an existing POD**, please note the following:

- If you are given a pod definition file, edit that file and use it to create a new pod.
- **If you are not given a pod definition file**, you may extract the definition to a file using the below command:
    
    `kubectl get pod <pod-name> -o yaml > pod-definition.yaml`
    
    Then edit the file to make the necessary changes, delete, and re-create the pod.
    
- To modify the properties of the pod, you can utilize the `kubectl edit pod <pod-name>` command. Please note that only the properties listed below are editable.
    - spec.containers[*].image
    - spec.initContainers[*].image
    - spec.activeDeadlineSeconds
    - spec.tolerations
    - spec.terminationGracePeriodSeconds
---

# Imperative commands

While you would be working mostly the declarative way – using definition files, imperative commands can help in getting one time tasks done quickly, as well as generate a definition template easily. This would help save considerable amount of time during your exams.

Before we begin, familiarize with the two options that can come in handy while working with the below commands:

`--dry-run` : By default as soon as the command is run, the resource will be created. If you simply want to test your command , use the `--dry-run=client` option. This will not create the resource, instead, tell you whether the resource can be created and if your command is right.

`-o yaml`: This will output the resource definition in YAML format on screen.

Use the above two in combination to generate a resource definition file quickly, that you can then modify and create resources as required, instead of creating the files from scratch.

#### POD

**Create an NGINX Pod**

```
kubectl run nginx --image=nginx
```

**Generate POD Manifest YAML file (-o yaml). Don’t create it(–dry-run)**

```
kubectl run nginx --image=nginx --dry-run=client -o yaml
```

#### Deployment

**Create a deployment**

```
kubectl create deployment --image=nginx nginx
```

**Generate Deployment YAML file (-o yaml). Don’t create it(–dry-run)**

```
`kubectl create deployment --image=nginx nginx --dry-run -o yaml`
```

**Generate Deployment with 4 Replicas**

```
kubectl create deployment nginx --image=nginx --replicas=4
```

**You can also scale a deployment using the** `kubectl scale` command.

**Another way to do this is to save the YAML definition to a file and modify**

```
kubectl create deployment nginx --image=nginx--dry-run=client -o yaml > nginx-deployment.yaml
```

**You can then update the YAML file with the replicas or any other field before creating the deployment.**

#### Service

**Create a Service named redis-service of type ClusterIP to expose pod redis on port 6379**

```
kubectl expose pod redis --port=6379 --name redis-service --dry-run=client -o yaml
```

**(This will automatically use the pod’s labels as selectors)**

**Or**

```
kubectl create service clusterip redis --tcp=6379:6379 --dry-run=client -o yaml
```

(This will not use the pods labels as selectors, instead it will assume selectors as **app=redis.** [You cannot pass in selectors as an option.](https://github.com/kubernetes/kubernetes/issues/46191) So it does not work very well if your pod has a different label set. So generate the file and modify the selectors before creating the service)

**Create a Service named nginx of type NodePort to expose pod nginx’s port 80 on port 30080 on the nodes:**

```
kubectl expose pod nginx --port=80 --name nginx-service --type=NodePort --dry-run=client -o yaml
```

**(This will automatically use the pod’s labels as selectors,** [but you cannot specify the node port](https://github.com/kubernetes/kubernetes/issues/25478). You have to generate a definition file and then add the node port in manually before creating the service with the pod.)

Or

```
kubectl create service nodeport nginx --tcp=80:80 --node-port=30080 --dry-run=client -o yaml
```

**(This will not use the pods labels as selectors)**

**Both the above commands have their own challenges. While one of it cannot accept a selector the other cannot accept a node port. I would recommend going with the `kubectl expose` command. If you need to specify a node port, generate a definition file using the same command and manually input the nodeport before creating the service.**

**Reference:**

[https://kubernetes.io/docs/reference/kubectl/conventions/](https://kubernetes.io/docs/reference/kubectl/conventions/)