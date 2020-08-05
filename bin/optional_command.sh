#!/bin/bash

command=$1
shift
arguments=$@
eval "$command $arguments" || touch failed.txt
