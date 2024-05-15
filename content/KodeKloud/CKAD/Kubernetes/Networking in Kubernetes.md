# Basics

Start with a single node Kubernetes cluster

Node has an IP address which is used to access the Kubernetes node

>[!note]
>If you are using Minikube, it will have a different IP address from your laptop

In Kubernetes, an IP addr is assigned to a pod.

When Kubernetes is initially configured, it creates an internal private network with all the pods attached to it.

Different pods will get different IP address within the network.

>[!note]
>Using the IP address to communicate between pods may not be a good idea as it is bound to change whenever the pod is restarted

---

## Multiple nodes
Suppose there are multiple nodes which have different IP addresses. This may not be part of a cluster yet.

Pods within the nodes will have an internal network.
- Pods between the nodes will have the same IP address.

When a cluster is set up, Kubernetes does not automatically set up the network.

Kubernetes Cluster Networking
- All container and pods can communicate to one another without NAT
- All nodes can communicate with all containers and vice-versa without NAT

>[!example]
>There exists solutions
>- Calico
>- Cisco
>- Cilium
>- VMWare NSX

