# Create an Helm Chart

This exercise will create a simple Helm chart for the sentence application.

In the `sentences-app/deploy/kubernetes/` folder we have Kubernetes YAML
definitions for the three microservices that make up the sentence application
(tree Deployment and tree Services):

```shell
$ ls -la sentences-app/deploy/kubernetes/
sentences-age-deployment.yaml
sentences-age-svc.yaml
sentences-deployment.yaml
sentences-name-deployment.yaml
sentences-name-svc.yaml
sentences-svc.yaml
```

To create a simple Helm chart


```shell
$ mkdir helm-chart
$ cd helm-chart
$ helm create sentence-app
$ rm -rf sentence-app/templates/*
```

This create a skeleton chart without any template files. Next, we copy the
original Kubernetes YAML files to the template folder:

```shell
$ cp -v ../sentences-app/deploy/kubernetes/*.yaml sentence-app/templates/
```

This way we have a very simple Helm chart for our sentences application - it has
no configurable values, but it will use the correct Kubernetes YAML

Before deploying the chart, we run a static validation of the chart:

```shell
$ helm lint sentence-app/
==> Linting sentence-app/
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, no failures
```

Normally a chart is fetched from a chart registry when deployed, however, a
chart stored locally can also be deployed with Helm. To deploy the chart from
the newly created chart run the following:

```shell
$ helm install --name sentences sentence-app/
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