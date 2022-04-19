##
## Build
##
FROM golang:1.17-alpine AS build

WORKDIR /app
COPY go.mod ./
COPY go.sum ./
COPY cmd ./cmd
COPY mafio ./mafio
COPY portal ./portal
RUN go mod download
RUN go test -v ./...
RUN go build -o /newCaseList cmd/newCaseList/main.go
RUN go build -o /updateCaseList cmd/updateCaseList/main.go

##
## Deploy
##
# need alpine for using bash, otherwise use scratch
FROM alpine:3.15
RUN apk add bash
COPY --from=build /newCaseList /usr/local/bin/newCaseList
COPY --from=build /updateCaseList /usr/local/bin/updateCaseList

RUN which newCaseList
RUN which updateCaseList
