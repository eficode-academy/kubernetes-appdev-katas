# Prometheus Metrics and Grafana Dashboards

In this exercise we will build upon the knowledge from the [Introducing
Prometheus and Grafana](introducing-prometheus-and-grafana.md) exercise.

We will learn about Prometheus query functions and operators and we will build a
dashboard for the sentences application.

This exercise assumes you have Prometheus, Grafana and the sentences application
and load generator running. If not, see the [Introducing Prometheus and
Grafana](introducing-prometheus-and-grafana.md) exercise.

In addition, insure that the front-end service is scaled to three replicas:

```shell
$ kubectl scale --replicas 3 deployment sentences
```

## Choose Metric Queries

The first thing to do before creating a dashboard is to chose a query that
return a metric we want to display in a dashboard.  Go to the Grafana *explore*
feature and in the query box type the metrics name `sentence_requests_total`.

Since this metric is a counter which increases on each request, we will see a
curve going towards the top-right part of the Grafana graph of the
`sentence_requests_total` metric.

Number of requests are typically easier to understand when given over time. We
can change the query which Grafana sends to Prometheus to 

```
rate(sentence_requests_total[2m])*60
```

With this query, Prometheus will return metrics with a per-second average
measured over the last 2 minutes. We can include general math in the query also,
and we here convert the metric into a requests/minute metric.

We now have found the first metric query for our dashboard.

## Metric Labels

The data returned with the above query results in five different curves and the
table also show five results. The results differ in the labels, e.g. observe the
value of the `type` label -- you should be able to find `sentence`, `age` and
`name`.

In addition, we see that e.g. the `kubernetes_pod_name` label have different
values matching the actual POD names of our deployed PODs. Compare the
`kubernetes_pod_name` label values with the following command to verify this:

```shell
$ kubectl get pods
```

Thus we have a `sentence_request_total` from each POD, however, for our second
metric query in our dashboard we want request/minute for each microservice type.

This can be done by using the Prometheus `sum()` aggregation operator. First,
enter the following query into Grafana:

```
sum(rate(sentence_requests_total[2m]))
```

this results in a single curve, hence all the `sentence_requests_total` metrics
from all microservices have been aggregated into a single metric which is not
what we wanted.

We need to specify to the `sum()` operator across which labels we want
aggregation. Instead enter the following query which specifies the `sum()` to
happen across the values of the `type` label.

```
sum by (type) (rate(sentence_requests_total[2m]))
```

This will be our second metric query for our dashboard.

## Create a Dashboard





## Cleanup

See cleanup in the [Introducing Prometheus and
Grafana](introducing-prometheus-and-grafana.md) exercise