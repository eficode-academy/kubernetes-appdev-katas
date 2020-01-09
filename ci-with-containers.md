# CI with Containers

This exercise will demonstrate unit and component testing of applications using containers.
It will also make you activate the CI system embedded in GitHub called GitHub Actions.

## Initial setup

Our application consists of three microservices:

* [sentences-age](../../../k8s-sentences-age) To output a random number between 0-100.
* [sentences-name](../../../k8s-sentences-name) To output a random name from the group Monty Python.
* [sentences-sentences](../../../k8s-sentences-sentence) That is the frontend, displaying the result from both microservices.

In this excercise we will build, spin up, use and test the docker images

All three applications follows the same structure:

```
.
├── app
├── build-app.sh
├── component-test
├── .git
├── .github
├── helm
├── push-app.sh
├── README.md
├── test
└── unit-test.sh

```

## Familiarizing with the setup

In each of the repositories, we have created a pipeline for the individual applications in the `.github/workflows/` folder.
The pipeline is going through the steps listed below.

`test-code -> build-docker-image -> component-test-docker-image`

* `test-code` runs the unit test through `unit-test.sh`
* `build-docker-image` builds the image, and pushes it up to dockerhub via `build-app.sh` and `push-app.sh`
* `component-test` takes the recently pushed image and runs `test/component-test.sh`

In the section below, we are familiarizing ourselves with the build pipline by hand before enabling it in GitHub Actions.

### Tasks

* Open up each of the three repositories and run the unit test to make sure that everything works:

```shell
$ ./unit-test.sh
=== RUN   TestAgeIntegerShouldBeBetween
--- PASS: TestAgeIntegerShouldBeBetween (0.00s)
    age_test.go:11: GetAge(0, 100) PASSED, expected 16 to be between 0 and 100
PASS
ok  	_/go	0.002s

```

The `unit-test.sh` script runs a (golang)[https://hub.docker.com/_/golang/] image, voluming in the code.

* try enabling the commented-out test in the file [age_test.go](../k8s-sentences-age/app/age_test.go). If you now try to run the command from above, you will see an error instead.
* Comment out the failed test again, so the pipeline will run smooth when set-up.

## Building the app

### Tasks

* run `build-app.sh` on all three applications to make build Docker images for all three
* run `docker image ls` and inspect that all three applications are there as images.

> Note: as shown below, we tag the images both with `1.0-local` and `latest`, but the image ID is still the same.

```bash
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
age                 1.0-local           7a6f2b86b867        4 minutes ago       11.6MB
age                 latest              7a6f2b86b867        4 minutes ago       11.6MB
...
golang              alpine              57ce7b9daa9b        13 days ago         359MB
praqma/vscode       1.39.2              111a3cf43058        3 weeks ago         1.21GB
golang              1.13.4              a2e245db8bd3        6 weeks ago         803MB
```

* Test one of the applications by running the docker image: `docker run -p 8080:8080 age:latest` and inspect the website by opening a browser on your IP:8080
* Terminate your running container with Ctrl+c

## Running Component Tests

Running component tests means that we run a microservice and then test it by making requests to it and validate the responses.

In the application repositories `test/component-test.sh` will run a docker-compose file, compile the python component test image and spinning up the application image and python test system.

The docker containers will hold onto the terminal for output, and return a non 0 exit code if the test fails.

Running tests against the main sentences service (which relies on the `name` and
`age` services), the compose start all three microservices. It is the same command as the two other applications, the docker-compose just have 4 containers instead of 2.

### Tasks

On all three applications

*`cd` into the test folder and run the component-test.sh file, and observe that the python container outputs an OK after executing the tests.

```bash
sut_1  | ...
sut_1  | ----------------------------------------------------------------------
sut_1  | Ran 3 tests in 0.027s
sut_1  | 
sut_1  | OK
ci_sut_1 exited with code 0

```

## Enabling GitHub Actions

Adding secrets:  DOCKER_PW and DOCKER_USER

will be used in the pipeline script

trigger a build, see that you have the images on your docker-hub account.
