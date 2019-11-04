# Introducinc Prometheus and Grafana

This exercise will demonstrate ...

## Deploying Prometheus and Grafana

First we will install Prometheus and Grafana using Helm. We will install thse
from the `stable` repository. To see available repositories use:

```shell
$ helm repo list
stable  https://kubernetes-charts.storage.googleapis.com
```

The `stable` repository is configured when running `helm init` which we did in a
previous exercise. If you didn't do those exercises you might have to run `helm
init` now.

To look for available Helm chart you can use the `helm search` feature, e.g.:

```shell
$ helm search prometheus
stable/prometheus                       9.2.0           2.13.1          Prometheus is a monitoring system and time seri...
```

This show that Prometheus chart version 9.2.0 is available and that the version
of the Prometheus application in that chart is 2.13.1.  You most likely will see
newer versions when trying this out...

To install Prometheus and Grafana with settings suitable for the following
exercises use the following commands:

```shell
helm3 install prometheus stable/prometheus --version 9.2.0 -f kubernetes-appdev-katas/resources/values-prometheus.yaml
helm3 install grafana stable/grafana --version 4.0.1 -f kubernetes-appdev-katas/resources/values-grafana.yaml
```

After running these command you can inspect the installed Helm-based
applications with `helm ls`:

```shell
$ helm ls
grafana         user1           1               2019-11-04 09:23:52.163779429 +0000 UTC deployed        grafana-4.0.1
prometheus      user1           1               2019-11-04 08:49:53.769610017 +0000 UTC deployed        prometheus-9.2.0
```

Also, inspect the PODs that these applications are based upon:

```shell
$ kubectl get pods
grafana-5c7b9b967f-pnkd2             2/2     Running   0          71s
prometheus-server-868b8cdb59-d7gpq   2/2     Running   0          48s
```

Grafana is deployed **without TLS** and as such this is not a deployment that is
suitable for production use. Grafana is exposed with a Kubernetes service of
type `LoadBalancer`. Use the following commands to get the external IP address
and the Grafana admin password:

```shell
$ kubectl get svc grafana -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
$ kubectl get secret grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

