# Testing with Containers

This exercise will demonstrate unit and component testing of applications using
containers.  It will use the application container built in the
[hello-sentences-app](hello-sentences-app.md) exercise.

The following exercise assumes commands are being run from the sentences-app
folder:

```shell
$ cd sentences-app
```

## Running Unit Tests

```shell
$ python -m unittest discover unit_tests/
```

This will run the unit tests locally and produce the following output:

```
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

While this is quick and convenient, it has the problem that it requires all test
requirements installed locally in the proper versions and with the proper
configuration. With real-world applications and CI/CD systems that build
software using different versions this becomes increasingly complex.

Below we will run the tests using a container such that testing becomes
independent of locally installed software (except for the ability to run
containers).

### Running Tests with a Container

The unit test Python requirements are defined in the
[test_requirements.txt](sentences-app/test_requirements.txt) file. When we build a container
to run the tests, we can add these requirements with the following lines in the
Dockerfile we use to build the container (`pip` is the python package
installer).:

```
COPY test_requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/test_requirements.txt
```

Next, we can also add the unit tests to the container with the following lines
in the Dockerfile:

```
COPY tests/*.py /usr/src/app/tests/
COPY unit_tests/*.py /usr/src/app/unit_tests/
```

Together with the application source code there is also a
[Dockerfile_test](sentences-app/Dockerfile_test) which contain the lines mentioned above and
which we can use to build a testing container. Use the following command to
build the testing container:

```shell
$ docker build -t sentences-test:v1 -f Dockerfile_test .
```

Since the current version of the testing container includes a fixed version of
the unit tests, we can either run this specific version of the unit tests, or we
can run unit tests which we have locally.

Use the following command to point the unit test framework inside the container
to the version of the unit tests that are also stored within the
container. Running unit tests this way should ensure that can be executed in a
reproducible manner.

```shell
$ docker run --rm -v $PWD:/src:ro -w /src sentences-test:v1 -m unittest discover -s /usr/src/app/unit_tests
```

If we change any of the unit tests we need to build a new test container
image. However, we can also point the test framework inside the container to the
local version of the unit tests with the following command:

```shell
$ docker run --rm -v $PWD:/src:ro -v $PWD/unit_tests:/unit_tests:ro -w /src sentences-test:v1 -m unittest discover -s /unit_tests
```

> To see the effect of changing the unit tests try enabling the commented-out
> test in the file [test_unit_tests.py](sentences-app/unit_tests/test_unit_tests.py). If you
> now try the two commands from above, you will see a different number of unit
> tests being executed.

## Running Component Tests

Running component tests means that we run a microservice and then test it by
making requests to it and validate the responses.

First, run the `name` microservice using docker:

```shell
$ docker run --rm -p8889:5000 sentences:v1 --mode name
```

This will start the `name` service on the local host (IP address 127.0.0.1, port 8889).

The docker container will hold onto the terminal for debug output, i.e. run the
following command in another shell (remember to change to the `sentences-app`
folder).

To run tests against this service, pass the URL to the name service to the tests
inside the testing container using an environment variable and run the
name-servce tests with the following command:

```shell
$ docker run --rm --net host -e SERVICE_URL='http://127.0.0.1:8889' sentences-test:v1 /usr/src/app/tests/test_name_service.py
```

Running tests against the main sentences service (which relies on the `name` and
`age` services), we need to start all three microservices. We can do this with
docker-compose with the following command:

```shell
$ docker-compose -f deploy/docker-compose.yaml up
```

Run tests again the main sentences service with the following command:

```shell
$ docker run --rm --net host sentences-test:v1
```

> When running tests against the main sentences service we didn't specify any
> URL or test suite. How does this work?

> Running component tests from locally stored tests are left as an exercise to
> the reader.


## Cleanup

Stop any running containers and docker-compose deployments by pressing Ctrl-C.
