-include Makefile.local

VERSION ?= 1.0

# Build application test (component and unit test) container image
.PHONY: build-test
build-test:
	docker build -t sentences-test:$(VERSION) -f Dockerfile_test .

# Run stand-alone main service container
.PHONY: run-service
run-service:
	docker run --rm -p8890:8080 hoeghh/sentence:$(VERSION)

# Run stand-alone age service container
.PHONY: run-age-service
run-age-service:
	docker run --rm -p8888:8080 hoeghh/age:$(VERSION)

# Run stand-alone name service container
.PHONY: run-name-service
run-name-service:
	docker run --rm -p8889:8080 hoeghh/name:$(VERSION)

# Run all containers of the sentence app, access main service on port 8890 and metrics on 8891
.PHONY: run-full-service
run-full-service:
	docker-compose -f deploy/docker-compose.yaml up

# Run full-service component test against services running locally on 127.0.0.1:8890
.PHONY: run-test
run-test:
	docker run --rm --net host sentences-test:$(VERSION)

# Run age-service component test against services running locally on 127.0.0.1:8888
.PHONY: run-age-service-test
run-age-service-test:
	docker run --rm --net host -e SERVICE_URL='http://127.0.0.1:8892' sentences-test:$(VERSION) /usr/src/app/tests/test_age_service.py

# Run name-service component test against services running locally on 127.0.0.1:8889
.PHONY: run-name-service-test
run-name-service-test:
	docker run --rm --net host -e SERVICE_URL='http://127.0.0.1:8893' sentences-test:$(VERSION) /usr/src/app/tests/test_name_service.py
