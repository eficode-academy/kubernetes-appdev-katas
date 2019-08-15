# Helm Chart with Parameters

This exercise will demonstrate adding parameters to a Helm chart to allow
customization of the installed application.

This exercise extends the Helm chart created in the
[create-a-helm-chart](create-a-helm-chart.md) exercise.

We will add the following options for customization:

- Configurable resource naming (using Helm built-in values)
- Configurable number of POD replicas in deployments (using single-value parameters with defaults)
- Configurable resource settings (using list-type value parameters)
- Optional definitions (using if/else constructs)

when we initially created the Hel chart we did it with an empty values.yaml
file.  Now replace the values.yaml with the following content:

```

```

> Note that the Helm best practices suggests using a flat values file vs. a
> nested one as shown above. Real-world charts however, very often use nested
> values and this is probably the defacto standard.

This values.yaml file shows:

- Using double `##` for documentation comments and single `#` for commented-out fields. This is not an official Helm standard but a very common approach.
- Image name and tag are separately configurable. This is a common pattern because e.g. the tag typically is configured independently from the image name.
- Resources are not defaulted in values.yaml. We cannot know the proper settings and instead we provide an empty map and allows users to set appropriate resource requests.
- Node-port (which is only relevant in case the Kubernetes service is of type `NodePort`) has no default. Again, we cannot know the proper default but instead indicate in the values.yaml file that there is a parameter that can be configured. Another typically used alternative for string-type values is to leave them as empty strings.

## Adding Parameters to the Chart

Now we need to update the chart template files such that values are inserted at
the appropriate places. We do that using the `{{` and `}}` template language
constructions.

In the `sentences-deployment.yaml` file, locate the specification of the number of replicas:

```
...
spec:
  replicas: 1
...
```

and change it to:

```
...
spec:
  replicas: {{ .Values.sentences.replicas }}
...
```

Verify the rendering as follows:

```shell
$ helm template sentence-app/ -x templates/sentences-deployment.yaml
```

Since values.yaml have a default replica count of 1, you will see no changes,
however, you can try changing the default, or explicitly override the value in
the helm invocation as follows:

```shell
$ helm template sentence-app/ -x templates/sentences-deployment.yaml --set sentences.replicas=3
```

Similarly, change the container image specification as follows:

```
...
      - image: {{ .Values.sentences.image.repository }}:{{ .Values.sentences.image.tag }}
...
```

and change the Deployment name as follows:

```
...
  name: {{ .Release.Name }}-sentences
...
```

The resource section is slightly different since this is not a single value but
instead a full YAML map. Also, we do not know whether the user will specify
limits or requests for either CPU or memory since all this is related to the
actual usage.

Instead we simply insert the full YAML as given by the user. To do this we use a
Helm function and pipeline as follows:

```
...
        resources:
{{ toYaml .Values.sentences.resources | indent 10 }}
...
```

As before, validate the resource setting with:

```shell
$ helm template sentence-app/ --set sentences.resources.requests.cpu=0.25 -x templates/sentences-deployment.yaml
```

## Values Files

When multiple variables needs to be set, its more convenient to have them
collected in files. Try this by creating a file called `values-resources.yaml`
with the following content:

```
sentences:
  resources:
    requests:
      cpu: 0.25
    limits:
      cpu: 0.25
```

and test template rendering with:

```shell
$ helm template sentence-app/ --values values-resources.yaml -x templates/sentences-deployment.yaml
```

Validate the chart and install the sentences application using the new chart:

```shell
$ helm lint sentence-app/
$ helm install --name sentences sentence-app/
```

This will install the chart with the default values. Try upgrading the chart
using an increased replica count:

```shell
$ helm upgrade sentences sentence-app/ --set sentences.replicas=3
```

Finally, inspect the chart status and actual values:

```shell
$ helm list
$ helm get sentences
```

Note that the `get` operation show the used values in the beginning.

## Cleanup

Delete the application installed with Helm:

```shell
$ helm delete sentences --purge
```
