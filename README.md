# Roslin Analysis Helix Filters and Post Processing Workflows 

#### [[DockerHub](https://hub.docker.com/repository/docker/mskcc/helix_filters_01)]

This repo contains scripts and workflows for usage with the Roslin pipeline in order to filter variant calling results

The subdir "roslin-post" is meant to include the main helix filter workflow + extra cBio Portal file generations (in development)

Example usage of this helix filter workflow:

```
make run PROJ_ID=My_Project MAF_DIR=/path/to/outputs/maf FACETS_DIR=/path/to/outputs/facets OUTPUT_DIR=/path/to/helix_filters TARGETS_LIST=/juno/work/ci/resources/roslin_resources/targets/HemePACT_v4/b37/HemePACT_v4_b37_targets.ilist
```

check the file 'ref/roslin_resources.json' to find the correct target set for your assay type

See the 'help' text in the Makefile for the most up to date instructions;

```
make help
```

## Run the test suite

```
make test
```

- NOTE: requires the fixtures directory on juno
