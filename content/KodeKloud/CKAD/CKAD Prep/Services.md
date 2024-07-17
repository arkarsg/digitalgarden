Enable communication within and outside between various components

Helps us connect applications together with other applications or users

![services](Screenshot%202024-06-20%20at%202.49.41%20PM.png)

Enables loose coupling between microservices

---
A node has an IP address and an internal node

![networking|500](Screenshot%202024-06-20%20at%202.51.11%20PM.png)

To access the application with just the IP address and port of the node, we need a *service*.

#### NodePort
An object that listens to a port on the node and forward requests to the port to a port on the pod running the application.

- Maps a port on the node to a port of a pod
![nodeport|500](Screenshot%202024-06-20%20at%202.53.41%20PM.png)


#### ClusterIP
A service creates a virtual IP inside the cluster to enable communication between different services

#### LoadBalancer
Enable load balancer with supported cloud provider

---

# Network policy

For a web server, the incoming request from the users is called an **ingress**.

The outgoing requests to the app server is an **egress**

A network policy is attached to a pod. For example, to allow traffic from a specific port or other additional rules.

```yaml
apiVersion: netowrking.k8s.io/v1
kind: NetworkPolicy
metadata:
	name: db-policy
spec:
	podSelector:
		matchLabels:
			role: db
	policyTypes:
		- Ingress
	ingress:
		- from:
			- podSelector:
				matchLabels:
					name: api-pod
		ports:
			- protocol: TCP
			  port: 3306
```

>[!caution]
>Not all network solutions support network policies

---

Suppose an API pod connects to a DB pod on port 3306. We only wish for API pod and no other pod to connect to the DB pod.

1. Associate the network policy with the pod using `podSelector` and `matchLabels`. This blocks out all traffic
2. Since the DB pod is receiving incoming traffic from API pod, it is an **ingress**.
	- The results from DB query is allowed back automatically and an egress does not have to be explicitly defined.
	- However, this does not mean that DB is able to make API calls to the API pod since it is an **egress**
	- `policyTypes` is `Ingress`
3.  Create a section called `ingress` to specify the rules
	- `from` section defines the source of traffic that we allow the traffic to come through

This creates a policy that blocks all traffics from other pods except the API pod.

>[!note] What if there are multiple environments and namespaces?
>With matching labels pod in any env or namespace can reach the pod.
>
>Then, we can use the `namespaceSelector`

Suppose we want to connect to a database at a certain IP address, then we can use the `ipBlock` to allow traffic in the IP address ranges


#### Egress
Suppose we want the DB pod that pushes to backup server.

1. Add `Egress` under policy types
2. Add `egress` section
	- `to` field using `ipBlock`
	- Specify the ports and protocols

---

## Ingress Controller
Kubernetes does not come with an ingress controller by default.
- It has to be deployed

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
	name: ingress-wear-watch
spec:
	rules:
	- http:
		  paths:
		  - path: /wear
		    pathType: Prefix
		    backend:
			    service:
				    name: wear-service
				    port:
					    number: 80
		  - path: /watch
		    pathType: Prefix
		    backend:
			    service:
				    name: watch-service
				    port:
					    number: 80
```

```bash
k create ingress ingress-test \
--rule="wear.my-online-store.com/wear*=wear-service:80
```

---

### Example of Ingress flow
>[!note]
>How does `ngix.ingresz.kubernetees.io/rewrite-target` work?

1. **Service Location**: Assume `wear-service` is running at `localhost:8080/`.

2. **Ingress Rule**: The Ingress resource defines a rule that allows users to access `wear-service` via `site.com/wear`.

3. **Rewrite Target**: The annotation `nginx.ingress.kubernetes.io/rewrite-target: /` is specified in the Ingress resource.

4. **User Request**: A user makes a request to `http://site.com/wear`.

5. **Ingress Controller Handling**:
    - **Path Matching**: The Ingress controller matches the path `/wear` as specified in the rule.
    - **Rewrite Path**: The controller rewrites the path from `/wear` to `/` due to the `rewrite-target` annotation.
    - **Forward Request**: The request is then forwarded to `wear-service`.

6. **Request to Backend**:
    - The request that `wear-service` receives is at `http://localhost:8080/` instead of `http://localhost:8080/wear`.

Here's a more detailed breakdown with a complete example:

### Ingress Resource
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-wear-watch
  namespace: app-space
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  rules:
    - http:
        paths:
          - path: /wear
            pathType: Prefix
            backend:
              service:
                name: wear-service
                port:
                  number: 8080
```

### Flow Example
1. **User Request**: `http://site.com/wear/item`
   - This is the initial request made by the user to the Ingress.

2. **Ingress Controller**:
   - **Matches Path**: `/wear` (because the request starts with `/wear`).
   - **Rewrites Path**: From `/wear/item` to `/item` (because of the `rewrite-target` annotation).

3. **Forwarded Request**:
   - The Ingress controller forwards the rewritten request to `http://localhost:8080/item`.

### Diagram

1. **Initial Request**:
   ```mermaid
   flowchart LR
   User --> site.com/wear/item
   ```

2. **Ingress Path Matching and Rewriting**:
   ```mermaid
   flowchart LR
   Ingress --> B["Matches /wear"] --> C["Rewrites /wear/item to /item"]
   ```

3. **Forwarded to Backend Service**:
   ```mermaid
   flowchart LR
   A["Forward to wear-service"] --> B["http://localhost:8080/item"]
   ```

### Conclusion

- The Ingress rule allows users to access `wear-service` with the URL `site.com/wear`.
- The `rewrite-target` annotation ensures that the `/wear` part of the URL is replaced with `/` before the request reaches `wear-service`.
- As a result, `wear-service` receives the correct path and processes the request accordingly.

This mechanism ensures that the backend service `wear-service` does not need to handle the `/wear` prefix and can treat incoming requests as if they were directly targeting it without the prefix.