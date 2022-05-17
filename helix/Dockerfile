##
## Build
##
FROM golang:1.17-alpine AS build

RUN apk update && apk add gcc musl-dev

WORKDIR /app
COPY go.mod ./
COPY go.sum ./
COPY cmd ./cmd
COPY mafio ./mafio
COPY portal ./portal
COPY testdata ./testdata
RUN go mod download
RUN go test -v ./...
RUN go build -o /newCaseList cmd/newCaseList/main.go
RUN go build -o /updateCaseList cmd/updateCaseList/main.go
RUN go build -o /filterUncalledMutations cmd/filterUncalledMutations/main.go

##
## Deploy
##
# need alpine for using bash, otherwise use scratch
FROM alpine:3.15
RUN apk add bash
COPY --from=build /newCaseList /usr/local/bin/newCaseList
COPY --from=build /updateCaseList /usr/local/bin/updateCaseList
COPY --from=build /filterUncalledMutations /usr/local/bin/filterUncalledMutations

RUN which newCaseList
RUN which updateCaseList
