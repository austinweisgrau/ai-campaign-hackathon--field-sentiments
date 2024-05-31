docker-build:
	# Build docker image locally
	docker build -t hackathon-field-analysis .

docker-run:
	# Build and run docker image locally
	$(MAKE) docker-build
	/bin/bash scripts/run_docker_local.sh
