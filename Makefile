docker-build:
	# Build docker image locally
	docker build -t hackathon-field-analysis .

docker-run:
	# Build and run docker image locally
	$(MAKE) docker-build
	/bin/bash scripts/run_docker_local.sh

deploy:
	# Deploy to heroku
	$(MAKE) docker-build
	docker tag hackathon-field-analysis registry.heroku.com/hackathon-field-analysis/web
	heroku container:login
	heroku container:push web
	heroku container:release web -a hackathon-field-analysis
