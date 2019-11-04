# Introducinc Prometheus and Grafana

This exercise will demonstrate ...

First we will install Prometheus and Grafana using Helm. We will install thse
from the `stable` repository. To see available repositories use:

```
$ helm repo list
stable  https://kubernetes-charts.storage.googleapis.com
```

The `stable` repository is configured when running `helm init` which we did in a
previous exercise. If you didn't do those exercises you might have to run `helm
init` now.

To look for available Helm chart you can use the `helm search` feature, e.g.:

```
$ helm search prometheus
stable/prometheus                       9.2.0           2.13.1          Prometheus is a monitoring system and time seri...
```

This show that Prometheus chart version 9.2.0 is available and that the version
of the Prometheus app in that chart is 2.13.1.  To install Prometheus with
settings suitable for the following exercises use the following command:

```
helm3 install prometheus stable/prometheus --version 9.2.0 -f kubernetes-appdev-katas/resources/values-prometheus.yaml
```

After running these command you can inspect the installed Helm-based
applications with `helm ls`:

```
$ helm ls
prometheus      user1           1               2019-11-04 08:49:53.769610017 +0000 UTC deployed        prometheus-9.2.0
```

Also, inspect the PODs that these applications are based upon:

```
$ kubectl get pods
prometheus-server-868b8cdb59-d7gpq   2/2     Running   0          48s
```