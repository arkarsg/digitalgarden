In Kubernetes, every object requires a `yaml` file.

If there are changes to be made, every `yaml` file needs to be changed and updated.

Helm does not care about the application or the resources. It looks at each resource and takes care of each one individually.

Known as a package manager for Kubernetes

Treat Kubernetes apps as apps instead of collection of objects.

---

# Helm charts

Suppose we have
- `deployment.yaml`
- `secret.yaml`
- `pv.yaml`
- `pvc.yaml`
- `service.yaml`

for an application.

Some of the values might change depending on the environment, for example, different image versions, different admin password, different storage providers.

First, the `yaml` files are transformed into *templates*. Values are turned into variables:
```yaml
# PV yaml
# PV definition
spec:
	capacity:
		storage: {{ .Values.storage }}

# More PV definition
```

These `Values` are stored in `values.yaml`

```yaml
# other values
storage: 20Gi
# More values
```

Now the application can be changed by modifying a single file called `values.yaml`

**Templates and the `values` form a ==Helm chart==**

`chart.yaml` file contains information about the chart itself, such as,
- name of the chart
- description of what the chart is
- keywords associated with the application
- information about the maintainers

>[!note] Repositories
>Community uploaded charts are available at `artifacthub.com`
>
>We can search for charts using
>```bash
>helm search hub wordpress
>```
>Add a custom repository
>```bash
>helm repo add bitnami https://charts.bitnami.com/bitnami
>```
>
>Find repos
>```bash
>helm repo list
>```

---

### Installing 
Install chart on cluster
```bash
helm install [release-name] [chart-name]
```

- Each installation of a chart is called a **release** and each release has a **release-name**
- Each release is completely independent of each other

#### Find out installed charts
```bash
helm list
```

#### Uninstall
```bash
helm uninstall [release-name]
```

#### Download a chart
- Download a chart without installing
- A chart is normally downloaded as a `tar` file
```bash
helm pull --untar bitnami/wordpress
```

