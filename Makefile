build:
	@docker build \
		-t anderson89marques/bbscraper .

run:
	@docker container run \
		-it anderson89marques/bbscraper:latest bbscraper