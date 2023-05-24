# Horizontal Pod Autoscaling

This exercise will demonstrate horizontal pod autoscaling using the sentences
application.

With this application, the main service will be the initial bottleneck, which we will see shortly.

- Scale the sentences application to 1 replica: `kubectl scale --replicas 1 deployment sentences`
- Delete the load generator: `kubectl delete -f resources/load-generator.yaml`

<details>
<summary>:bulb: > If you don't have the sentences application deployed</summary>

The sentences application can be deployed with the following command.

```shell
$ kubectl apply -f sentences-app/deploy/kubernetes/
```
</details> 


Next, in a separate shell, run the following to monitor the running pods:

```shell
$ watch kubectl get pods
```

You should see one pod of each of the microservices:

```
sentence-age-f747b9d95-tw4ff       1/1     Running   0          101m
sentence-name-8448ccfd89-vsv7v     1/1     Running   0          101m
sentences-66fb575cf8-2sdw2         1/1     Running   0          21m
```

In another shell run the following command to monitor the resource consumption
of each of the running pods:

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

All three of the microservices pods have CPU `requests` and `limits` set to 0.25
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
pods in a deployment, we could use the HorizontalPodAutoscaler.

Lets create a HorizontalPodAutoscaler (v1) resource that adjusts the number of pods
such that the average CPU load of the pods are 65% of their requested CPU
allocation:

```shell
$ kubectl apply -f sentences-app/deploy/hpa.yaml
```

Next, in a separate shell, run the following to monitor the status of the
HorizontalPodAutoscaler (using the abbreviation 'hpa' for
HorizontalPodAutoscaler):

```shell
$ watch kubectl get hpa sentences
```

This will initially show 100% measured load (relative to CPU requests), a target
of 65% and currently one replica:

```
NAME        REFERENCE              TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
sentences   Deployment/sentences   100%/65%   1         5         1          27s
```

After a couple of minutes, the HorizontalPodAutoscaler will have scaled the
`sentences` deployment up w.r.t. the load:

```
NAME                              CPU(cores)   MEMORY(bytes)
loadgen-5fff765cc-b8ntf           24m          1Mi
sentence-age-f747b9d95-tw4ff      142m         27Mi
sentence-name-8448ccfd89-vsv7v    145m         25Mi
sentences-66fb575cf8-4kkcl        209m         28Mi
sentences-66fb575cf8-6w2lr        161m         27Mi
```

Now delete the load generator:

```shell
$ kubectl delete -f resources/load-generator.yaml
```

When stopping the load generator, the HorizontalPodAutoscaler will slowly
scale the deployment down to `1` pod again.

<details>
<summary>:bulb: > Why does it not scale down/up instantly? </summary>
When the load decreases, the HPA intentionally waits a certain amount of time before scaling the app down. This is known as the cooldown delay and helps that the app is scaled up and down too frequently. The result of this is that for a certain time the app runs at the previous high replica count even though the metric value is way below the target. This may look like the HPA doesn't respond to the decreased load, but it eventually will.

For more information read this brilliant blogpost by Expedia: https://medium.com/expedia-group-tech/autoscaling-in-kubernetes-why-doesnt-the-horizontal-pod-autoscaler-work-for-me-5f0094694054

</details>

# Cleanup

Note that the load generator might have been deleted above.

```shell
$ kubectl delete -f resources/load-generator.yaml
$ kubectl delete -f sentences-app/deploy/hpa.yaml
$ kubectl delete -f sentences-app/deploy/kubernetes/
```
