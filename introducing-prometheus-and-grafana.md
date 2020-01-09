# Introducing Prometheus and Grafana

This exercise will demonstrate deploying the Prometheus and Grafana applications
using Helm. We will also deploy the sentences application and inspect how
metrics are propagated from the application through Prometheus and displayed in
Grafana.

## Deploying Prometheus and Grafana

First we will install Prometheus and Grafana using Helm. We will install them
from the `stable` repository. To see available repositories use:

First add a repository to your Helm installation:

```shell
$ helm3 repo add stable https://kubernetes-charts.storage.googleapis.com/
```

Next, you can inspect your Helm repositories with `helm repo list`:

```shell
$ helm repo list
stable  https://kubernetes-charts.storage.googleapis.com
```

To look for available Helm chart you can use the `helm search` feature, e.g.:

```shell
$ helm2 search prometheus
$ helm3 search repo prometheus
stable/prometheus                       9.2.0           2.13.1          Prometheus is a monitoring system and time seri...
```

This show that Prometheus chart version 9.2.0 is available and that the version
of the Prometheus application in that chart is 2.13.1.  You most likely will see
newer versions when trying this out...

To install Prometheus and Grafana with settings suitable for the following
exercises use the following commands:

```shell
$ helm3 install prometheus stable/prometheus --version 9.2.0 -f resources/values-prometheus.yaml
$ helm3 install grafana stable/grafana --version 4.0.1 -f resources/values-grafana.yaml
```

> This exercise assume a Kubernetes cluster with metrics support. Most managed
> Kubernetes solutions will have support for metrics. On self-deployed clusters
> one might need to deploy the metrics-server application:
>
> ```shell
> $ helm3 install metrics-server stable/metrics-server --version 2.8.8 --set args[0]="--kubelet-insecure-tls"
> ```

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

Note that Grafana is deployed **without TLS** and as such this is not a
deployment that is suitable for production use.

Grafana is exposed with a Kubernetes service of type `NodePort`. Use the
following commands to get the external IP address/port and the Grafana `admin`
user password:

```shell
$ kubectl get -o jsonpath="{.spec.ports[0].nodePort}" services grafana
$ kubectl get nodes -o wide
$ kubectl get secret grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

## Deploying the Application

The sentences application can be deployed with the following command.

```shell
$ kubectl apply -f sentences-app/deploy/kubernetes/
```

After this, we should have 5 PODs running (Prometheus, Grafana and three PODs
for the sentences application).  To verify that the application is running, look
up the main service and node-port and fetch a result with curl as we did in the
[hello-sentences-app](hello-sentences-app.md) exercise.

## Debugging Metrics

In the following we will look into:

- How to manually query metrics exported from an application prepared for Prometheus
- How Prometheus maintains status for each auto-discovered scrape-targets (like our application PODs)
- How we can query and display metrics with Prometheus, i.e. without Grafana

Going through these steps will not only give good insight into the metrics
framework but also show the primary techniques necessary when application
metrics fail to be available in Grafana.

### Debugging Metrics From PODs

First, lets manually query the metrics from our sentences application. Remember
that each microservice exports a metric called `sentence_requests_total` which
is a counter that increments for each request the microservices processes.

The sentences application exports metrics on port 8080 and path '/metrics'. Any
port can generally be used, and we will later see how Prometheus figures out
which port to scrape for metrics.

Query metrics API of the sentences deployment similarly to how you fetched
sentences. The difference is that we add the '/metrics' path to the query:

```shell
$ curl -s <NODE-IP>:<PORT>/metrics | egrep '^sentence'
```

We use `egrep` here to filter out the essential information, and we will see the
following output:

```
sentence_requests_total{type="sentence"} 6.0
```

> If you get no results here, it could be because you skipped verifying the
> initial deployment of the sentences application. Normally, metrics with a zero
> value are not reported, i.e. until you fetch a sentence for the first time,
> the curl above will return nothing.

Try fetching more sentences and metrics to see the `sentence_requests_total`
metric increment.

This show that we have a metric with name `sentence_requests_total` with a label
`type` that have the value `sentence`. The other microservices `age` and `name`
use values `age` and `name` respectively for the `type` label. Metrics can have
many labels and with these we can separate metrics into different dimensions,
e.g. microservice type, versions etc. The metric name `sentence_request_total`
can be considered the *what* and the labels define the *who*.

Our `curl` operation showed that the metrics API on the sentences application
works as expected.  If this had not worked, we should debug the microservice
itself.

### Debugging Prometheus Metrics Scraping

Next, we look into Prometheus. The Prometheus GUI is exposed using a
NodePort-type service. Look up the node port as above and open the GUI in a web
browser.

```shell
$ kubectl get -o jsonpath="{.spec.ports[0].nodePort}" services prometheus-server
```

When you have the Prometheus GUI op, select the `Status` menu item and then the
`Targets` option as shown below. Scroll down to the section with the heading `kubernetes-pods (3/3 up)`

This shows the list of targets that Prometheus has identified through the
Kubernetes API. We see that three POD target show up with the labels matching
the three microservices of the sentences application. If our list of scrape
targets do not match our expectation we should verify that 1) Our Kubernetes
resources are correctly annotated to tell Prometheus to scrape then and that the
port and path is correct and 2) that Prometheus is deployed with proper
Kubernetes authorization to auto-discover scrape targets through the Kubernetes
API.

![prometheus-scrape-targets](images/prometheus-scrape-targets.png)

Next, select the `Graph` menu item and type in `sentence_requests_total` in the
query box as shown below and press return. This will show the number of requests
handled by each of the microservices in the sentences application.  The fact
that we see metrics here verifies that the metrics of the sentences application
are available from Prometheus.

![prometheus-scrape-targets](images/prometheus-graph.png)

## Explore Metrics in Grafana

The GUI Prometheus is mostly used for low-level debugging and metrics are
typically visualized with Grafana since Grafana provides many more options for
building dashboards.

When logged-in to Grafana go to the *camera shutter* option in the left-side,
which is the metrics *explore* feature. This feature provide access to a simple
metrics query option, which often is used instead of directly accessing
Prometheus when we are beyond basic debugging of the metrics feature.

In the query box type the metrics name `sentence_requests_total` as shown below:

![prometheus-scrape-targets](images/grafana-explore.png)

This shows that Grafana can access metrics from Prometheus.

## Deploying a Dashboard

Dashboards can be created manually but often an existing dashboard should be
used.  Grafana supports dynamically loading of dashboards through Kubernetes
ConfigMaps. If we have an existing dashboard in JSON format, we can simply
create a ConfigMap containing the JSON file and annotate the ConfigMap to let
Grafana know it should use the content as a dashboard.

To install a dashboard for the sentences application create and annotate a
ConfigMap as follows:

```shell
$ kubectl create configmap dashboard --from-file sentences-app/dashboard.json
$ kubectl label configmap dashboard grafana_dashboard='1'
```

After this you will be able to use the dashboard in Grafana.  Go to the *Window*
option above the *camera shutter* option and select `Home` and/or `Manage` to
see newly loaded dashboards.

To generate some load on the sentences application, use the following command
and watch the effect in the dashboard:


```shell
$ kubectl apply -f resources/load-generator.yaml
```

After a short while, you should see the effect of the generated load in the
dashboards with *requests/s* and also the *POD cpu usage*.

> If you are doing this exercise after having done the auto-scaling section, you
> could deploy the HorisontalPODAutoscaler resource to see auto-scaling and the
> dashboard with POD counts for the individial microservices to change.
>
> ```shell
> kubectl apply -f sentences-app/deploy/hpa.yaml
> ```

# Cleanup

Delete the applications and additional services with the following commands.

*If you are going to proceed to the next Prometheus/Grafana exercise, you might
want to leave everything running for now*

```shell
$ kubectl delete -f sentences-app/deploy/kubernetes/
$ helm3 delete grafana
$ helm3 delete prometheus
$ kubectl delete configmap dashboard
$ kubectl delete -f resources/load-generator.yaml
$ kubectl delete -f sentences-app/deploy/hpa.yaml
```
