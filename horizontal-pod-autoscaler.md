# Horizontal POD Autoscaling

This exercise will demonstrate horizontal POD autoscaling using the sentences
application.

The sentences application have three microservices; A main service that builds a
sentence from the output from the two other services. With this application, the
main service will be the initial bottleneck, which we will see shortly.

First, ensure that the sentences application is deployed:

```shell
kubectl apply -f sentences-app/deploy/kubernetes/
```

Next, in a separate shell, run the following to monitor the running PODs:

```shell
watch kubectl get pods
```

You should see one POD of each of the microservices:

```
sentence-age-f747b9d95-tw4ff       1/1     Running   0          101m
sentence-name-8448ccfd89-vsv7v     1/1     Running   0          101m
sentences-66fb575cf8-2sdw2         1/1     Running   0          21m
```

In another shell run the following command to monitor the resource consumption
of each of the runnung PODs:

```shell
watch kubectl top pods
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
kubectl apply -f resources/load-generator.yaml
```

> A single load generator should be sufficient for this exercise, however,
> additional load generators can be created by scaling the multitool deployment
> and running more `ab` commands.

All three of the microservices PODs have CPU `requests` and `limits` set to 0.5
CPUs, i.e. we now see the main microservice max-out around 0.5 CPU while the
other two microservices use much less:

```
NAME                               CPU(cores)   MEMORY(bytes)
sentence-age-f747b9d95-tw4ff       107m         21Mi            
sentence-name-8448ccfd89-vsv7v     106m         20Mi            
sentences-66fb575cf8-cg7c8         500m         33Mi
```

If we want to scale the main microservice, we could do it manually with:

```shell
kubectl scale --replicas 4 deployment sentences
```

However, this would obviously be a manual process. If we want Kubernetes
automatically to adjust the number of replicas based on e.g. the CPU load of the
PODs in a deployment, we could use the HorizontalPODAutoscaler.

Lets create a HorizontalPODAutoscaler resource that adjusts the number of PODs
such that the average CPU load of the PODs are 80% of their requested CPU
allocation:

```shell
kubectl apply -f sentences-app/deploy/hpa.yaml
```

Next, in a separate shell, run the following to monitor the status of the
HorizontalPODAutoscaler (using the abbreviation 'hpa' for
HorizontalPODAutoscaler):

```shell
watch kubectl get hpa sentences
```

This will initially show 100% measured load (relative to CPU requests), a target
of 80% and currently one replica:

```
NAME        REFERENCE              TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
sentences   Deployment/sentences   100%/80%   1         5         1          27s
```

After a short while, the horizontal POD autoscaler will have scaled the
`sentences` deployment to five pods.

When stopping the load generator, the horizontal POD autoscaler will slowly
scale the deployment down to 1 POD again.

# Cleanup

```shell
kubectl delete deployment multitool
kubectl delete -f sentences-app/deploy/kubernetes/hpa.yaml
kubectl delete -f sentences-app/deploy/kubernetes/
```
