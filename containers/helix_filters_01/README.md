Image that by default builds from "master" branch.

Can provide a branch, tag, or commit hash by using COMMIT_VERSION ARG.

For example:

```
docker build --build-arg COMMIT_VERSION="bda2c6ef61168e3e0c170f993ca8f96da9fb48b4" -f helix_filters_01/Dockerfile .
```
