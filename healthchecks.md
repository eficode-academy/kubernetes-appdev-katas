# Kubernetes health checks

## Learning goal

- Creating healthchecks
- Examine how the two probes work.

## Overview

Health checks in Kubernetes are a mechanism to
check if a pod is able to handle load. This status
can be used by Kubernetes to avoid routing traffic
to pods which are unhealthy, or automatically
recreate unhealthy pods.

Kubernetes has two built-in ways of making a
health check on a pod:

- _readiness probes_ that finds out if your pod is
  ready to receive traffic
- _liveness probes_ that finds out if your pod is
  alive and well

When we use `kubectl` to print the status of a
pod, we receive information on the status of the
pod.

```
NAME                     READY   STATUS    RESTARTS   AGE
probe-59cf4f5578-vwllc   1/1     Running   1          10m
```

In this example, "1/1" in the READY-column means
shows the amount of containers in this pod which
Kubernetes identified to be in the READY-state.

The difference between a container being healthy
or unhealthy, is vital. A container can be
creating, failing or otherwise deployed but
unavailable - and in this state Kubernetes will
choose not to route traffic to the container if it
deems it unhealthy.

## Exercise

Apply the deployment and service found in the
`health-checks` folder:

- `kubectl apply -f health-checks/probes.yaml `
- `kubectl apply -f health-checks/probes-svc.yaml`
- Try to access the service through the public IP
  of one of the nodes.

<details>
<summary>:bulb: How is it that you do that?</summary>

- Find the service with `kubectl get services` command.

- Note down the port number for the probes service.

- Get the nodes EXTERNAL-IP address. Run `kubectl get nodes -o wide`.

Copy the external IP address of any one of the nodes, for example, `34.244.123.152` and paste it in your browser.

Copy the port from your frontend service that looks something like `31941` and paste it next to your IP in the browser, for example, `34.244.123.152:31941` and hit it.

</details>

- Scale the deployment by changing the `replicas`
  amount to 2 in the `probes.yaml`
- Again, access the application through your
  browser. Refresh the page multiple times such
  that you hit both of the instances
- Execute a bash session in one of the instances
  `kubectl exec -ti probe-59cf4f5578-vwllc -- bash`
- First, remove the file `/tmp/ready`, and monitor that the browser will eventually not route traffic to that pod.
- Run `kubectl get pods` to see that the pod you executed into are not ready anymore.
- Run `kubectl describe pod probe-59cf4f5578-vwllc` and see that the conditions for the pod are describing it as not ready:

```bash
Conditions:
  Type              Status
  Initialized       True 
  Ready             False 
  ContainersReady   False 
  PodScheduled      True 
```

- Remove the file `/tmp/alive`, and observe that within a short while you will get kicked out of the container, as the pod is restarting.
- Observe that the pod has now been restarted when you list the pods with `kubectl get pods`
- Look at the events:  `kubectl describe pod probe-59cf4f5578-vwllc` and see the events that you have triggered through this exercise.

Congratulations!

You have now tried out both to pause traffic to a
given pod when its readinessprobe is failing, and
trigger a pod restart when the livelinessprobe is
failing.

## Clean up

```
kubectl delete -f health-checks
```
