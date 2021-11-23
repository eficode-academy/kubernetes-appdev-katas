# Horizontal POD Autoscaling

This exercise will demonstrate horizontal POD autoscaling using the sentences
application.

The sentences application have three microservices; A main service that builds a
sentence from the output from the two other services. With this application, the
main service will be the initial bottleneck, which we will see shortly.

If you already have the sentences application deployed, 
from the last exercise, scale the `sentences` deployment down to
`1` replica and delete the `load-generator` deployment.

> If you don't have the sentences application deployed,
> deploy it with either `apply` like in the 
> [hello-sentences-app](hello-sentences-app.md#running-the-sentences-application-on-kubernetes)
> exercise or using Helm, if you did the [create-a-helm-chart](create-a-helm-chart.md) exercise.

Next, in a separate shell, run the following to monitor the running PODs:

```shell
$ watch kubectl get pods
```

You should see one POD of each of the microservices:

```
sentence-age-f747b9d95-tw4ff       1/1     Running   0          101m
sentence-name-8448ccfd89-vsv7v     1/1     Running   0          101m
sentences-66fb575cf8-2sdw2         1/1     Running   0          21m
```

In another shell run the following command to monitor the resource consumption
of each of the running PODs:

```shell
$ watch kubectl top pods
```

Since there is no load on the microservices, you should see a low CPU
consumption - something like the following, where 1m is one milli-CPU,
i.e. 0.001 of a full cluster-node CPU:

```
NAME                               CPU(cores)   MEMORY(bytes)
sentence-age-f747b9d95-tw4ff       1m           21Mi            
sentence-name-8448ccfd89-vsv7v     1m           21Mi            
sentences-66fb575cf8-2sdw2         1m           21Mi 
```

Next we apply some load to the sentence application, start a load generator as
follows (ApacheBench - see YAML file for details):

```shell
$ kubectl apply -f resources/load-generator.yaml
```

> A single load generator should be sufficient for this exercise, however,
> additional load generators can be created by scaling the load generator
> deployment.

All three of the microservices PODs have CPU `requests` and `limits` set to 0.25
CPUs, i.e. we now see the main microservice max-out around 0.25 CPU while the
other two microservices use much less:

```
NAME                               CPU(cores)   MEMORY(bytes)
sentence-age-f747b9d95-tw4ff       52m          21Mi
sentence-name-8448ccfd89-vsv7v     53m          20Mi
sentences-66fb575cf8-cg7c8         250m         33Mi
```

If we want to scale the main microservice, we could do it manually with:

```shell
$ kubectl scale --replicas 4 deployment sentences
```

However, this would obviously be a manual process. If we want Kubernetes
automatically to adjust the number of replicas based on e.g. the CPU load of the
PODs in a deployment, we could use the HorizontalPODAutoscaler.

Lets create a HorizontalPODAutoscaler resource that adjusts the number of PODs
such that the average CPU load of the PODs are 65% of their requested CPU
allocation:

```shell
$ kubectl apply -f sentences-app/deploy/hpa.yaml
```

Next, in a separate shell, run the following to monitor the status of the
HorizontalPODAutoscaler (using the abbreviation 'hpa' for
HorizontalPODAutoscaler):

```shell
$ watch kubectl get hpa sentences
```

This will initially show 100% measured load (relative to CPU requests), a target
of 80% and currently one replica:

```
NAME        REFERENCE              TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
sentences   Deployment/sentences   100%/65%   1         5         1          27s
```

After a short while, the horizontal POD autoscaler will have scaled the
`sentences` deployment to five pods (or at least more then one):

```
NAME                              CPU(cores)   MEMORY(bytes)
loadgen-5fff765cc-b8ntf           24m          1Mi
sentence-age-f747b9d95-tw4ff      142m         27Mi
sentence-name-8448ccfd89-vsv7v    145m         25Mi
sentences-66fb575cf8-4kkcl        209m         28Mi
sentences-66fb575cf8-6w2lr        161m         27Mi
sentences-66fb575cf8-cgcxl        167m         26Mi
sentences-66fb575cf8-wtqcc        121m         27Mi
sentences-66fb575cf8-xds6f        140m         26Mi
```

Now delete the load generator:

```shell
$ kubectl delete -f resources/load-generator.yaml
```

When stopping the load generator, the horizontal POD autoscaler will slowly
scale the deployment down to 1 POD again.

# Cleanup

Note that the load generator might have been deleted above.

```shell
$ kubectl delete -f resources/load-generator.yaml
$ kubectl delete -f sentences-app/deploy/hpa.yaml
$ kubectl delete -f sentences-app/deploy/kubernetes/
```
