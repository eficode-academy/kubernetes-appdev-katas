# Horizontal POD Autoscaling with POD Preemption

This exercise will demonstrate horizontal POD autoscaling using the sentences
application and with preemption of lower priority PODs. Preempting PODs
(stopping and deleting from the cluster) is necessary when we do not want to add
additional nodes to our cluster but instead want to change how we used the
current cluster compute resources.

First, ensure that the sentences application is deployed:

```shell
kubectl apply -f sentences-app/deploy/kubernetes/
```

Next, in a separate shell, run the following to monitor resources:

```shell
watch kubectl get pods,hpa,deploy
```

You should see one POD of each of the microservices:

```
NAME                                  READY   STATUS    RESTARTS   AGE
pod/sentence-age-78856f44bd-5w2zx     1/1     Running   0          7m
pod/sentence-name-6d967d5dbd-js8pb    1/1     Running   0          7m
pod/sentences-5b56894f96-sthgh        1/1     Running   0          7m

NAME                                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.extensions/sentence-age      1/1     1            1           7m
deployment.extensions/sentence-name     1/1     1            1           7m
deployment.extensions/sentences         1/1     1            1           7m
```

With the deployment status, pay particular attantion to the various
columns. Different version of Kubernetes and kubectl use slightly different
formats, but generally you should be able to observe that not all the requested
nginx PODs become 'AVAILABLE'.

Next we apply some load to the sentence application, start a load generator as
follows (ApacheBench - see YAML file for details):

```shell
kubectl apply -f resources/load-generator.yaml
```

> A single load generator should be sufficient for this exercise, however,
> additional load generators can be created by scaling the load generator
> deployment.

In another shell run the following command to monitor the resource consumption
of each of the runnung PODs:

```shell
watch kubectl top pods
```

**If you are doing this exercise on a shared Kubernetes cluster, you should
  coordinate the creation of the dummy workload mention below with the other
  Kubernetes cluster users**

> Next, we create a dummy workload with the sole purpose of consuming our
> remaining compute resources (CPU resources in this case)
>
> ```shell
> kubectl apply -f resources/nginx-deplyment.yaml
> ```
>
> Generally, both the nginx workload and the three microservices in the sentence
> application requests 0.25 CPUs. To see our used CPU resources, use the following
> command:
>
> ```shell
> kubectl describe nodes |grep '^  Resource' -A3
> ```
>
> This will show our current cluster-wide memory and CPU usage.
>
> Scale the nginx dummy workload such that it consumes all our CPU resources. This
> should result in some PODs ending in a `Pending` state, i.e. adjust the number
> of replicas to suit your allowed `requests.cpu` quota:
>
> ```shell
> kubectl scale --replicas 7 deployment nginx-guaranteed
> ```
>
> If you have scaled the nginx-guaranteed deployment beyond your current quota,
> you will see a difference between the `DESIRED` and `AVAILABLE` columns in the
> deployment listing.

Create a HorizontalPODAutoscaler object to automatically scale the sentence
application:

```shell
kubectl apply -f sentences-app/deploy/hpa.yaml
```

With load being applied to the sentence application, the HorizontalPODAutoscaler
will try increase the replica count, however the newly created POD end up in a
`Pending` state.  The reason for this can be seen by inspecting the POD
resource:

```shell
kubectl describe pod <pod-name-xxx-yyy>
```

with which you should see, that the POD cannot be schedule due to insufficient
available CPU resources.

This is because all our PODs have the same priority, i.e. no PODs are evicted to
make room for our new POD. To see the QoS class and priority of all PODs, try
the following command:

```shell
kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.qosClass}{"\t"}{.spec.priority}{"\n"}{end}'
```

This will show that all our PODs have a priority of zero.

To ensure that the sentence application is able to evict the PODs from the nginx
deployment, we need to increase the POD priority of the sentence application.

> The following assumes some pre-deployed priority classes. If you are running
> this on a self-managed Kubernetes cluster, you might need to deploy
> `resources/priority-classes.yaml` yourself.

To see which PriorityClasses we have available, use the following command:

```shell
kubectl get priorityclasses
```

This will show, that we have a `medium-priority` class with a priority value of
`100`.

To ensure that our appliction is able to make CPU resources available by
evicting nginx POD, we change the priority of the sentence application by adding
a `priorityClassName` statement to the sentence application deployment YAML:

...
spec:
  ...
  template:
    ...
    spec:
      priorityClassName: medium-priority
```

**Which deployment should we change?**: The sentence application consist of
three deployments, and it's the one named `sentences` in the file
`sentences-app/deploy/kubernetes/sentences-deployment.yaml` file which is not
able to scale. *Will it be sufficient to add a `priorityClassName` to this main
microservice?* When the Kubernetes scheduler evicts a POD to make room for
another main sentence POD, it will choose one of the other PODs with a lower
priority. This could be one of the other microservices in the sentence
application, and since the main microservice depends on these, we are basically
breaking the whole application in our effort to scale it!  *We need to add
priority to all deployments in the sentence application!*

When priority have been added to the sentence application, redeploy it:

```shell
kubectl apply -f sentences-app/deploy/kubernetes/
```

The effect should be eviction of some of the nginx PODs and multiple `sentences`
PODs.

# Cleanup

```shell
kubectl delete deployment multitool
kubectl delete deployment nginx-guaranteed
kubectl delete -f sentences-app/deploy/kubernetes/hpa.yaml
kubectl delete -f sentences-app/deploy/kubernetes/
```
