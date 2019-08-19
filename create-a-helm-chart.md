# Create an Helm Chart

This exercise will create a simple Helm chart for the sentence application.  The
chart will be 'simple' in the sense that it will not provide support for
customizing application parameters.

> Helm comes in two different major version - 2 and 3. In the following we will
> provide command-lines for both and indicate with the command name which
> version of Helm the command refers to, e.g. for Helm v2 we will use:
> ```shell
> $ helm2 ...
>```
> and for Helm v3 we will use:
> ```shell
> $ helm3 ...
>```
> The numbers should obviously be removed before running the command since the
> Helm command will be `helm` irrespective of the Helm version installed.

In the `sentences-app/deploy/kubernetes/` folder we have Kubernetes YAML
definitions for the three microservices that make up the sentence application
(tree Deployments and tree Services):

```shell
$ ls -la sentences-app/deploy/kubernetes/
sentences-age-deployment.yaml
sentences-age-svc.yaml
sentences-deployment.yaml
sentences-name-deployment.yaml
sentences-name-svc.yaml
sentences-svc.yaml
```

To create a simple Helm chart we can use `helm create` to create a template chart:


```shell
$ mkdir helm-chart
$ cd helm-chart
$ helm create sentence-app
```

Since we will use the sentence application YAML as templates for the chart we
delete the ones created by `helm create`:

```
$ rm -rf sentence-app/templates/*
$ echo "" > sentence-app/values.yaml
```

This provides us with skeleton chart without any template files. Next, we copy
the original Kubernetes YAML files to the template folder:

```shell
$ cp -v ../sentences-app/deploy/kubernetes/*.yaml sentence-app/templates/
```

Now we have a Helm chart for our sentences application - it is simple in the
sense that it has no configurable values, but it is a complete installable chart
and it will use the correct sentence application Kubernetes YAML definitions.

Before deploying the chart, we run a static validation of the chart:

```shell
$ helm lint sentence-app/
==> Linting sentence-app/
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, no failures
```

Normally a chart is fetched from a chart registry (like a container registry),
however, a chart stored locally can also be deployed with Helm. To deploy the
chart from the newly created chart run the following:

```shell
$ helm2 install --name sentences sentence-app/
$ helm3 install sentences sentence-app/
```

Running this command produce the following output, which specify which resources
that where created:

```
NAME:   sentences
LAST DEPLOYED: Thu Jul 11 14:26:22 2019
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1/Deployment
NAME           READY  UP-TO-DATE  AVAILABLE  AGE
sentence-age   0/1    1           0          0s
sentence-name  0/1    1           0          0s
sentences      0/1    1           0          0s

==> v1/Pod(related)
NAME                            READY  STATUS             RESTARTS  AGE
sentence-age-7cfcb9755b-bjg44   0/1    ContainerCreating  0         0s
sentence-name-757fdf5c56-mj9dz  0/1    ContainerCreating  0         0s
sentences-76d8456745-qd7qb      0/1    ContainerCreating  0         0s

==> v1/Service
NAME           TYPE       CLUSTER-IP      EXTERNAL-IP  PORT(S)   AGE
sentence-age   ClusterIP  10.96.119.239   <none>       5000/TCP  0s
sentence-name  ClusterIP  10.110.60.80    <none>       5000/TCP  0s
sentences      ClusterIP  10.103.227.249  <none>       5000/TCP  0s
```

To see the applications installed with Helm use the `helm ls` operation:

```shell
$ helm ls
NAME         REVISION   UPDATED                    STATUS     CHART                APP VERSION   NAMESPACE   
sentences    1          Wed Aug 14 08:44:55 2019   DEPLOYED   sentence-app-0.1.0   1.0           default
```

To see the Kubernetes YAML which Helm used to install the application use the `helm get` operation:

```shell
$ helm get sentences
```

In our case this will be identical to the YAML files we copied previously since
we haven't provided any means of customizing the application installation.

# Food for Thought

In this exercise we created a single Helm chart for the complete application
even though its based on three microservices. When would it make sense to have a
Helm chart for each microservice?

# Cleanup

Delete the application installed with Helm:

```shell
$ helm2 delete sentences --purge
$ helm3 delete sentences
```
