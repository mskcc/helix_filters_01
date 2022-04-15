SHELL:=/bin/bash
.ONESHELL:
UNAME:=$(shell uname)

# project setup:
# $ go mod init helix
# $ go get github.com/google/go-cmp
# $ go get github.com/google/go-cmp/cmp
# $ go install github.com/google/go-cmp/cmp

# run the test cases
test:
	set -euo pipefail
	go test -v ./... | sed ''/PASS/s//$$(printf "\033[32mPASS\033[0m")/'' | sed ''/FAIL/s//$$(printf "\033[31mFAIL\033[0m")/''


BUILD_DIR:=$(CURDIR)/bin
build:
	mkdir -p "$(BUILD_DIR)"
	go build -o "$(BUILD_DIR)/newCaseList" cmd/newCaseList/main.go
	go build -o "$(BUILD_DIR)/updateCaseList" cmd/updateCaseList/main.go

# make the Docker container
GIT_NAME:=helix
# this should default to 'latest'
GIT_TAG:=$(shell git describe --tags --abbrev=0)
DOCKER_TAG:=mskcc/$(GIT_NAME):$(GIT_TAG)
docker-build:
	docker build --no-cache -t "$(DOCKER_TAG)" .
