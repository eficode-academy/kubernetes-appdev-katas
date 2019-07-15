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

In another shell, run the following to monitor the status of the deployments and
in particular the number of replicas in each:

```shell
watch kubectl get deployment
```

This will create an output like this:

```
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
sentence-age       1/1     1            1           3m7s
sentence-name      1/1     1            1           3m7s
sentences          1/1     1            1           3m7s
```

Pay particular attantion to the `UP-TO-DATE` column (the requested replicas) and
the `AVAILABLE` column (the number of running PODs).

Next, we create a dummy workload with the sole purpose of consuming our
remaining compute resources (CPU resources in this case)

```shell
kubectl apply -f resources/nginx-deplyment.yaml
```

Generally, both the nginx workload and the three microservices in the sentence
application requests 0.5 CPUs. To see our allowed quota, use the following
command:

```shell
quota
```

Scale the nginx dummy workload such that it consumes all our CPU resources. This
should result in some PODs ending in a `Pending` state, i.e. adjust the number
of replicas to suit your allowed CPU quota:

```shell
kubectl scale --replicas 3 deployment nginx-guaranteed
```

Next we apply some load to the sentence application, first create a multitool
POD in which we can run the load generator tool:

```shell
kubectl create deployment multitool --image praqma/network-multitool
```

Start a shell in the multitool container:

```shell
kubectl exec -it <pod name> -- bash
```

and run a load generator (Apache Bench):

```shell
ab -n 100000000 -c 10 http://sentences:5000/
```

> A single load generator should be sufficient for this exercise, however,
> additional load generators can be created by scaling the multitool deployment
> and running more `ab` commands.

Create a HorizontalPODAutoscaler object to automatically scale the sentence
application:

```shell
kubectl apply -f sentences-app/deploy/hpa.yaml
```

With load being applied to the sentence application, the HorizontalPODAutoscaler
will increase the replica count, however, the newly created `sentence` POD will
remain in `Pending` as shown below in the POD listing:

```
NAME                                READY   STATUS    RESTARTS   AGE
multitool-5b5bc555c8-txnct          1/1     Running   0          3h42m
nfs-provisioner-6587fdd6f6-cqmcs    1/1     Running   0          3h45m
nginx-guaranteed-6479bf87df-72t7c   1/1     Running   0          28m
nginx-guaranteed-6479bf87df-p4fnr   1/1     Running   0          28m
nginx-guaranteed-6479bf87df-r6cfn   1/1     Running   0          60m
sentence-age-c569ddff5-27q8z        1/1     Running   0          11m
sentence-name-65486ccf55-5m4wm      1/1     Running   0          11m
sentences-6bd76d66ff-7tj6f          0/1     Pending   0          9m28s
sentences-6bd76d66ff-nm5b7          1/1     Running   0          11m
```

This is because all our PODs have the same priority, i.e. no PODs are evicted to
make room for our new POD. To see the QoS class and priority of all PODs, try
the following command:

```shell
kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.qosClass}{"\t"}{.spec.priority}{"\n"}{end}'
```

This will show that all our PODs have a priority of zero.

To ensure that the sentence application is able to evict the PODs from the nginx
deployment, we need to increase the POD priority of the sentence application.

> The following assumes some pre-deployed priority classes. If you are running this on a self-managed Kubernetes cluster, you might need to deploy `resources/priority-classes.yaml` yourself.

To see which PriorityClasses we have available, use the following command:

```shell
kubectl get priorityclasses
```

This will show, that we have a `medium-priority` class with a priority value of
`100`. Next change the sentence application deployment and redeploy the sentence
application:

**Note**: The sentence application consist of three deployment, and its the one
named `sentences` in the file
`sentences-app/deploy/kubernetes/sentences-deployment.yaml` file which is not
able to scale. *Will it be sufficient to add a priority to this main
microservice?* When the Kubernetes scheduler evicts a POD to make room for
another main sentence POD, it will choose one of the other PODs with a lower
priority. This could be one of the other microservices in the sentence
application, and since the main microservice depends on these, we are basically
breaking the whole application in our effort to scale it!  *We need to add
priority to the other dependent deployments in the sentence application.*

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
