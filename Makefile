IMG_NAME=shardnova-engine
TAG=local
VOLUME_TO_MOUNT=$(shell pwd)

IMG=shardrealms.com/$(IMG_NAME)
CONTAINER=$(IMG_NAME)
VOLUME_DESTINATION=/home/default

build:
	docker build --pull \
	-t $(IMG):$(TAG) \
	-f Dockerfile .

run-enter: rm
	docker run -it \
	--name $(CONTAINER) \
	-v $(VOLUME_TO_MOUNT):$(VOLUME_DESTINATION) \
	-e ENVIRONMENT=local \
	$(IMG):$(TAG) \
	/bin/bash

run-local: rm
	docker run -d \
	--name $(CONTAINER) \
	-v $(VOLUME_TO_MOUNT):$(VOLUME_DESTINATION) \
	-e ENVIRONMENT=local \
	$(IMG):$(TAG)

push:
	docker push \
	$(IMG):$(TAG)

rm:
	docker rm \
	-f $(CONTAINER) || true

run-test: 
	docker run \
	--name $(CONTAINER)_test --rm  \
	$(IMG):$(TAG) \
	make _test

_test:
	make unit-test-python
	make functional-test-python
	make integration-test

unit-test-python:
	@echo "### Running Python unit tests ###"
	@echo "### Finished Python unit tests ###"

functional-test-python:
	@echo "### Running Python functional tests ###"
	@echo "### Finished Python functional tests ###"

integration-test:
	@echo "### Running integration tests ###"
	@echo "### Finished integration tests ###"

# tags the image with the most recent git commit
tag:
	$(eval TAG := $(shell git rev-parse --verify HEAD))