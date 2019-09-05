# Testing with Containers

This exercise will demonstrate unit and component testing of applications using
containers.  It will use the application container built in the TBD exercise.

## Running Unit Tests

```shell
$ cd sentences-app
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
[test_requirements.txt](sentence_app/test_requirements.txt) file. When we build a container
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
[Dockerfile_test](sentence_app/Dockerfile_test) which contain the lines mentioned above and
which we can use to build a testing container. Use the following command to
build the testing container:

```shell
$ cd sentences-app
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
> test in the file [test_unit_tests.py](sentence_app/unit_tests/test_unit_tests.py). If you
> now try the two commands from above, you will see a different number of unit
> tests being executed.


## Running Component Tests
