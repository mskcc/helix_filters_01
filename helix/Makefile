SHELL:=/bin/bash
.ONESHELL:
UNAME:=$(shell uname)

# SETUP DEVELOPMENT ENVIRONMENT FROM HERE: https://github.com/stevekm/go-env

# project setup:
# $ go mod init helix
# $ go get github.com/google/go-cmp
# $ go get github.com/google/go-cmp/cmp
# $ go install github.com/google/go-cmp/cmp
# gofmt -l -w .

# run the test cases
test:
	set -euo pipefail
	go clean -testcache && \
	go test -v ./... | sed ''/PASS/s//$$(printf "\033[32mPASS\033[0m")/'' | sed ''/FAIL/s//$$(printf "\033[31mFAIL\033[0m")/''


BUILD_DIR:=$(CURDIR)/bin
build:
	mkdir -p "$(BUILD_DIR)"
	go build -o "$(BUILD_DIR)/newCaseList" cmd/newCaseList/main.go
	go build -o "$(BUILD_DIR)/updateCaseList" cmd/updateCaseList/main.go
	go build -o "$(BUILD_DIR)/filterUncalledMutations" cmd/filterUncalledMutations/main.go

build-test: $(BUILD_DIR)/newCaseList $(BUILD_DIR)/updateCaseList
	./bin/newCaseList all foo Sample1,Sample2,Sample2 > cases.txt
	./bin/updateCaseList cases.txt Sample2,Sample3
	rm -f cases.txt


# make the Docker container
GIT_NAME:=helix
# this should default to 'latest'
GIT_TAG:=$(shell git describe --tags --abbrev=0)
DOCKER_TAG:=mskcc/$(GIT_NAME):$(GIT_TAG)
docker-build:
	docker build -t "$(DOCKER_TAG)" .
# --no-cache

docker-push:
	docker push "$(DOCKER_TAG)"
