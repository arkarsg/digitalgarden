Security is of prime concern for production-ready applications in Kubernetes.

>[!note] Secure hosts
>- Password based authentication disabled
>- SSH Key based authentication
>- Root disabled

## `kube-apiserver`
Controlling access to the API server

### Who can access?
#### Files
- Username and passwords
- Username and tokens
- Certificates
- External auth providers
- Service accounts

### Authorization
- RBAC
- ABAC – attribute based auth
- Node auth
- Webhooks

Components of the Kube ApiServer uses TLS certificates.

---

- Restrict access between pods using network policy.

---

## Authentication
### User
- Admins
- Developers

All User access is managed by the `kube-apiserver`.
1. Authenticate requests
2. Serve requests

#### How does `kube-apiserver` authenticate?
1. Static password files
2. Static token files
3. Certificates
4. Third-party identity services (LDAP, Kuberos etc)

#### Static password files
Store a list of password, user and uid in, for example, a `csv` file.

Pass `--basic-auth-file=user-details.csv` to the `kube-apiserver`. `kube-apiserver` has to be restarted.

##### Using `kubeadm` tool
```yaml
apiVersion: v1
kind: Pod
metadata:
	creationTimestamp: null
	name: kube-apiserver
	namespace: kube-system
spec:
	containers:
	- command:
		- kube-apiserver
		- --allow-authorization-mode=Node,RBAC
		- --advertise-address=172.17.0.107
		- --allow-privileged=true
		- --enable-admission-plugins=NodeRestriction
		- --enable-bootstrap-token-auth=true
		- --basic-auth-file=user-details.csv
		image: k8s.gcr.io/kube-apiserver-amd64:v1.11.3
		name: kube-apiserver
```

**Create necessary roles and role bindings for these users**
```yaml
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
	namespace: default
	name: pod-reader
rules:
	- apiGroups:
	  resources: ["pods"]
	  verbs: ["get", "watch", "list"]

---

kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
	namespace: default
	name: read-pods
subjects:
	- kind: User
	  name: user1
	  apiGroup: rbac.authorization.k8s.io
roleRef:
	kind: Role
	name: pod-reader # this must match the name of the Role or ClusterRole
	apiGroup: rbac.authorization.k8s.io
```

>[!note]
>Optionally, use user groups to apply roles too

##### Using `curl` tool
```bash
curl -v -k https://master-node-ip:6443/api/v1/pods -u "user1:password123"
```
---

#### Static Token file
Instead of password, `csv` file holds user tokens.

```bash
curl -v -k https://master-node-ip:6443/api/v1/pods --header "Authorization: Bearer <user-token>"
```

>[!caution]
>Storing static files is not recommended as it is not secure — no longer available after `v1.19`
>- Consider volume mount while providing auth file in a kubeadm setup

#### KubeConfigs
Suppose we have a certificate and key for user clients.

```bash
curl https://my-kube-playground:6443/api/v1/pods \
--key admin.key
--cert admin.crt
--cacert ca.crt
```

The information is moved to a KubeConfig file
The file has 3 sections
- Clusters, clusters that users have access to
- Contexts, defines which user account is used to access a cluster
- Users, users that have access

```yaml
apiVersion: v1
kind: Config
clusters:
- name: my-kube-playground
  cluster:
	  certificate-authority: ca.crt
	  server: https://my-kube-playground:6443
contexts:
- name: my-kube-admin@my-kube-playground
  context:
	  cluster: my-kube-playground
	  uaser: my-kube-admin

users:
- name: my-kube-admin
  user:
	  client-certificate: admin.crt
	  client-key: admin.key # use full path
```

The file is left as is and is read by the `kubectl` command.

```bash
k config view
```

To change context,

```bash
k config use-context prod-user@production
```

##### Namespaces
The `context` section can take in an additional field called `namespace`. When the context is specified, the namespace switches automatically.

##### Certificates
Instead of using certificate files, use `certificate-authority-data` to pass the data as a `base64` encoded value.

### Service accounts
- Bots, third-party bots

---

Kubernetes does not keep track of users. However, we can create service accounts in Kubernetes.

---

# API Groups
- `/metrics` and `/healthz` API are used to monitor the health of the cluster
- `/version` is used to find out the version of Kubernetes
- `/logs` are used to integrate logging with third party applications

## `api` – Core group
Where all core functionalities exists, such as
- namespaces
- pods
- rc
- events
- endpoints

## `apis` – Named groups
More organised
- `/apps`, `/extensions`, `/networking.k8s.io` etc

API groups have `resources` and has a set of actions

For example, `/apis/apps/v1/deployments` have the relevant verbs to get, create, update deployments

---

To access the API with `curl`, we have to specify the certificate files.

Alternatively, use `k proxy` which uses `kubectl` config file on your machine

>[!caution]
>Kube Proxy is not the same as `kubectl proxy`
>- Kube proxy allows connectivity between pods
>- `kubectl proxy` allows you to access the `apiserver`

---

# Authorization
Authorization is about what a user can do after it gains access.

For example, an admin may be able to create or delete pods and deployments.

We do not want `developers` and `bots` to modify cluster config such as modifying nodes. However, we want them to be able to perform a certain set of operations.

- Restrict users to namespaces

## Mechanisms

### Node

### Attribute based authorization
Associate user with a set of permissions. For example,
- view, create, delete pods

A change in the attribute requires a restart of the API server

### Role based access control
Instead of associating user with rules, we create a role. Then associate users to that role.

#### Creating a role
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
	name: developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list", "get", "create", "update", "delete"]
  resourceNames: ["webapp"]
- apiGroups: [""]
  resources: ["ConfigMap"]
  verbs: ["create"]
```

We can be more specific with `resourceNames`. For example, restricting `developer` to only create `webapp` pods

#### Creating a role binding
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
	name: devuser-developer-binding
subjects:
# Specify the user details
- kind: User
  name: dev-user
  apiGroup: rbac.authorization.k8s.io/v1
roleRef:
# Specify the details of Roles
	kind: Role
	name: developer
	apiGroup: rbac.authorization.k8s.io/v1
```
Note that roles and role binding binds to namespaces

#### Check access
`k auth can-i create deployments`

Check access as another user,
`k auth can-i create deployments --as dev-user --namespace test`

### Webhook
Third party tool such as Open Policy Agent helps admission control and authorization.

User makes an API call to Kube API. Kube API queries the tool to decide if operation is allowed.

---

`authorization-mode` is set in Kube API server. If it is not specified, it defaults to `AlwaysAllow`.

If there are multiple values, users’ requests are authorized in each one it is specified.
If it is denied, it is still forwarded to the next authorization module. As soon as a module approves the user’s request, no more checks are done.

---
# Cluster Roles
>[!note]
>Roles and role bindings are `namespaced` — they are created within namespaces

Resources are namespaced or cluster-scoped.

Cluster scoped resources are those where a namespace is not specified.
For example
- nodes
- PV
- clusterroles
- PV
- clusterrolebindings
- certificatesigningrequests
- namespaces

---

### `clusterroles`
Cluster roles are like roles but cluster scoped resources.

For example,
- A cluster admin role can be created to provide cluster administrator permissions to view, create or delete **nodes** in the cluster
- Storage admin can be created to authorize a storage admin to create persistent volumes and claims

To implement this, first we create a `ClusterRole` resource:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
	name: cluster-administrator
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["list", "get", "create", "delete"]
```

Then, create another object called `ClusterRoleBinding` that links the user to the `ClusterRole`

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
	name: cluster-admin-role-binding
subjects:
- kind: User
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
roleRef:
	kind: ClusterRole
	name: cluster-administrator
	apiGroup: rbac.authorization.k8s.io
```

>[!note]
>You can create a `ClusterRole` for namespaced resources as well. This will give access to all specified resources across clusters

---

# Admission Controller
Suppose there is an API request to create a pod which is already authenticated and authorized. Then, for example, to ensure that the pod being created only use images from an internal registry and the image does not use the `latest` tag, disallow `runAsUser: 0`, and that metadata contains labels RBAC does not support this. However, admission controllers validates configuration or performs additional operation before the resource is created.

>[!example] `NamespaceExists`
>Suppose there is an API call to `--namespace blue` which does not exists.
>`NamespaceExists` throws an error. This is enabled by default.
>
>`NamespaceAutoProvision` creates a namespace if it does not exist.

---

To view enabled admission controllers:
```bash
kube-apiserver -h | grep enable-admission-plugins
```

With a `kubeadm` setup,
```bash
k exec kube-apiserver-controlplane -n kube-system -- kube-apiserver -h | grep enable-admission-plugins
```

```bash
ps -ef | grep kube-apiserver | grep admission-plugins
```

---

## Validating and Mutating Admission Controllers
### Validating admission controller
Admission controller such as `NamespaceExists` **validates** that the namespace exists

### Mutating admission controller
Admission controller `DefaultStorageClass` **mutates** a request to create a PVC and checks if it has a storage class mentioned in it. If there is no storage class, it will modify the request before the object is created.

>[!note]
>Mutating admission controllers are ran before validating admission controllers. This allows changes made by mutation admission controller to also be validated.

## Creating our own Admission Controller
1. Deploy our own Admission Webhook server that contains the admission controller logic
	- This can be an API server written in any language
	- It must accept, mutate and validate APIs and respond with a JSON object that the webserver accepts
	- Deploy the webhook server. This can be a standalone deployment or deployed within the Kubernetes cluster with a service
2. Configure webhook on Kubernetes by creating a webhook configuration object
```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration # MutatingWebhookConfiguration
metadata:
	name: "pod-policy.example.com"
webhooks:
- name: "pod-policy.example.com"
  # location of the webhook server
  clientConfig:
	  # If it was deployed externally
	  # url: "https://external-server.example.com"
	  service:
	    namespace: "webhook-namespace"
	    name: "webhook-service"
	  caBundle: "xxx" # Communicating over TLS
  rules:
  # Specifies when the webhook is called
    - apiGroups: [""]
      apiVersion: ["v1"]
      operations: ["CREATE"]
      resources: ["pods"]
      scope: "Namespaced"
```

---

# Custom resources definition
Resources have controllers that runs in the background to watch over the resources and make changes

To create a custom resource, first define a `Custom Resource Defintion`. Objects created are stored in `etcd`

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
	name: flighttickets.flights.com
spec:
	scope: Namespaced
	group: flights.com
	names:
	  kind: FlightTicket
	  singular: flightticket
	  plural: flighttickets
	  shortNames:
			- ft
	versions:
	  - name: v1
	    served: true
	    storage: true
	    schema:
		  openAPIV3Schema:
		    type: object
		    properties:
		      spec:
		        type: object
		        properties:
		          from:
		            type: string
		          to:
		            type: string
		          number:
		            type: integer
		            minimum: 1
		            maximum: 10
```

---

# Custom controllers
Controller monitors objects in the `etcd` and perform actions based on changes in the objects.

A controller is any process that runs in a loop and continuously monitors the Kubernetes cluster, and listening to specific objects being changed.

1. Write your custom controller in your preferred language (ie Go)
2. Build the controller and run the code
3. Package as Docker image
4. Deploy controller as pod or deployment

---
# Operator framework
Combine Custom Resource Definition and Custom controller into a single operator.

>[!example] `etcd`
>The `etcd` in Kubernetes is built with the Operator framework. At its core, it has the `EtcdCluster` and `EtcdController`. Unlike custom resources and controllers, operators can do more. For example:
>- `EtcdBackup`, `Backup Operator`
>- `EtcdRestore`, `Restore Operator`

All operators are available at `OperatorHub.io`