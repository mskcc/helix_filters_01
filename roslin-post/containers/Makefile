SHELL:=/bin/bash

export DOCKERTAG:=singularityware/singularity:v3.3.0
export SINGULARITYDIR:=$(CURDIR)/facets-1.6.3
build:
	docker run \
	--privileged \
	--rm \
	-ti \
	-v "$(SINGULARITYDIR):/image" "$(DOCKERTAG)" \
	build /image/facets-1.6.3.sif /image/facets-1.6.3.def

shell:
	docker run \
	--privileged \
	--rm \
	-ti \
	-v "$(SINGULARITYDIR):/image" \
	--entrypoint "/bin/bash" \
	"$(DOCKERTAG)"
